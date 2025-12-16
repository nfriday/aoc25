from math import prod

with open("12.txt", "r") as file:
    lines = file.read()

sections = [section.splitlines() for section in lines.split("\n\n")]

shape_sizes = [ sum([i.count("#") for i in section[1:]]) for section in sections[:-1] ]

valid = 0
for region in sections[-1]:
    parts = region.split(" ")

    region_area = prod([ int(i) for i in parts[0].strip(":").split("x") ])

    shape_counts = [ int(i) for i in parts[1:] ]

    shapes_total_area = sum(prod(i) for i in zip(shape_counts,shape_sizes))

    if shapes_total_area < region_area:
        valid+=1

print(valid)
