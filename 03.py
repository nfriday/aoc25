with open("03.txt", "r") as file:
    lines = file.read().splitlines()

banks = [ list(map(int,list(line))) for line in lines ]

def max_battery(batteries):
    max = 0
    max_index = 0
    for index, battery in enumerate(batteries):
        if battery > max:
            max = battery
            max_index = index
            if max == 9:
                break
    return max_index, max

def max_joltage(bank, count):
    on_batteries = []
    min_index = 0
    for offset in range(count-1,0,-1):
        index, battery = max_battery(bank[min_index:-offset])
        min_index = min_index + index + 1
        on_batteries.append(battery)
    index, battery = max_battery(bank[min_index:]) # final battery
    on_batteries.append(battery)
    return int("".join([str(battery) for battery in on_batteries]))

result = sum(max_joltage(bank, 2) for bank in banks)
print(result)

result = sum(max_joltage(bank, 12) for bank in banks)
print(result)