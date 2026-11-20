import pytest

from main import (
    ACTIVITIES,
    CABLES,
    ITEMS,
    MAX_WEIGHT,
    greedy_knapsack,
    min_connection_cost,
    select_activities,
)


@pytest.mark.parametrize(
    ("activities", "expected"),
    [
        ([], []),
        ([(1, 2), (2, 3), (3, 4)], [(1, 2), (2, 3), (3, 4)]),
        ([(1, 3), (2, 4), (4, 5)], [(1, 3), (4, 5)]),
    ],
)
def test_select_activities(
    activities: list[tuple[int, int]],
    expected: list[tuple[int, int]],
) -> None:
    assert select_activities(activities) == expected


@pytest.mark.parametrize(
    ("items", "capacity", "expected"),
    [
        ([], 10, 0),
        ([(60, 10), (100, 20), (120, 30)], 50, 160),
        ([(10, 5)], 2, 0),
        ([(10, 5)], 0, 0),
        ([(10, 5)], 5, 10),
    ],
)
def test_greedy_knapsack(
    items: list[tuple[int, int]],
    capacity: int,
    expected: int,
) -> None:
    assert greedy_knapsack(items, capacity) == expected


@pytest.mark.parametrize(
    ("cables", "expected"),
    [
        ([], 0),
        ([5], 0),
        ([4, 3, 2, 6], 29),
        ([1, 2, 3, 4], 19),
    ],
)
def test_min_connection_cost(cables: list[int], expected: int) -> None:
    assert min_connection_cost(cables) == expected

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))