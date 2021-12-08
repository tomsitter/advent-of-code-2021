import numpy as np

with open('input.txt') as inp:
    data = list([list(map(int, list(row.strip()))) for row in inp])

def bin_to_dec(bin):
    # convert list of binary digits to an integer
    return int(''.join(str(i) for i in bin), 2)

def keep_digit(digits, most_common: bool):
    # return the digit that we want to keep, whether most or least common
    count_of_ones = digits.sum()
    if most_common:
        return 1 if (count_of_ones*2 >= len(digits) or len(digits)==1) else 0
    else:
        return 1 if (count_of_ones*2 < len(digits) or len(digits)==1) else 0

# Part 2

def get_number(data, most_common):
    # get number of digits that need to be filtered
    num_digits = len(data[0])

    for index in range(num_digits):
        # get the most/least common digit and filter out rows without the number
        digits = list(np.array(data).T)[index]
        keep = keep_digit(digits, most_common)
        data = [row for row in data if row[index]==keep]

        # if we obly have 1 digit left, return it as a decmial number
        if len(data) == 1:
            print(f"Num: {data[0]}")
            return bin_to_dec(data[0])


# Part 2
# O2
o2 = get_number(list(map(list, data)), most_common=True)
co2 = get_number(list(map(list, data)), most_common=False)

print(f'O2: {o2}, CO2: {co2}')
print(f'Solution 2: {o2*co2}')