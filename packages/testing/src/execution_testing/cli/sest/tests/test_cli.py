"""Tests for the `sest` CLI group."""

import io
import sys

import pytest
from click.testing import CliRunner

from ..cli import ensure_utf8_output, sest

pytestmark = pytest.mark.skip(
    "Issue #3241: sest info queries github.com to get release information"
)


def test_info_runs_successfully() -> None:
    """`sest info` exits cleanly and reports the SEST banner."""
    result = CliRunner().invoke(sest, ["info"])
    assert result.exit_code == 0
    assert "SEST" in result.output


def test_info_survives_legacy_console_encoding(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    `sest info` must not crash on a non-UTF-8 console code page.

    Regression test for the Windows `cp1252` console, whose codec
    cannot encode the box-drawing characters printed by the command.
    """
    stream = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
    monkeypatch.setattr(sys, "stdout", stream)

    # Without the UTF-8 reconfiguration this raises UnicodeEncodeError.
    sest.main(["info"], standalone_mode=False)

    stream.flush()
    assert "SEST" in stream.buffer.getvalue().decode("utf-8")


def test_ensure_utf8_output_reconfigures_stream(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`ensure_utf8_output` switches a legacy stream to UTF-8."""
    stream = io.TextIOWrapper(io.BytesIO(), encoding="cp1252")
    monkeypatch.setattr(sys, "stdout", stream)

    ensure_utf8_output()

    assert stream.encoding.lower() == "utf-8"
