import pytest
from src.utils.secure_input import sanitize_input


def test_sanitize_input_removes_special_characters():
    assert sanitize_input("import os.rmdir") == "import osrmdir"
    assert sanitize_input("Hello, World!") == "Hello World!"
    assert sanitize_input("123$%^456") == "123456"


def test_sanitize_input_keeps_alphanumeric_and_spaces():
    assert sanitize_input("Hello World 123") == "Hello World 123"
    assert sanitize_input("Python3 is great") == "Python3 is great"
    assert sanitize_input("Emoji 😊 Test") == "Emoji  Test"  # Removing emoji
    assert sanitize_input("中文字符测试") == ""  # Removing non-ASCII characters


def test_sanitize_input_empty_string():
    assert sanitize_input("") == ""


def test_sanitize_input_only_special_characters():
    assert sanitize_input("@#$%^&*()") == ""


def test_sanitize_input_sql_injection():
    malicious_input = "'; DROP TABLE users; --"
    sanitized_input = sanitize_input(malicious_input)
    assert sanitized_input == " DROP TABLE users "


def test_sanitize_input_allow_exclamation():
    assert sanitize_input("!help") == "!help"


if __name__ == "__main__":
    pytest.main()
