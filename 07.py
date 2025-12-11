class Grid:
    def __init__(self, data):
        self.data = data

        self.width = len(self._get_row(0))
        self.height = len(data)

        self.start = [0, next(i for i,value in enumerate(self._get_row(0)) if value=="S")]
        self._set(*self.start, 1)

    def _get_row(self, row):
        return self.data[row]

    def _get(self, row, col):
        return self.data[row][col]

    def _set(self, row, col, value):
        self.data[row][col] = value

    def _get_splitter_positions(self, row):
        return [i for i,value in enumerate(self._get_row(row)) if value=="^"]

    def _process_row(self,row):
        splits = 0

        for splitter_col in self._get_splitter_positions(row):
            if self._get(row-1,splitter_col) == 1:
                splits += 1
                for target_col in [splitter_col-1,splitter_col+1]:
                    self._set(row,target_col, 1)

        for col in range(self.width):
            if self._get(row,col) == "." and self._get(row-1,col) == 1:
                self._set(row,col,1)

        return splits

    def process(self):
        splits = 0
        for row in range(1,self.height):
            splits += self._process_row(row)
        return splits

class Grid2(Grid):

    def __init__(self, data):
        super().__init__(data)

        for i,row in enumerate(self.data):
            self.data[i] = [0 if x == "." else x for x in row]

    def _add(self,row,col,value):
        current = self._get(row,col)
        if current == "^":
            return
        if value == "^":
            return
        self._set(row,col,current+value)

    def _process_row(self,row):
        for col in range(self.width):
            above = self._get(row-1,col)
            self._add(row,col,above)

        for splitter_col in self._get_splitter_positions(row):
            for target_col in [splitter_col-1,splitter_col+1]:
                above = self._get(row-1,splitter_col)
                self._add(row,target_col,above)

    def process(self):
        for row in range(1,self.height):
            self._process_row(row)
        return sum(i for i in self._get_row(self.height-1))

    def print(self,n):
        for row in self.data[:n]:
            print("".join([str(i) for i in row]))

with open("07.txt", "r") as file:
    lines = file.read().splitlines()

# part 1
grid = Grid([ list(line) for line in lines ])
splits = grid.process()
print(splits)

# part 2
grid = Grid2([ list(line) for line in lines ])
beams = grid.process()
print(beams)