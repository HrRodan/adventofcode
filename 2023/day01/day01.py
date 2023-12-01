import re

with open('input.txt') as file:
    lines = [line.strip() for line in file.readlines()]

line_number = [re.sub(r'[\D]', '', line) for line in lines]
line_number_first_end = [int(line[0] + line[-1]) if line else 0 for line in line_number]

result1 = sum(line_number_first_end)

print(result1)

# part 2
number_map = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

exp = '(?=('+'|'.join(number_map.keys())+'|\d))'
line_number2 = [re.findall(exp, line) for line in lines]
line_number_numberical_2 = [[number_map.get(number, number) for number in line] for line in line_number2]
sum_lines = [int(numbers[0] + numbers[-1]) for numbers in line_number_numberical_2]
print(sum(sum_lines))