"""Day 9 record validation and clean-completion regressions."""

import json
import traceback

import pytest

from app.local_provider import LocalProviderDecoder, ProviderError, decode_response


MODEL = "qwen3:0.6b"


def record(**updates):
    data = {"model": MODEL, "response": "Hi", "done": False}
    data.update(updates)
    return (json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


def padded_record(size, ending=b"\n", *, done=False, padding_character="x"):
    base = record(padding="", done=done)[:-1]
    assert size >= len(base) + len(ending)
    remaining = size - len(base) - len(ending)
    encoded = padding_character.encode("utf-8")
    count, remainder = divmod(remaining, len(encoded))
    return base[:-2] + encoded * count + b"x" * remainder + base[-2:] + ending


def test_every_split_preserves_unicode_and_order():
    wire = record(response="café") + record(response="🙂!", done=True)
    for offset in range(len(wire) + 1):
        assert decode_response([wire[:offset], b"", wire[offset:]], expected_model=MODEL) == "café🙂!"
    assert decode_response((wire[i:i + 1] for i in range(len(wire))), expected_model=MODEL) == "café🙂!"


@pytest.mark.parametrize("ending", [b"\n", b"\r\n"])
def test_record_cap_accepts_exact_boundary_and_rejects_one_over_before_copy(ending):
    wire = padded_record(65536, ending)
    decoder = LocalProviderDecoder(MODEL)
    decoder.feed(wire)
    assert decoder.text_fragments == ["Hi"]
    assert not decoder.buffer
    with pytest.raises(ProviderError) as error:
        decoder.feed(padded_record(65537, ending))
    assert error.value.category == "limit-exceeded"
    assert str(error.value) == "Model response exceeded a limit."
    assert len(decoder.buffer) <= 65536


def test_unfinished_record_cannot_grow_past_limit():
    decoder = LocalProviderDecoder(MODEL)
    decoder.feed(b"x" * 65536)
    with pytest.raises(ProviderError, match="^Model response exceeded a limit\\.$"):
        decoder.feed(b"x")
    assert len(decoder.buffer) == 65536


def test_large_coalesced_chunk_and_total_cap_count_metadata_and_blank_bytes():
    decoder = LocalProviderDecoder(MODEL)
    wire = padded_record(65536) * 4
    decoder.feed(wire)
    assert decoder.total_bytes == 262144
    assert decoder.text_fragments == ["Hi"] * 4
    assert not decoder.buffer
    with pytest.raises(ProviderError) as error:
        decoder.feed(b"\n")
    assert error.value.category == "limit-exceeded"
    assert decoder.total_bytes == 262144


@pytest.mark.parametrize("number", ["NaN", "Infinity", "-Infinity", "1e999", "-1e999"])
def test_nonfinite_numbers_are_rejected_even_in_nested_metadata(number):
    wire = record()[:-2] + b',"metadata":{"value":' + number.encode() + b'}}\n'
    with pytest.raises(ProviderError) as error:
        decode_response([wire], expected_model=MODEL)
    assert error.value.category == "invalid-response"


@pytest.mark.parametrize("wire", [
    b'{"model":"qwen3:0.6b","response":"Hi","done":false,"done":true}\n',
    record()[:-2] + b',"metadata":{"x":1,"x":2}}\n',
])
def test_duplicate_keys_are_rejected_at_every_object_level(wire):
    with pytest.raises(ProviderError) as error:
        decode_response([wire], expected_model=MODEL)
    assert error.value.category == "invalid-response"


@pytest.mark.parametrize("updates", [
    {"model": "other"}, {"model": None}, {"model": 1},
    {"done": 1}, {"done": "true"}, {"done": None},
    {"response": 1}, {"response": None},
    {"eval_count": -1}, {"eval_count": True}, {"eval_count": 1.5}, {"eval_count": "3"},
])
def test_schema_rejects_wrong_identity_types_and_token_metadata(updates):
    with pytest.raises(ProviderError) as error:
        decode_response([record(**updates)], expected_model=MODEL)
    assert error.value.category == "invalid-response"


@pytest.mark.parametrize("field", ["model", "done", "response"])
def test_required_nonterminal_fields_cannot_be_missing(field):
    data = json.loads(record())
    del data[field]
    with pytest.raises(ProviderError) as error:
        decode_response([(json.dumps(data) + "\n").encode()], expected_model=MODEL)
    assert error.value.category == "invalid-response"


@pytest.mark.parametrize("count", [0, 64])
def test_valid_integer_token_count_boundary(count):
    decoder = LocalProviderDecoder(MODEL)
    decoder.feed(record(eval_count=count))
    assert decoder.text_fragments == ["Hi"]


def test_output_token_count_over_cap_is_a_limit_error():
    with pytest.raises(ProviderError) as error:
        decode_response([record(eval_count=65)], expected_model=MODEL)
    assert error.value.category == "limit-exceeded"


@pytest.mark.parametrize("chunk", ["text", None, bytearray(b"x"), 42])
def test_invalid_chunk_type_has_safe_error(chunk):
    with pytest.raises(ProviderError) as error:
        decode_response([chunk], expected_model=MODEL)
    assert error.value.category == "invalid-response"
    assert str(error.value) == "Invalid model response."


@pytest.mark.parametrize("value", [None, False, "", "SYNTHETIC_PROVIDER_ERROR_SENTINEL"])
def test_any_error_member_overrides_success_fields_without_disclosure(value, capsys):
    with pytest.raises(ProviderError) as error:
        decode_response([record(error=value, done=True)], expected_model=MODEL)
    assert error.value.category == "provider-failure"
    assert str(error.value) == "Local model request failed."
    assert "SYNTHETIC_PROVIDER_ERROR_SENTINEL" not in str(error.value)
    assert capsys.readouterr() == ("", "")


@pytest.mark.parametrize("wire", [
    b'{"SYNTHETIC_PRIVATE_INPUT_SENTINEL": broken}\n',
    b'{"response":"SYNTHETIC_PRIVATE_INPUT_SENTINEL\xff"}\n',
])
def test_malformed_records_do_not_expose_private_exception_chains(wire, capsys):
    with pytest.raises(ProviderError) as error:
        decode_response([wire], expected_model=MODEL)
    assert error.value.category == "invalid-response"
    rendered = "".join(traceback.format_exception_only(error.value))
    assert rendered.strip() == "app.local_provider.ProviderError: Invalid model response."
    assert error.value.__cause__ is None
    assert error.value.__suppress_context__ is True
    assert capsys.readouterr() == ("", "")


def test_truncated_record_does_not_return_preceding_text():
    with pytest.raises(ProviderError) as error:
        decode_response([record(), b"{"], expected_model=MODEL)
    assert error.value.category == "incomplete-response"


def terminal_without_text():
    return (json.dumps({"model": MODEL, "done": True}) + "\n").encode()


@pytest.mark.parametrize("terminal", [terminal_without_text(), record(response="", done=True)])
@pytest.mark.parametrize("tail", [b"", b" \t\r\n", b" \t"])
def test_metadata_completion_waits_for_clean_eof(terminal, tail):
    assert decode_response([record(), terminal, b"", tail], expected_model=MODEL) == "Hi"


@pytest.mark.parametrize("wire,offset", [
    pytest.param(wire[:-1], offset, id=f"{kind}-byte-{offset}")
    for kind, wire in [("terminal-text", record(done=True)),
                       ("metadata-terminal", record()+terminal_without_text())]
    for offset in range(len(wire))
])
def test_final_record_without_newline_accepts_every_split(wire, offset):
    assert decode_response([wire[:offset], wire[offset:]], expected_model=MODEL) == "Hi"


@pytest.mark.parametrize("chunks", [[], [b" \n"], [record()], [terminal_without_text()],
                                   [record(response=""), terminal_without_text()]])
def test_missing_completion_or_empty_answer_is_incomplete(chunks):
    with pytest.raises(ProviderError) as error:
        decode_response(chunks, expected_model=MODEL)
    assert error.value.category == "incomplete-response"


@pytest.mark.parametrize("tail", [record(done=True), record(), b"{", b"\xff"])
@pytest.mark.parametrize("coalesced", [False, True])
def test_nonblank_data_after_completion_is_invalid(tail, coalesced):
    chunks = [record(done=True), tail]
    if coalesced:
        chunks = [b"".join(chunks)]
    with pytest.raises(ProviderError) as error:
        decode_response(chunks, expected_model=MODEL)
    assert error.value.category == "invalid-response"


@pytest.mark.parametrize("prefix", [b"", record(), record(done=True)])
@pytest.mark.parametrize("value", [None, False, 0, {}, "SYNTHETIC_PROVIDER_ERROR_SENTINEL"])
def test_error_precedence_including_after_terminal(prefix, value, capsys):
    with pytest.raises(ProviderError) as error:
        decode_response([prefix, record(error=value, done=True)], expected_model=MODEL)
    assert error.value.category == "provider-failure"
    assert str(error.value) == "Local model request failed."
    assert "SYNTHETIC_PROVIDER_ERROR_SENTINEL" not in "".join(traceback.format_exception(error.value))
    assert capsys.readouterr() == ("", "")


@pytest.mark.parametrize("value", [None, 4, {}, False])
def test_terminal_response_if_present_must_be_string(value):
    with pytest.raises(ProviderError) as error:
        decode_response([record(done=True, response=value)], expected_model=MODEL)
    assert error.value.category == "invalid-response"


@pytest.mark.parametrize("tail", [b'{', b'{"x":', b'{"x":"unfinished',
                                  b'{"x":tru', b'{"x":1e+', b'{"x":1.',
                                  b'{"x":"\\u12', b'{"x":"\xf0\x9f'])
def test_unfinished_final_record_is_incomplete(tail):
    with pytest.raises(ProviderError) as error:
        decode_response([record(), tail], expected_model=MODEL)
    assert error.value.category == "incomplete-response"


@pytest.mark.parametrize("tail", [b'{broken}', b'{"x":nope}', b'{"x":"\\q"}',
                                  b'{"x":"\xff"}', b'{"x":1 "y":2}',
                                  b'{"x":1.2.', b'{"x":1e2e', b'{"x":"\\u1z',
                                  b'{"x":tru ', b'{"x":- '])
def test_malformed_final_record_is_invalid(tail):
    with pytest.raises(ProviderError) as error:
        decode_response([record(), tail], expected_model=MODEL)
    assert error.value.category == "invalid-response"


@pytest.mark.parametrize("prefix", [[], [record()], [record(done=True)]])
def test_source_failure_is_safe_and_never_replayed(prefix, capsys, caplog):
    attempts = []
    class Source:
        def __iter__(self):
            attempts.append("iteration")
            yield from prefix
            raise OSError("SYNTHETIC_SOURCE_ERROR_SENTINEL")
    with pytest.raises(ProviderError) as error:
        decode_response(Source(), expected_model=MODEL)
    assert attempts == ["iteration"]
    assert error.value.category == "provider-failure"
    assert str(error.value) == "Local model request failed."
    assert "SYNTHETIC_SOURCE_ERROR_SENTINEL" not in "".join(traceback.format_exception(error.value))
    assert error.value.__suppress_context__
    assert capsys.readouterr() == ("", "")
    assert caplog.records == []


def test_source_acquisition_failure_is_safe(capsys, caplog):
    class Source:
        def __iter__(self):
            raise OSError("SYNTHETIC_SOURCE_ERROR_SENTINEL")
    with pytest.raises(ProviderError) as error:
        decode_response(Source(), expected_model=MODEL)
    assert error.value.category == "provider-failure"
    assert "SYNTHETIC_SOURCE_ERROR_SENTINEL" not in "".join(traceback.format_exception(error.value))
    assert capsys.readouterr() == ("", "")
    assert caplog.records == []


@pytest.mark.parametrize("failure", [KeyboardInterrupt, SystemExit, RuntimeError])
def test_unexpected_or_control_exception_is_not_swallowed(failure):
    def source():
        yield record(done=True)
        raise failure()
    with pytest.raises(failure):
        decode_response(source(), expected_model=MODEL)


@pytest.mark.parametrize("updates,category", [({}, "length-limited"),
    ({"model": "other"}, "invalid-response"), ({"response": None}, "invalid-response"),
    ({"eval_count": True}, "invalid-response"), ({"eval_count": 65}, "limit-exceeded"),
    ({"error": None}, "provider-failure")])
def test_length_policy_respects_validation_precedence(updates, category):
    with pytest.raises(ProviderError) as error:
        decode_response([record(done=True, done_reason="length", **updates)], expected_model=MODEL)
    assert error.value.category == category


def test_failure_does_not_consume_more_source_or_close_caller_resource():
    events = []
    def source():
        yield record(error=None)
        events.append("advanced")
    with pytest.raises(ProviderError):
        decode_response(source(), expected_model=MODEL)
    assert events == []


def test_complete_stream_keeps_total_and_post_terminal_byte_limits():
    wire = padded_record(65536) * 3
    terminal = record(response="", done=True)
    # Pad with separate bounded blank records to reach the aggregate boundary.
    padding = 262144 - len(wire) - len(terminal)
    chunks = [wire, terminal, b"\n" * padding]
    assert decode_response(chunks, expected_model=MODEL) == "Hi" * 3
    with pytest.raises(ProviderError) as error:
        decode_response(chunks + [b"\n"], expected_model=MODEL)
    assert error.value.category == "limit-exceeded"


@pytest.mark.parametrize("fails", [False, True])
def test_caller_keeps_source_cleanup_ownership(fails):
    class Source:
        def __init__(self):
            self.records = iter([record(error=None)] if fails else [record(done=True)])
            self.closes = 0
        def __iter__(self):
            return self
        def __next__(self):
            return next(self.records)
        def close(self):
            self.closes += 1
    source = Source()
    try:
        if fails:
            with pytest.raises(ProviderError):
                decode_response(source, expected_model=MODEL)
        else:
            assert decode_response(source, expected_model=MODEL) == "Hi"
        assert source.closes == 0
    finally:
        source.close()
    assert source.closes == 1


def test_unknown_metadata_and_mixed_line_endings_preserve_text():
    wire = record(response="café", metadata={"safe": [1, 2]}).replace(b"\n", b"\r\n")
    wire += record(response="🙂", done=True)
    assert decode_response([wire], expected_model=MODEL) == "café🙂"


# Canonical contract stream; distinct variants remain individually collected.
ASSEMBLY_WIRE = record(response="Hel") + record(response="lo") + record(response="!", done=True)


@pytest.mark.parametrize("offset", range(1, len(ASSEMBLY_WIRE)), ids=lambda n: f"byte-{n}")
def test_contract_each_two_piece_split(offset):
    assert decode_response([ASSEMBLY_WIRE[:offset], ASSEMBLY_WIRE[offset:]], expected_model=MODEL) == "Hello!"


def test_contract_one_byte_chunks_with_interleaved_empty_chunks():
    chunks = [b""]
    for value in ASSEMBLY_WIRE:
        chunks.extend([bytes([value]), b""])
    assert decode_response(chunks, expected_model=MODEL) == "Hello!"


@pytest.mark.parametrize("chunks", [
    [record(response="Hel"), record(response="lo"), record(response="!", done=True)],
    [ASSEMBLY_WIRE],
], ids=["separate-records", "coalesced-records"])
def test_contract_ordered_ascii_assembly(chunks):
    assert decode_response(chunks, expected_model=MODEL) == "Hello!"


UNICODE_WIRE = record(response="café🙂") + terminal_without_text()
UNICODE_SPLITS = [index for index, byte in enumerate(UNICODE_WIRE) if byte & 0xc0 == 0x80]


@pytest.mark.parametrize("offset", UNICODE_SPLITS, ids=lambda n: f"unicode-byte-{n}")
def test_contract_each_multibyte_split(offset):
    assert decode_response([UNICODE_WIRE[:offset], UNICODE_WIRE[offset:]], expected_model=MODEL) == "café🙂"


@pytest.mark.parametrize("endings", [(b"\n",)*3, (b"\r\n",)*3, (b"\r\n", b"\n", b"\r\n")],
                         ids=["lf", "crlf", "mixed"])
def test_contract_record_endings_with_split_crlf(endings):
    records = [record(response="Hel"), record(response="lo"), record(response="!", done=True)]
    wire = b"".join(value[:-1] + ending for value, ending in zip(records, endings))
    split = wire.find(b"\r\n") + 1 if b"\r\n" in wire else len(records[0])
    assert decode_response([wire[:split], wire[split:]], expected_model=MODEL) == "Hello!"


def test_contract_blank_records_before_between_and_after_text():
    assert decode_response([b" \t\r\n", record(), b"\t\n", terminal_without_text(), b" \n"], expected_model=MODEL) == "Hi"


@pytest.mark.parametrize("field", ["model", "response"])
def test_contract_duplicate_identity_and_text_keys(field):
    # Keep identity valid: last-key-wins must not be rejected for a wrong model.
    value = MODEL if field == "model" else "other"
    wire = record(done=True)[:-2] + b',"' + field.encode() + b'":' + json.dumps(value).encode() + b'}\n'
    with pytest.raises(ProviderError) as error:
        decode_response([wire], expected_model=MODEL)
    assert error.value.category == "invalid-response"


@pytest.mark.parametrize("tail", [
    record(done=True).rstrip(b"\n") + b" t",
    b'{"x":1 t',
], ids=["extra-data-literal-prefix", "missing-comma-literal-prefix"])
def test_literal_prefix_does_not_hide_earlier_json_syntax_error(tail):
    with pytest.raises(ProviderError) as error:
        decode_response([tail], expected_model=MODEL)
    assert error.value.category == "invalid-response"


@pytest.mark.parametrize("wire", [b"[]\n", b'"text"\n', b"null\n", b"true\n", b"5\n"],
                         ids=["array", "string", "null", "boolean", "number"])
def test_contract_top_level_shapes(wire):
    with pytest.raises(ProviderError) as error:
        decode_response([wire], expected_model=MODEL)
    assert error.value.category == "invalid-response"


@pytest.mark.parametrize("wire,category", [
    (b'{"response":broken}\n', "invalid-response"),
    (b'{"model":"qwen3:0.6b","response":"\xff","done":false}\n' + terminal_without_text(), "invalid-response"),
    (b'{"response":"\xf0\x9f', "incomplete-response"),
], ids=["malformed-line", "invalid-utf8-line", "truncated-utf8-tail"])
def test_contract_corruption_after_partial_text(wire, category):
    with pytest.raises(ProviderError) as error:
        decode_response([record(), wire], expected_model=MODEL)
    assert error.value.category == category


@pytest.mark.parametrize("chunks,category", [
    ([record(), record()], "incomplete-response"),
    ([record(), record(done=True, model="other")], "invalid-response"),
    ([record(response={})], "invalid-response"),
], ids=["multiple-text-no-terminal", "terminal-model-change", "object-response"])
def test_contract_additional_state_and_schema_boundaries(chunks, category):
    with pytest.raises(ProviderError) as error:
        decode_response(chunks, expected_model=MODEL)
    assert error.value.category == category


@pytest.mark.parametrize("terminal", [terminal_without_text(), record(response="", done=True)])
def test_contract_empty_fragment_before_real_answer(terminal):
    assert decode_response([record(response=""), record(), terminal], expected_model=MODEL) == "Hi"


@pytest.mark.parametrize("prefix", [[], [record()]])
def test_contract_bare_error_object(prefix):
    with pytest.raises(ProviderError) as error:
        decode_response(prefix + [b'{"error":"SYNTHETIC_PROVIDER_ERROR_SENTINEL"}\n'], expected_model=MODEL)
    assert error.value.category == "provider-failure"


@pytest.mark.parametrize("size", [65536, 65537], ids=["exact", "over"])
@pytest.mark.parametrize("padding_character", ["x", "é"], ids=["ascii", "utf8"])
def test_contract_complete_stream_record_byte_boundary(size, padding_character):
    wire = padded_record(size, padding_character=padding_character)
    assert len(wire) == size
    if padding_character == "é":
        assert len(wire.decode()) < 65536
    if size == 65536:
        assert decode_response([wire, terminal_without_text()], expected_model=MODEL) == "Hi"
    else:
        with pytest.raises(ProviderError) as error:
            decode_response([wire, terminal_without_text()], expected_model=MODEL)
        assert error.value.category == "limit-exceeded"


def test_contract_small_chunks_enforce_unfinished_buffer_cap_immediately():
    decoder = LocalProviderDecoder(MODEL)
    for _ in range(64):
        decoder.feed(b"x" * 1024)
    with pytest.raises(ProviderError) as error:
        decoder.feed(b"x")
    assert error.value.category == "limit-exceeded"
    assert len(decoder.buffer) == 65536


@pytest.mark.parametrize("extra", [b"", b"\n"], ids=["exact", "over"])
@pytest.mark.parametrize("padding_character", ["x", "é"], ids=["ascii", "utf8"])
def test_contract_total_cap_counts_ignored_metadata_bytes(extra, padding_character):
    chunks = [padded_record(65536, padding_character=padding_character)] * 3
    chunks += [padded_record(65536, done=True, padding_character=padding_character)]
    assert sum(map(len, chunks)) == 262144
    if extra:
        with pytest.raises(ProviderError) as error:
            decode_response(chunks + [extra], expected_model=MODEL)
        assert error.value.category == "limit-exceeded"
    else:
        assert decode_response(chunks, expected_model=MODEL) == "Hi" * 4


def test_contract_blank_only_flood_cannot_bypass_aggregate_limit():
    with pytest.raises(ProviderError) as error:
        decode_response([b"\n" * 65536] * 4 + [b"\n"], expected_model=MODEL)
    assert error.value.category == "limit-exceeded"


@pytest.mark.parametrize("count,category", [(64, None), (65, "limit-exceeded"),
    (-1, "invalid-response"), (True, "invalid-response"), ("64", "invalid-response")])
def test_contract_terminal_token_metadata(count, category):
    chunks = [record(), record(response="", done=True, eval_count=count)]
    if category is None:
        assert decode_response(chunks, expected_model=MODEL) == "Hi"
    else:
        with pytest.raises(ProviderError) as error:
            decode_response(chunks, expected_model=MODEL)
        assert error.value.category == category


@pytest.mark.parametrize("wire,category", [
    (b'{"error":"SYNTHETIC_PRIVATE_INPUT_SENTINEL"}\n', "provider-failure"),
    (b'{"SYNTHETIC_PRIVATE_INPUT_SENTINEL":broken}\n', "invalid-response"),
    (b'{"response":"SYNTHETIC_PRIVATE_INPUT_SENTINEL\xff"}\n', "invalid-response"),
], ids=["provider", "json", "utf8"])
def test_contract_private_markers_absent_from_all_public_diagnostics(wire, category, capsys, caplog):
    with pytest.raises(ProviderError) as error:
        decode_response([wire], expected_model=MODEL)
    assert error.value.category == category
    assert "SYNTHETIC_PRIVATE_INPUT_SENTINEL" not in "".join(traceback.format_exception(error.value))
    assert capsys.readouterr() == ("", "")
    assert caplog.records == []


@pytest.mark.parametrize("outcome", ["success", "provider-failure", "invalid-response"])
def test_contract_decoder_has_zero_external_side_effects(outcome, monkeypatch):
    import http.client
    import os
    import socket
    import subprocess
    import urllib.request
    calls = []
    def forbidden(*args, **kwargs):
        calls.append("external call")
        raise AssertionError("Decoder attempted an external operation")
    with monkeypatch.context() as patches:
        for target, name in [(socket, "socket"), (socket, "create_connection"),
            (http.client.HTTPConnection, "connect"), (urllib.request, "urlopen"),
            (subprocess, "Popen"), (os, "system"), (os, "kill"), (os, "killpg")]:
            patches.setattr(target, name, forbidden)
        if outcome != "success":
            with pytest.raises(ProviderError) as error:
                wire = record(error=None) if outcome == "provider-failure" else b'{broken}\n'
                decode_response([wire], expected_model=MODEL)
            assert error.value.category == outcome
        else:
            assert decode_response([record(done=True)], expected_model=MODEL) == "Hi"
    assert calls == []


@pytest.mark.parametrize("wire", [b'{"x":false "y":1e', b'{"x":1 "y":2.', b'[true 1e', b'{"x":false 2.', b'[01e', b'[1.e'],
                         ids=["missing-comma-before-exponent", "missing-comma-before-decimal",
                              "missing-comma-before-number-exponent", "missing-comma-before-number-decimal",
                              "leading-zero-before-exponent", "decimal-without-digits-before-exponent"])
def test_number_suffix_does_not_hide_earlier_json_syntax_error(wire):
    with pytest.raises(ProviderError) as error:
        decode_response([wire], expected_model=MODEL)
    assert error.value.category == "invalid-response"
