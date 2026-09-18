import random
import time
from typing import TypedDict


class Item(TypedDict):
    id: int
    name: str


class Request(TypedDict):
    ip: str
    status: int


ATTACKER_IP = "13.13.13.13"
STATUS_MIN = 100
STATUS_MAX = 599


def generate_products(n: int) -> list[Item]:
    if n < 0:
        raise ValueError("Количество товаров не может быть отрицательным")

    identifiers = list(range(1, n + 1))
    random.shuffle(identifiers)
    return [{"id": item_id, "name": f"Товар_{item_id}"} for item_id in identifiers]


def bubble_sort(arr: list[Item]) -> list[Item]:
    result = arr.copy()

    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if result[index]["id"] > result[index + 1]["id"]:
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        if not swapped:
            break

    return result


def insertion_sort(arr: list[Item]) -> list[Item]:
    result = arr.copy()

    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0 and result[position]["id"] > current["id"]:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current

    return result


def quick_sort(arr: list[Item]) -> list[Item]:
    result = arr.copy()

    def sort_range(left: int, right: int) -> None:
        if left >= right:
            return

        pivot = result[random.randint(left, right)]["id"]
        i, j = left, right
        while i <= j:
            while result[i]["id"] < pivot:
                i += 1
            while result[j]["id"] > pivot:
                j -= 1
            if i <= j:
                result[i], result[j] = result[j], result[i]
                i += 1
                j -= 1

        sort_range(left, j)
        sort_range(i, right)

    if result:
        sort_range(0, len(result) - 1)
    return result


def _random_ipv4() -> str:
    octets = [random.randint(0, 255) for _ in range(4)]
    return ".".join(str(octet) for octet in octets)


def generate_requests(n: int) -> list[Request]:
    if n < 0:
        raise ValueError("Количество запросов не может быть отрицательным")

    statuses = [200, 200, 200, 301, 404, 404, 500, 502]
    attacker_count = n // 10
    requests = []

    for _ in range(n - attacker_count):
        requests.append({"ip": _random_ipv4(), "status": random.choice(statuses)})
    for _ in range(attacker_count):
        requests.append({"ip": ATTACKER_IP, "status": random.choice(statuses)})

    random.shuffle(requests)
    return requests


def counting_sort_by_status(requests: list[Request]) -> list[Request]:
    buckets = [[] for _ in range(STATUS_MAX - STATUS_MIN + 1)]

    for request in requests:
        status = request["status"]
        if not STATUS_MIN <= status <= STATUS_MAX:
            raise ValueError(f"HTTP-статус должен быть в диапазоне 100..599: {status}")
        buckets[status - STATUS_MIN].append(request)

    result = []
    for bucket in buckets:
        result.extend(bucket)
    return result


def _ip_to_int(ip: str) -> int:
    octets = ip.split(".")
    if len(octets) != 4:
        raise ValueError(f"Некорректный IPv4-адрес: {ip}")

    number = 0
    for octet in octets:
        if not octet.isdigit():
            raise ValueError(f"Октет IPv4 должен быть целым числом: {ip}")
        value = int(octet)
        if not 0 <= value <= 255:
            raise ValueError(f"Октет IPv4 должен быть в диапазоне 0..255: {ip}")
        number = number * 256 + value
    return number


def radix_sort_by_ip(requests: list[Request]) -> list[Request]:
    current = [(_ip_to_int(request["ip"]), request) for request in requests]

    for shift in (0, 8, 16, 24):
        buckets = [[] for _ in range(256)]
        for ip_number, request in current:
            digit = (ip_number >> shift) & 0xFF
            buckets[digit].append((ip_number, request))

        current = []
        for bucket in buckets:
            current.extend(bucket)

    return [request for _, request in current]


def _count_values(values) -> dict:
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts


def _print_results(
    title: str,
    first_column: str,
    second_column: str,
    results: dict[str, tuple[float, int]],
) -> None:
    print(f"\n{title}:")
    print(f"{first_column:<25} {second_column:>9}       Время, с")
    print("-" * 58)
    for name, (elapsed, amount) in results.items():
        print(f"{name:<25} {amount:>9} {elapsed:>16.6f}")


def _measure_sort(sort_function, data: list) -> tuple[float, int]:
    started = time.perf_counter()
    sort_function(data)
    return time.perf_counter() - started, len(data)


def _benchmark_products(product_count: int, slow_sample_size: int) -> None:
    print(f"\nГенерация {product_count} товаров...")
    products = generate_products(product_count)
    slow_sample = products[:slow_sample_size]

    product_results = {
        "Пузырьковая (выборка)": _measure_sort(bubble_sort, slow_sample),
        "Вставками (выборка)": _measure_sort(insertion_sort, slow_sample),
        "Быстрая": _measure_sort(quick_sort, products),
    }
    _print_results("Производительность сортировок товаров", "Алгоритм", "Элементов", product_results)
    print(f"Пузырьковая сортировка и сортировка вставками выполнены на выборке из {slow_sample_size} товаров.")


def _print_status_statistics(requests: list[Request]) -> None:
    status_counts = _count_values(request["status"] for request in requests)
    print("\nСтатистика HTTP-статусов:")
    for status in range(STATUS_MIN, STATUS_MAX + 1):
        if status in status_counts:
            print(f"{status}: {status_counts[status]}")


def _print_suspicious_ips(requests: list[Request], threshold: int) -> None:
    ip_counts = _count_values(request["ip"] for request in requests)
    suspects = {
        ip: count for ip, count in ip_counts.items() if count > threshold
    }
    print(f"\nПодозрительные IP (> {threshold} запросов) — возможная подозрительная активность:")
    for ip, count in suspects.items():
        print(f"{ip}: {count}")


def _benchmark_requests(request_count: int, suspicious_threshold: int) -> None:
    print(f"\nГенерация {request_count} HTTP-запросов...")
    requests = generate_requests(request_count)
    if len(requests) != request_count:
        raise RuntimeError("Количество сгенерированных запросов не совпадает с запрошенным")

    request_results = {
        "Counting Sort по статусу": _measure_sort(counting_sort_by_status, requests),
        "Radix Sort по IP": _measure_sort(radix_sort_by_ip, requests),
    }
    _print_results("Производительность сортировок HTTP-запросов", "Метод", "Запросов", request_results)

    _print_status_statistics(requests)
    _print_suspicious_ips(requests, suspicious_threshold)


def main() -> None:
    _benchmark_products(product_count=1000000, slow_sample_size=5000)
    _benchmark_requests(request_count=10000, suspicious_threshold=100)


if __name__ == "__main__":
    main()
