#!/usr/bin/env python3
"""Test should_render() helper function for optional fields handling."""

import sys
from pathlib import Path

# Setup path to common.py
LOADERS_DIR = Path(__file__).resolve().parent / "loaders"
sys.path.insert(0, str(LOADERS_DIR))

from common import should_render

def test_should_render():
    """Test the should_render() validation function."""
    
    print("Testing should_render() helper function...")
    print("-" * 50)
    
    tests = [
        # (value, expected_result, description)
        (None, False, "None should not render"),
        ("", False, "Empty string should not render"),
        ("  ", False, "Whitespace-only string should not render"),
        ("text", True, "Non-empty string should render"),
        ("Δ Transform", True, "Non-empty string with special chars should render"),
        ([], False, "Empty list should not render"),
        ([1], True, "Non-empty list should render"),
        ({}, False, "Empty dict should not render"),
        ({"key": "value"}, True, "Non-empty dict should render"),
        (0, True, "Zero should render (it's a valid value)"),
        (False, True, "False should render (it's a valid value)"),
    ]
    
    passed = 0
    failed = 0
    
    for value, expected, description in tests:
        result = should_render(value)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result == expected:
            passed += 1
        else:
            failed += 1
        print(f"{status}: {description}")
        print(f"       Input: {repr(value)}")
        print(f"       Expected: {expected}, Got: {result}")
        print()
    
    print("-" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    return failed == 0

if __name__ == "__main__":
    success = test_should_render()
    sys.exit(0 if success else 1)
