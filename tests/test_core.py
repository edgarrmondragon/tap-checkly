"""Tests standard tap features using the built-in SDK tests library."""

from __future__ import annotations

from typing import Any

from singer_sdk.testing import get_standard_tap_tests

from tap_checkly.tap import TapCheckly

SAMPLE_CONFIG: dict[str, Any] = {}


def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(TapCheckly, config=SAMPLE_CONFIG)
    for test in tests:
        test()
