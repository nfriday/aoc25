with open("01.txt", "r") as file:
    lines = file.read().splitlines()
data = [ (i[0], int(i[1:])) for i in lines ]

# part 1
pos = 50
slots = 100
count = 0
for direction, value in data:
    direction_mult = 1 if direction == "R" else -1
    pos += (value * direction_mult)
    pos = pos % slots
    if pos == 0:
        count += 1

print(count)

# part 2
pos = 50
slots = 100
count = 0
for direction, value in data:
    direction_mult = 1 if direction == "R" else -1

    if pos == 0 and direction == "L":
        pos = 100

    pos += (value * direction_mult)

    if pos >= 100:
        count += pos // 100

    if pos <= 0:
        count += (-pos // 100) + 1

    pos = pos % slots

print(count)