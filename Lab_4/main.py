import json
from collections import defaultdict, deque


def load_edges(file_path="metro.json"):
	with open(file_path, encoding="utf-8") as file:
		return json.load(file)


def normalize_station_name(station_name):
	return station_name.strip().lower().title()


def build_graph(edge_list):
	graph = defaultdict(list)
	for station_a, station_b in edge_list:
		station_a = normalize_station_name(station_a)
		station_b = normalize_station_name(station_b)
		graph[station_a].append(station_b)
		graph[station_b].append(station_a)
	return graph


graph = build_graph(load_edges())


def bfs(start, end):
	queue = deque([[start]])
	visited = {start}

	while queue:
		path = queue.popleft()
		station = path[-1]

		if station == end:
			return path

		for neighbor in graph.get(station, []):
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append(path + [neighbor])

	return None


def dfs(start, end, visited=None):
	if visited is None:
		visited = set()

	visited.add(start)
	if start == end:
		return [start]

	for neighbor in graph.get(start, []):
		if neighbor not in visited:
			path = dfs(neighbor, end, visited)
			if path is not None:
				return [start] + path

	return None


def demo():
    # 1. BFS CHECK
    path = bfs("Спасская", "Пушкинская")
    assert path, "BFS ERR: Путь пуст"
    assert path[0] == "Спасская" and path[-1] == "Пушкинская", "BFS ERR: Начальная и конечная станция неверны"
    assert len(path) == 4, "BFS ERR: Путь не кратчайший"
    for a, b in zip(path, path[1:]):
        assert b in graph[a]

    # 2. DFS CHECK
    path = dfs("Спасская", "Пушкинская")
    assert path, "DFS ERR: Путь пуст"
    assert path[0] == "Спасская" and path[-1] == "Пушкинская", "DFS ERR: Начальная и конечная станция неверны"
    assert len(path) == len(set(path)), "DFS ERR: В пути есть петли"
    for a, b in zip(path, path[1:]):
        assert b in graph[a]
    print("Проверка пройдена")


if __name__ == "__main__":
	demo()
	start = input("Откуда: ")
	end = input("Куда: ")
	start = normalize_station_name(start)
	end = normalize_station_name(end)
	path = bfs(start, end)

	if path is None:
		print("Станции не связаны")
	else:
		print(f"Выход: {' -> '.join(path)}")
