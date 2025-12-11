with open("02.txt", "r") as file:
    lines = file.read().splitlines()

data = [ list(map(int,i.split("-"))) for i in "".join(lines).split(",") ]

def numbers_with_n_digits(n):
    start = 10**(n-1)
    end = 10**n
    for number in range(start,end):
        yield number

# part 1

def get_invalid_ids(min, max):
    invalid_ids = []
    lengths = [n//2 for n in range(len(str(min)),len(str(max))+1) if n%2 == 0]
    for repeatable_part_length in lengths:
        for repeatable_part in numbers_with_n_digits(repeatable_part_length):
            target = int(str(repeatable_part) * 2)
            if target < min:
                continue
            if target > max:
                break
            invalid_ids.append(target)
    return invalid_ids

print(sum([ i for min, max in data for i in get_invalid_ids(min,max) ]))

# part 2

def get_invalid_ids_p2(min,max):
    invalid_ids = []
    min_length = len(str(min))
    max_length = len(str(max))
    for repeatable_part_length in range(1,max_length//2+1):
        for target_length in range(min_length, max_length+1):
            for repeatable_part in numbers_with_n_digits(repeatable_part_length):
                repeatable_part_count = target_length // repeatable_part_length
                if repeatable_part_count < 2:
                    continue # gross, but cba fixing it properly
                if target_length % repeatable_part_length != 0:
                    continue
                target = int(str(repeatable_part) * repeatable_part_count)
                if target < min:
                    continue
                if target > max:
                    break
                invalid_ids.append(target)
    return set(invalid_ids)

for min, max in data:
    for invalid_id in get_invalid_ids_p2(min,max):
        if invalid_id < min or invalid_id > max:
            print("error:", invalid_id, "not in", min, "-", max)
            exit(1)

print(sum([ i for min, max in data for i in get_invalid_ids_p2(min,max) ]))