
class Grid:
    def __init__(self, data):
        self.grid = data

        self.rows = len(self.grid[0])
        self.cols = len(self.grid)

        for row in range(self.rows):
            for col in range(self.cols):
                self.parse(row=row,col=col)

    def get(self, row, col):
        return self.grid[row][col]

    def set(self,row,col,value):
        self.grid[row][col] = value

    def parse(self, row, col):
        value = 1 if self.get(row=row,col=col) == '@' else 0
        self.set(row=row,col=col,value=value)

    def surrounding_coords(self, row, col):
        def possible(coord):
            r,c = coord
            if r >= self.rows or r < 0:
                return False
            if c >= self.cols or c < 0:
                return False
            return True

        surrounding = [
            [row-1, col-1],
            [row-1, col],
            [row-1, col+1],
            [row, col-1],
            [row, col+1],
            [row+1, col-1],
            [row+1, col],
            [row+1, col+1],
        ]

        return filter(possible, surrounding)

    def surrounding_values(self, row, col):
        return [self.get(row=srow,col=scol) for srow,scol in self.surrounding_coords(row=row,col=col)]

    def accessible(self, row, col):
        if self.get(row=row,col=col) == 0:
            return False
        return sum(self.surrounding_values(row,col)) < 4

    def accessible_count(self):
        return sum(self.accessible(row=row,col=col) for row in range(self.rows) for col in range(self.cols))

    def remove(self, row, col):
        self.set(row=row,col=col,value=0)

    def remove_accessible(self):
        removed = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.accessible(row=row,col=col):
                    self.remove(row=row,col=col)
                    removed += 1
        return removed

with open("04.txt", "r") as file:
    lines = file.read().splitlines()
data = [list(line) for line in lines]

grid = Grid(data)

# part 1
print(grid.accessible_count())

# part 2
count = 0
while (removed := grid.remove_accessible()) > 0:
    count += removed
print(count)