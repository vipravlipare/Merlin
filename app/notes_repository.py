"""Read the signed-in actor's active notes from PostgreSQL.

This module is an internal repository layer. It does not create an HTTP route
or authenticate anyone. A future route must pass an actor UUID resolved from
trusted authentication, never a user ID copied from request data.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

import psycopg
from psycopg.pq import TransactionStatus

from app.note_rules import MAX_TITLE_WEIGHTED_LENGTH, truncate_weighted


@dataclass(frozen=True)
class ActiveNoteListItem:
    """Fields shown for one note; title is stored title or body preview."""
    id: UUID
    title: str
    updated_at: datetime


def list_active_notes(
    conn: psycopg.Connection,
    actor_id: UUID,
) -> list[ActiveNoteListItem]:
    """Return one actor's non-trash notes, newest content edit first.

    The caller must resolve ``actor_id`` from trusted authentication. Tests may
    use synthetic UUIDs to exercise database ownership rules; that does not
    make this function an authentication boundary.

    This function requires an idle connection so its transaction-local actor
    setting cannot leak into another operation in a caller-owned transaction.
    The connection remains owned by the caller and is not closed here.
    """
    if not isinstance(actor_id, UUID):
        raise ValueError("A trusted actor UUID is required")

    # Do not create a savepoint inside someone else's transaction: PostgreSQL
    # keeps SET LOCAL values until the outer transaction ends.
    if conn.info.transaction_status is not TransactionStatus.IDLE:
        raise RuntimeError("Notes listing requires an idle database connection")

    # Own one transaction so the actor setting always resets at its end.
    with conn.transaction():
        with conn.cursor() as cur:
            # Let PostgreSQL reject accidental writes in this list operation.
            cur.execute("SET TRANSACTION READ ONLY")
            # The third argument makes this custom setting transaction-local.
            # Bind the UUID as data; never interpolate actor input into SQL.
            cur.execute(
                "SELECT set_config('merlin.actor_id', %s, true)",
                (str(actor_id),),
            )
            # The view excludes trash. The explicit owner filter also makes
            # the intended scope visible in this query and supports its index.
            cur.execute(
                """
                SELECT id, title, body, updated_at
                FROM public.active_notes
                WHERE user_id = %s
                ORDER BY updated_at DESC, id ASC
                """,
                (actor_id,),
            )
            rows = cur.fetchall()

    # Convert database rows to a small immutable result type after commit.
    items = []
    for note_id, stored_title, body, updated_at in rows:
        # Untitled notes use the same weighted cap as real titles. The helper
        # preserves complete graphemes and emoji sequences at the boundary.
        display_title = (
            stored_title
            if stored_title is not None
            else truncate_weighted(body, MAX_TITLE_WEIGHTED_LENGTH)
        )
        items.append(
            ActiveNoteListItem(
                id=note_id,
                title=display_title,
                updated_at=updated_at,
            )
        )
    return items
