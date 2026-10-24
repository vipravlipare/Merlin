"""Input rules to call before a future API writes notes or account email."""

from dataclasses import dataclass

import emoji
import regex

# A grapheme is one displayed character, even when several Unicode parts form it.
_GRAPHEMES = regex.compile(r"\X")
MAX_TITLE_WEIGHTED_LENGTH = 175
MAX_BODY_WEIGHTED_LENGTH = 7000


def _validated_graphemes(value: str) -> list[str]:
    """Validate PostgreSQL-compatible text, then split it into display units."""
    if not isinstance(value, str):
        raise ValueError("Text must be a string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise ValueError("Text must be valid UTF-8") from None
    if "\x00" in value:
        raise ValueError("PostgreSQL text cannot contain NUL")
    return _GRAPHEMES.findall(value)


def weighted_length(value: str) -> int:
    """Count a known displayed emoji as four, every other grapheme as one."""
    # The pinned emoji library recognizes complete sequences, such as a family emoji.
    return sum(4 if emoji.is_emoji(part) else 1 for part in _validated_graphemes(value))


def truncate_weighted(value: str, limit: int) -> str:
    """Keep the longest grapheme-safe prefix within a weighted text limit."""
    if type(limit) is not int or limit < 0:
        raise ValueError("Text limit must be a nonnegative integer")

    kept: list[str] = []
    used = 0
    for part in _validated_graphemes(value):
        weight = 4 if emoji.is_emoji(part) else 1
        if used + weight > limit:
            break
        kept.append(part)
        used += weight
    return "".join(kept)


def normalize_email(value: str | None) -> str | None:
    """Preserve display casing; database lower(email) enforces uniqueness."""
    if value is None:
        return None
    weighted_length(value)  # Reject invalid text, not validate email ownership.
    # Remove edge whitespace; an empty result becomes the database NULL value.
    return value.strip() or None


# This result carries a decision; it never writes to or deletes from the database.
@dataclass(frozen=True)
class ValidatedNote:
    title: str | None
    body: str
    delete_on_save: bool


def validate_note(title: str | None, body: str | None, *, is_draft: bool = False) -> ValidatedNote:
    """Normalize absent text and identify an explicitly saved blank note."""
    # Enforce strict boolean type checking
    if not isinstance(is_draft, bool):
        raise ValueError("is_draft must be a boolean")
    # A whitespace-only title is absent; keep the original text of a real title.
    if title is not None:
        title_length = weighted_length(title)
        if not title.strip():
            title = None
        elif title_length > MAX_TITLE_WEIGHTED_LENGTH:
            raise ValueError("Title exceeds weighted length 175")
    # Do not strip the body: spaces and line breaks may be part of the writing.
    body = "" if body is None else body
    if weighted_length(body) > MAX_BODY_WEIGHTED_LENGTH:
        raise ValueError("Body exceeds weighted length 7000")
    # Explicitly saving a blank note requests deletion; a blank draft may stay.
    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())
