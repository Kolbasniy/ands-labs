import heapq
from collections.abc import Sequence


ACTIVITIES = [
    (1, 4),
    (3, 5),
    (0, 6),
    (5, 7),
    (3, 8),
    (5, 9),
    (6, 10),
    (8, 11),
    (8, 12),
    (2, 13),
    (12, 14),
]
ITEMS = [(60, 10), (100, 20), (120, 30)]
MAX_WEIGHT = 50
CABLES = [4, 3, 2, 6]


def select_activities(activities: Sequence[tuple[int, int]]) -> list[tuple[int, int]]:
    sorted_activities = sorted(
        activities,
        key=lambda activity: activity[1],
    )

    selected_activities: list[tuple[int, int]] = []
    last_end_time = 0

    for start, end in sorted_activities:
        if start >= last_end_time:
            selected_activities.append((start, end))
            last_end_time = end

    return selected_activities


def greedy_knapsack(items: Sequence[tuple[int, int]], capacity: int) -> int:
    sorted_items = sorted(
        items,
        key=lambda item: item[0] / item[1],
        reverse=True,
    )

    total_value = 0
    remaining_capacity = capacity

    for value, weight in sorted_items:
        if remaining_capacity == 0:
            break

        if weight <= remaining_capacity:
            total_value += value
            remaining_capacity -= weight

    return total_value


def min_connection_cost(cables: Sequence[int]) -> int:
    if len(cables) <= 1:
        return 0

    cable_heap = list(cables)
    heapq.heapify(cable_heap)

    total_cost = 0

    while len(cable_heap) > 1:
        shortest_length = heapq.heappop(cable_heap)
        second_shortest_length = heapq.heappop(cable_heap)

        merged_length = shortest_length + second_shortest_length
        total_cost += merged_length

        heapq.heappush(cable_heap, merged_length)

    return total_cost


if __name__ == "__main__":
    chosen_activities = select_activities(ACTIVITIES)
    print("Задача A:")
    print(
        f"Выбранные активности ({len(chosen_activities)} шт.): "
        f"{chosen_activities}\n"
    )

    max_value = greedy_knapsack(ITEMS, MAX_WEIGHT)
    print("Задача B:")
    print(f"Максимальная стоимость в рюкзаке: {max_value}\n")

    cost = min_connection_cost(CABLES)
    print("Задача C:")
    print(f"Минимальная стоимость соединения: {cost}")