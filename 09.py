from itertools import combinations, pairwise
from PIL import Image, ImageDraw

def area(a,b):
    return (abs(a[0]-b[0]) + 1) * (abs(a[1]-b[1]) + 1)

with open("09.txt", "r") as file:
    lines = file.read().splitlines()
data = [ list(map(int,line.split(","))) for line in lines ]

# part 1

print(max(area(a,b) for a,b in combinations(data,2)))

# part 2

def draw(data,rectangle,scale,res):

    def scaledown(coord):
        return [i//scale for i in coord]

    image = Image.new("RGB", (res,res), "white")
    draw = ImageDraw.Draw(image)
    points = [scaledown(coord) for coord in data + [data[0]]]
    draw.line(points, fill="black", width=1)

    draw_rectangle = [scaledown(coord) for coord in list(zip(sorted([x for x,_ in rectangle]),sorted([y for _,y in rectangle])))]
    draw.rectangle(draw_rectangle,outline="green",fill=None)
    # for point in rectangle:
    #     draw.point(point,fill="green")

    image.save('09.png')

def intersection_or_inner_junction(rectangle,connection):
    rectangle_x_coords = sorted([x for x,_ in rectangle])
    rectangle_y_coords = sorted([y for _,y in rectangle])
    rectangle_top_left = [rectangle_x_coords[0], rectangle_y_coords[0]]
    rectangle_top_right = [rectangle_x_coords[1], rectangle_y_coords[0]]
    rectangle_bottom_left = [rectangle_x_coords[0], rectangle_y_coords[1]]
    rectangle_bottom_right = [rectangle_x_coords[1], rectangle_y_coords[1]]

    connection_x_coords = sorted([x for x,_ in connection])
    connection_y_coords = sorted([y for _,y in connection])

    is_vertical_connection = connection_x_coords[0] == connection_x_coords[1]

    def top_collision():
        if not is_vertical_connection:
            return False
        if not rectangle_x_coords[0] < connection_x_coords[0] < rectangle_x_coords[1]:
            return False
        if connection_y_coords[0] <= rectangle_y_coords[0] and connection_y_coords[1] > rectangle_y_coords[0]:
            return True
        return False

    def bottom_collission():
        if not is_vertical_connection:
            return False
        if not rectangle_x_coords[0] < connection_x_coords[0] < rectangle_x_coords[1]:
            return False
        if connection_y_coords[0] < rectangle_y_coords[1] and connection_y_coords[1] >= rectangle_y_coords[1]:
            return True
        return False

    def left_collision():
        if is_vertical_connection:
            return False
        if not rectangle_y_coords[0] < connection_y_coords[0] < rectangle_y_coords[1]:
            return False
        if connection_x_coords[0] <= rectangle_x_coords[0] and connection_x_coords[1] > rectangle_x_coords[0]:
            return True
        return False

    def right_collision():
        if is_vertical_connection:
            return False
        if not rectangle_y_coords[0] < connection_y_coords[0] < rectangle_y_coords[1]:
            return False
        if connection_x_coords[0] < rectangle_x_coords[1] and connection_x_coords[1] >= rectangle_x_coords[1]:
            return True
        return False

    return top_collision() or bottom_collission() or left_collision() or right_collision()

max_area = 0
max_rectangle = None

connections = list(pairwise(data)) + [(data[-1],data[0])]

for rectangle in combinations(data,2):
    new_area = area(*rectangle)

    if new_area < max_area:
        continue

    valid = True
    for connection in connections:
        if intersection_or_inner_junction(rectangle,connection):
            valid = False
            break

    if not valid:
        continue

    max_area = new_area
    max_rectangle = rectangle

print(max_area)
print(max_rectangle)

draw(data,max_rectangle,100,1000)