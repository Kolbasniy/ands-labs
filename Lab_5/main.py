import json, heapq
from collections import defaultdict


def load_edges(file_path="metro.json"):
	with open(file_path, encoding="utf-8") as file:
		return json.load(file)


def normalize_station_name(station_name):
	return station_name.strip().lower().title()


def build_graph(edge_list):
	graph = defaultdict(list)
	for station_a, station_b, weight in edge_list:
		station_a = normalize_station_name(station_a)
		station_b = normalize_station_name(station_b)
		graph[station_a].append((station_b, weight))
		graph[station_b].append((station_a, weight))
	return graph


graph = build_graph(load_edges())


def dijkstra(start, end):
	queue = [(0, [start])]
	visited = set()
	while queue:
		time, path = heapq.heappop(queue)
		node = path[-1]
		if node == end:
			return time, path
		if node in visited:
			continue
		visited.add(node)
		for neighbor, w in graph[node]:
			if neighbor not in visited:
				heapq.heappush(queue, (time + w, path + [neighbor]))
	return None


def demo():
	assert dijkstra("Спасская", "Пушкинская") == (
		6,
		["Спасская", "Достоевская", "Владимирская", "Пушкинская"],
	)
	assert dijkstra("Садовая", "Садовая") == (0, ["Садовая"])
	print("Проверка пройдена")


if __name__ == "__main__":
	demo()
	start = normalize_station_name(input("Откуда: "))
	end = normalize_station_name(input("Куда: "))
	result = dijkstra(start, end) if start in graph and end in graph else None
	if result:
		time, path = result
		print(f"Выход: {' -> '.join(path)} ({time} мин)")
	else:
		print("Станции не связаны")