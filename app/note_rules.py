"""Input rules to call before a future API writes notes or account email."""

from dataclasses import dataclass

import emoji
import regex

# A grapheme is one displayed character, even when several Unicode parts form it.
_GRAPHEMES = regex.compile(r"\X")


def weighted_length(value: str) -> int:
    """Count a known displayed emoji as four, every other grapheme as one."""
    if not isinstance(value, str):
        raise ValueError("Text must be a string")
    try:
        value.encode("utf-8")
    except UnicodeEncodeError:
        raise ValueError("Text must be valid UTF-8") from None
    if "\x00" in value:
        raise ValueError("PostgreSQL text cannot contain NUL")
    # The pinned emoji library recognizes complete sequences, such as a family emoji.
    return sum(4 if emoji.is_emoji(part) else 1 for part in _GRAPHEMES.findall(value))


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
        elif title_length > 175:
            raise ValueError("Title exceeds weighted length 175")
    # Do not strip the body: spaces and line breaks may be part of the writing.
    body = "" if body is None else body
    if weighted_length(body) > 7000:
        raise ValueError("Body exceeds weighted length 7000")
    # Explicitly saving a blank note requests deletion; a blank draft may stay.
    return ValidatedNote(title, body, not is_draft and title is None and not body.strip())
