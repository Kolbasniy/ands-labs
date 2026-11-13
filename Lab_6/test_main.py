import pytest

from main import SolutionA, SolutionB, SolutionC, build_tree


def test_build_tree() -> None:
    assert build_tree([1, 2, 3, None, 4]) == build_tree([1, 2, 3, None, 4])
    assert build_tree([1, 2, 3, None, 4]) != build_tree([1, 2, 3, 4, None])
    assert build_tree([]) is None


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1, 2, 2, 3, 4, 4, 3], True),
        ([1, 2, 2, None, 3, None, 3], False),
        ([], True),
    ],
)
def test_is_symmetric(values: list[int | None], expected: bool) -> None:
    assert SolutionA().is_symmetric(build_tree(values)) is expected


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([1, 2, 3, 4, 5], 3),
        ([1, 2], 1),
        ([], 0),
    ],
)
def test_diameter_of_binary_tree(values: list[int | None], expected: int) -> None:
    assert SolutionB().diameter_of_binary_tree(build_tree(values)) == expected


@pytest.mark.parametrize(
    ("values", "x", "y", "expected"),
    [
        ([1, 2, 3, 4], 4, 3, False),
        ([1, 2, 3, None, 4, None, 5], 5, 4, True),
        ([1, 2, 3], 2, 2, False)
    ],
)
def test_is_cousins(
    values: list[int | None],
    x: int,
    y: int,
    expected: bool,
) -> None:
    assert SolutionC().is_cousins(build_tree(values), x, y) is expected


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
