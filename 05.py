with open("05.txt", "r") as file:
    lines = file.read()

ranges_lines, ingredients_lines = map(lambda x: x.splitlines(), lines.split("\n\n"))

ranges = [ list(map(int,i.split("-"))) for i in ranges_lines ]
ingredients = [ int(i) for i in ingredients_lines ]

#part 1

fresh_count = 0
for ingredient in ingredients:
    for min, max in ranges:
        if min <= ingredient <= max:
            fresh_count += 1
            break

print(fresh_count)

# part 2

def prune_range(new, existing):
    min, max = new

    existing_min, existing_max = existing

    min_overlaps = min in range(existing_min, existing_max+1)
    max_overlaps = max in range(existing_min, existing_max+1)
    new_wraps_existing = min < existing_min and max > existing_max

    if min_overlaps and max_overlaps:
        return None

    if new_wraps_existing:
        return [ [min, existing_min-1], [existing_max+1, max] ]

    if min_overlaps:
        min = existing_max + 1

    if max_overlaps:
        max = existing_min - 1

    return [ [min,max] ]

assert prune_range(new=[5,10], existing=[1,20]) == None
assert prune_range(new=[1,8], existing=[5,10]) == [ [1,4] ]
assert prune_range(new=[7,11], existing=[5,10]) == [ [11,11] ]
assert prune_range(new=[1,20], existing=[5,10]) == [ [1,4], [11,20] ]
assert prune_range(new=[5,10], existing=[5,10]) == None

fresh_ranges = []

while ranges:
    new_range = ranges.pop()
    discard = False

    for existing_range in fresh_ranges:
        pruned_ranges = prune_range(new_range, existing_range)
        if not pruned_ranges:
            discard = True
            break
        if len(pruned_ranges) > 1:
            discard = True
            ranges.extend(pruned_ranges)
            break
        new_range = pruned_ranges[0]

    if discard:
        continue

    fresh_ranges.append(new_range)

print(sum(max-min+1 for min,max in fresh_ranges))
