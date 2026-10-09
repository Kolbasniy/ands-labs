import pytest

from pathlib import Path
from tasks import first_unique, is_anagram, is_subset, longest_palindrome


@pytest.mark.parametrize(
	("small", "big", "expected"),
	[
		(["b", "d", "f"], ["a", "b", "c", "d", "e", "f"], True),
		(["b", "d", "f", "h"], ["a", "b", "c", "d", "e", "f"], False),
	],
)
def test_is_subset(small, big, expected):
	assert is_subset(small, big) is expected


@pytest.mark.parametrize(
	("value", "expected"),
	[
		("minimum", "n"),
		("aabbcc", None),
	],
)
def test_first_unique(value, expected):
	assert first_unique(value) == expected


@pytest.mark.parametrize(
	("value", "expected"),
	[
		("abccccdd", 7),
		("a", 1),
		("aAbBABba", 8),
		("abcdefghijklmnoPQrstuvwxyz", 1),
		("wasitacaroracatisaw", 19),
		("bbbabab", 7),
		("abcdeedcba", 10),
		("looooooongestpalindrOme", 13),
		("abcdeedcbaxyz", 11),
		(Path("test_data.txt").read_text(encoding="utf-8"), 1122),
	],
)
def test_longest_palindrome(value, expected):
	assert longest_palindrome(value) == expected


@pytest.mark.parametrize(
	("value", "other", "expected"),
	[
		("нора", "рано", True),
		("монета", "отмена", True),
		("мышка", "камыш", True),
		("тормони", "монитор", True),
		("тоемони", "монитор", False),
	],
)
def test_is_anagram(value, other, expected):
	assert is_anagram(value, other) is expected
