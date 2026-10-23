"""Decode bounded local-provider records and require clean completion."""

import json
import math
import re
from collections.abc import Iterable
from typing import Any


_ERROR_MESSAGES = {
    "invalid-response": "Invalid model response.",
    "incomplete-response": "Model response was incomplete.",
    "limit-exceeded": "Model response exceeded a limit.",
    "provider-failure": "Local model request failed.",
    "length-limited": "Model response reached its output limit.",
    "canceled": "Model request was canceled.",
}


class ProviderError(Exception):
    """Expose only an agreed category and fixed public message."""

    def __init__(self, category: str = "invalid-response") -> None:
        super().__init__(_ERROR_MESSAGES[category])
        self.category = category


def _check_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject JSON objects containing duplicate keys."""
    fields = {}
    for key, value in pairs:
        if key in fields:
            raise ProviderError()
        fields[key] = value
    return fields


def _parse_strict_float(val_str: str) -> float:
    """Parse float and reject non-finite numbers (including 1e999 which overflows to infinity)."""
    val = float(val_str)
    if not math.isfinite(val):
        raise ProviderError()
    return val


def _parse_constant_handler(val_str: str) -> float:
    """Explicitly reject NaN, Infinity, and -Infinity constant literals."""
    raise ProviderError()


def _is_truncated_json(error: json.JSONDecodeError) -> bool:
    """Recognize the supported unfinished JSON suffixes at EOF."""
    record_str = error.doc
    tail = record_str[error.pos:]
    unfinished_number = re.search(
        r'(?:^|[\s\[:,])-?(?:0|[1-9][0-9]*)(?:\.|(?:\.[0-9]+)?[eE][+-]?)$',
        record_str,
    )
    return (
        error.pos >= len(record_str.rstrip())
        or error.msg.startswith("Unterminated string")
        or (error.msg == "Expecting value" and bool(tail) and any(
            literal.startswith(tail) and literal != tail
            for literal in ("true", "false", "null")
        ))
        or (error.msg == "Expecting value" and tail == "-")
        or (error.msg == "Invalid \\uXXXX escape"
            and bool(re.fullmatch(r"u[0-9a-fA-F]{0,3}", tail)))
        # The parser must have reached this number. A later numeric suffix
        # cannot hide a syntax error that occurred earlier in the record.
        or (error.msg == "Expecting ',' delimiter" and unfinished_number is not None
            and error.pos >= unfinished_number.start()
            and record_str[error.pos:error.pos + 1] in {".", "e", "E"})
    )


class LocalProviderDecoder:
    """
    Stateful decoder enforcing strict byte limits, UTF-8/JSON validation,
    model verification, and safety constraints.
    """
    MAX_RECORD_BYTES = 65536
    MAX_TOTAL_BYTES = 262144

    def __init__(self, expected_model: str) -> None:
        self.expected_model = expected_model
        self.done_received: bool = False
        self.total_bytes: int = 0
        self.buffer: bytearray = bytearray()
        self.text_fragments: list[str] = []

    def feed(self, chunk: bytes) -> None:
        """Process an incoming byte chunk with strict byte-cap and type guards."""
        # Prevent raw TypeError by validating input type upfront
        if not isinstance(chunk, bytes):
            raise ProviderError()

        chunk_len = len(chunk)
        if self.total_bytes + chunk_len > self.MAX_TOTAL_BYTES:
            raise ProviderError("limit-exceeded")

        self.total_bytes += chunk_len
        # Copy at most one bounded record, even when a chunk contains many lines.
        start = 0
        view = memoryview(chunk)
        while start < chunk_len:
            newline = chunk.find(b'\n', start)
            end = chunk_len if newline == -1 else newline + 1
            if len(self.buffer) + end - start > self.MAX_RECORD_BYTES:
                raise ProviderError("limit-exceeded")
            self.buffer.extend(view[start:end])
            if newline == -1:
                break
            record_bytes = bytes(self.buffer[:-1])
            self.buffer.clear()
            self._process_record(record_bytes)
            start = end

    def _process_record(self, record_bytes: bytes, *, final: bool = False) -> None:
        # Decode strict UTF-8 (avoiding internal exception chaining to prevent information leakage)
        try:
            record_str = record_bytes.decode('utf-8', errors='strict')
        except UnicodeDecodeError as error:
            category = "incomplete-response" if (
                final and not self.done_received
                and error.reason == "unexpected end of data"
            ) else "invalid-response"
            raise ProviderError(category) from None

        # Ignore bounded whitespace-only records, including a blank EOF tail.
        if not record_str.strip():
            return

        # Decode strict JSON with duplicate key, finite float, and constant rejections
        try:
            data = json.loads(
                record_str,
                object_pairs_hook=_check_duplicate_keys,
                parse_float=_parse_strict_float,
                parse_constant=_parse_constant_handler
            )
        except json.JSONDecodeError as error:
            # Only an unfinished final record is truncation. Earlier syntax
            # errors remain invalid even when the source omits a final LF.
            truncated = _is_truncated_json(error)
            category = "incomplete-response" if (
                final and not self.done_received and truncated
            ) else "invalid-response"
            raise ProviderError(category) from None
        except (ValueError, RecursionError):
            # Includes malformed JSON, oversized integers and excessive nesting.
            raise ProviderError() from None

        if not isinstance(data, dict):
            raise ProviderError()

        # Safe errors: Reject ANY error member present (even if null or false) with fixed messages/categories
        if "error" in data:
            raise ProviderError("provider-failure")

        if self.done_received:
            raise ProviderError()

        # Validate model field presence, type, and expected_model match
        if "model" not in data or not isinstance(data["model"], str):
            raise ProviderError()

        if data["model"] != self.expected_model:
            raise ProviderError()

        # Validate 'done' field is required and strictly a boolean
        if "done" not in data or not isinstance(data["done"], bool):
            raise ProviderError()

        if "eval_count" in data:
            count = data["eval_count"]
            if type(count) is not int or count < 0:
                raise ProviderError()
            if count > 64:
                raise ProviderError("limit-exceeded")

        # Nonterminal records require text; terminal records may be metadata-only.
        if "response" not in data and not data["done"]:
            raise ProviderError()

        response_val = data.get("response", "")
        if not isinstance(response_val, str):
            raise ProviderError()

        if data["done"] and data.get("done_reason") == "length":
            raise ProviderError("length-limited")

        self.text_fragments.append(response_val)
        self.done_received = data["done"]


def decode_response(chunks: Iterable[bytes], *, expected_model: str) -> str:
    """
    Interface function to decode chunks, validate protocol rules, and return assembled text.
    expected_model is required and keyword-only.
    """
    decoder = LocalProviderDecoder(expected_model=expected_model)
    # Catch source failures only around iterator acquisition/advancement;
    # parser/programmer failures must not be mislabeled as transport failures.
    try:
        source = iter(chunks)
    except OSError:
        raise ProviderError("provider-failure") from None
    while True:
        try:
            chunk = next(source)
        except StopIteration:
            break
        except OSError:
            raise ProviderError("provider-failure") from None
        decoder.feed(chunk)

    # LF is optional on the final record; EOF itself never grants completion.
    if decoder.buffer:
        decoder._process_record(bytes(decoder.buffer), final=True)
        decoder.buffer.clear()

    answer = "".join(decoder.text_fragments)
    if not decoder.done_received or not answer:
        raise ProviderError("incomplete-response")
    return answer
