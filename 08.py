import math
from itertools import combinations
from collections import Counter

class Junction:
    def __init__(self, coords):
        self.coords = coords
        self.circuit = None

    def __str__(self):
        return f"{self.circuit}:{','.join(map(str,self.coords))}"

class CircuitTracker:
    def __init__(self):
        self.circuits = {}

    def new(self, id, junctions):
        self.circuits[id] = junctions

    def add(self, id, junction):
        self.circuits[id].append(junction)

    def merge(self, destination, source):
        self.circuits[destination] += self.circuits[source]
        del self.circuits[source]

    def circuit_count(self):
        return len(self.circuits)

    def circuit_max(self):
        return max(len(v) for k,v in self.circuits.items())

    def __str__(self):
        return ", ".join([f"{k}: {len(v)}" for k,v in self.circuits.items()])

def distance(a,b):
    return math.sqrt( (a.coords[0] - b.coords[0])**2 + (a.coords[1] - b.coords[1])**2 + (a.coords[2] - b.coords[2])**2 )

def gen_circuit_id():
    id = 1
    while True:
        yield id
        id += 1

def override_circuit_ids(junctions, id, new_id):
    for junction in junctions:
        if junction.circuit == id:
            junction.circuit = new_id

def join(a,b,id_generator,junctions,circuit_tracker):
    if not a.circuit and not b.circuit:
        new_circuit_id = next(id_generator)
        circuit_tracker.new(new_circuit_id, [a,b])
        a.circuit = b.circuit = new_circuit_id
        return
    if a.circuit and not b.circuit:
        circuit_tracker.add(a.circuit, b)
        b.circuit = a.circuit
        return
    if b.circuit and not a.circuit:
        circuit_tracker.add(b.circuit, a)
        a.circuit = b.circuit
        return
    if a.circuit and b.circuit and (a.circuit != b.circuit):
        circuit_tracker.merge(a.circuit,b.circuit)
        override_circuit_ids(junctions,b.circuit,a.circuit)
        return

with open("08.txt", "r") as file:
    lines = file.read().splitlines()
data = [ list(map(int,line.split(","))) for line in lines ]

junctions = [Junction(coords) for coords in data]

distances = [[a,b,distance(a,b)] for a,b in combinations(junctions,2)]
distances = sorted(distances, key=lambda i: i[2])

gen_circuit_id = gen_circuit_id()

circuit_tracker = CircuitTracker()

part_1_iterations = 1000

for a,b,_ in distances[:part_1_iterations]:
    join(a,b,gen_circuit_id,junctions,circuit_tracker)

circuit_counts = dict(Counter(j.circuit for j in junctions))
del circuit_counts[None]
circuit_counts = [ i[1] for i in sorted(circuit_counts.items(), key=lambda x: x[1], reverse=True) ]
print(math.prod(circuit_counts[:3]))

for a,b,_ in distances[part_1_iterations:]:
    join(a,b,gen_circuit_id,junctions,circuit_tracker)
    if circuit_tracker.circuit_count() == 1 and circuit_tracker.circuit_max() == len(junctions):
        print(a.coords[0]*b.coords[0])
        break

