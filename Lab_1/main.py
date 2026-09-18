import random
import time

CATALOG_SIZE = 1000000
ID_FIELD = "id"


def create_products(total):
    return [{ID_FIELD: idx, "name": f"Товар_{idx}"} for idx in range(1, total + 1)]


def search_from_start(data, wanted_id):
    index = 0
    data_length = len(data)
    while index < data_length:
        if data[index][ID_FIELD] == wanted_id:
            return index
        index += 1
    return -1


def search_with_binary_bounds(data, wanted_id, left, right):
    while left <= right:
        pivot = (left + right) // 2
        current = data[pivot][ID_FIELD]
        if current == wanted_id:
            return pivot
        if current < wanted_id:
            left = pivot + 1
        else:
            right = pivot - 1
    return -1


def search_exponentially(data, wanted_id):
    count = len(data)
    if count == 0:
        return -1

    if data[0][ID_FIELD] == wanted_id:
        return 0

    border = 1
    while border < count and data[border][ID_FIELD] <= wanted_id:
        border *= 2

    start = border // 2
    end = min(border, count - 1)
    return search_with_binary_bounds(data, wanted_id, start, end)


def search_binarily(data, wanted_id):
    return search_with_binary_bounds(data, wanted_id, 0, len(data) - 1)


def search_by_interpolation(data, wanted_id):
    left = 0
    right = len(data) - 1

    while left <= right and data[left][ID_FIELD] <= wanted_id <= data[right][ID_FIELD]:
        if left == right:
            return left if data[left][ID_FIELD] == wanted_id else -1

        distance = data[right][ID_FIELD] - data[left][ID_FIELD]
        probe = left + int((float(right - left) / distance) * (wanted_id - data[left][ID_FIELD]))

        probe_id = data[probe][ID_FIELD]
        if probe_id == wanted_id:
            return probe
        if probe_id < wanted_id:
            left = probe + 1
        else:
            right = probe - 1

    return -1


def measure(func, data, wanted_id):
    started_at = time.perf_counter()
    func(data, wanted_id)
    return time.perf_counter() - started_at


product_list = create_products(CATALOG_SIZE)
print(f"Сгенерировано {CATALOG_SIZE} товаров.")

cases = {
    "В начале": 1,
    "В середине": CATALOG_SIZE // 2,
    "В конце": CATALOG_SIZE,
    "Случайный": random.randint(1, CATALOG_SIZE),
    "Отсутствует": CATALOG_SIZE + 1,
}

methods = {
    "Линейный": search_from_start,
    "Экспоненц-й": search_exponentially,
    "Бинарный": search_binarily,
    "Интерполяц-й": search_by_interpolation,
}

bench = {}
for method_title, method_impl in methods.items():
    timings = {}
    for case_title, target in cases.items():
        timings[case_title] = measure(method_impl, product_list, target)
    bench[method_title] = timings

print("\n" + "=" * 83)
print(f"{'Алгоритм':<13} | {'В начале':<11} | {'В середине':<11} | {'В конце':<11} | {'Случайный':<11} | {'Отсутствует':<11}")
print("-" * 83)

for method_title, method_times in bench.items():
    formatted = [f"{method_times[case_title]:.6f}s".ljust(11) for case_title in cases]
    print(f"{method_title:<13} | " + " | ".join(formatted))

print("=" * 83)