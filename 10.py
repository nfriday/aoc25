from heapq import heappush, heappop
import re
import numpy
from scipy.optimize import milp, LinearConstraint, Bounds

class Machine:
    def __init__(self, target_lights, moves):
        self.target = sum(2**i for i in target_lights)
        self.moves = [sum(2**i for i in move) for move in moves]
        self.graph = {}
        self.start = 0
        self.build_graph()

    def connection(self, position, move):
        return position ^ move

    def get_connections(self, position):
        return [self.connection(position,move) for move in self.moves]

    def build_graph(self,start=0):
        queue = [self.start]
        seen = set()
        while queue:
            position = queue.pop()
            seen.add(position)
            self.graph[position] = {}
            for connection in self.get_connections(position):
                self.graph[position][connection] = 1
                if connection not in seen:
                    queue.append(connection)

    def dijkstra(self):
        start=self.start
        distances = {position: 9999 for position in self.graph}
        distances[start] = 0
        queue = [(0,start)]
        while queue:
            distance, current = heappop(queue)
            if current == self.target:
                break
            if distance > distances[current]:
                continue
            for neighbour, weight in self.graph[current].items():
                new_distance = distance + weight
                if new_distance < distances[neighbour]:
                    distances[neighbour] = new_distance
                    heappush(queue, (new_distance, neighbour))
        return distances[self.target]

with open("10.txt", "r") as file:
    lines = file.read().splitlines()

def parse(line):
    match = re.match(r'\[(.+)\] (.*) \{', line)
    target_lights = [i for i,v in enumerate(match.group(1)) if v =='#']
    moves = [ list(map(int,i.strip("()").split(","))) for i in match.group(2).split()]
    return target_lights, moves

print(sum(Machine(*parse(line)).dijkstra() for line in lines))

# part 2

def parse2(line):
    match = re.match(r'\[.+\] (.*) \{(.*)\}', line)
    target_joltages = list(map(int,match.group(2).split(",")))
    moves = [ list(map(int,i.strip("()").split(","))) for i in match.group(1).split()]
    return target_joltages, moves

def solve(target,moves):
    matrix = numpy.array([
        [ 1 if i in move else 0 for move in moves ]
        for i in range(len(target))
    ])

    target_matrix = numpy.array(target)

    objective = numpy.ones(len(moves))

    constraints = LinearConstraint(matrix, lb=target_matrix, ub=target_matrix)

    integrality = numpy.ones(len(moves))

    bounds = Bounds(lb=0, ub=numpy.inf)

    result = milp(c=objective, constraints=constraints, bounds=bounds, integrality=integrality)

    return int(result.fun)

print(sum(solve(*parse2(line)) for line in lines))