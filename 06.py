import math
import re

class Problems:
    def __init__(self, lines):
        data = [re.split(r'\ +', line.strip()) for line in lines]
        self.rows = data[:-1]
        self.operators = data[-1]

    def __iter__(self):
        self.pointer = 0
        return self

    def __next__(self):
        if self.pointer >= len(self.operators):
            raise StopIteration
        inputs = [ row[self.pointer] for row in self.rows ]
        operator = self.operators[self.pointer]
        self.pointer += 1
        return self._solve(inputs, operator)

    def _solve(self, inputs, operator):
        int_inputs = [int(i) for i in inputs]
        if operator == '+':
            return sum(int_inputs)
        return math.prod(int_inputs)

class Problems2:
    def __init__(self, lines):
        self.rows = lines[:-1]
        self.operators = lines[-1]
        self.operator_positions = [ position for position, value in enumerate(list(self.operators)) if value != " " ]

    def __iter__(self):
        self.pointer = 0
        return self

    def __next__(self):
        if self.pointer >= len(self.operator_positions):
            raise StopIteration

        start = self.operator_positions[self.pointer]

        if self.pointer == len(self.operator_positions) - 1:
            end = len(self.operators)
        else:
            end = self.operator_positions[self.pointer + 1] - 1

        operator = self.operators[start]

        parts = [ row[start:end] for row in self.rows ]
        inputs = [ "".join([ part[n] for part in parts ]) for n in range(len(parts[0])) ]

        self.pointer += 1

        return self._solve(inputs, operator)

    def _solve(self, inputs, operator):
        int_inputs = [int(i) for i in inputs]
        if operator == '+':
            return sum(int_inputs)
        return math.prod(int_inputs)

with open("06.txt", "r") as file:
    lines = file.read().splitlines()

problems = Problems(lines)
print(sum(solution for solution in iter(problems)))

problems = Problems2(lines)
print(sum(solution for solution in iter(problems)))