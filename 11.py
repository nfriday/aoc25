from collections import deque

def build_graph(lines):
    graph = {}
    for line in lines:
        nodes = line.split(" ")
        graph[nodes[0].strip(":")] = set(nodes[1:])
        graph["out"] = set()
    return graph

def count_paths(graph, start, end):

    # count incoming edges
    indegree = {node:0 for node in graph}
    for node in graph:
        for neighbour in graph[node]:
            indegree[neighbour] = indegree.get(neighbour, 0) + 1

    # topological sort
    topological_order = []
    queue = deque()
    for node, degree in indegree.items():
        if degree == 0:
            queue.append(node)

    while queue:
        node = queue.popleft()
        topological_order.append(node)
        for neighbour in graph[node]:
            indegree[neighbour] -= 1
            if indegree[neighbour] == 0:
                queue.append(neighbour)

    # traverse in topological order to count ways
    ways = {node:0 for node in graph}
    ways[start] = 1
    for node in topological_order:
        for neighbour in graph[node]:
            ways[neighbour] += ways[node]

    return ways[end]

with open("11.txt", "r") as file:
    lines = file.read().splitlines()

graph = build_graph(lines)

# part 1
print(count_paths(graph,"you","out"))

# part 1
svr_fft_dac_out = count_paths(graph,"svr","fft") * count_paths(graph,"fft","dac") * count_paths(graph,"dac","out")
svr_dac_fft_out = count_paths(graph,"svr","dac") * count_paths(graph,"dac","fft") * count_paths(graph,"fft","out")
print(svr_fft_dac_out + svr_dac_fft_out)
