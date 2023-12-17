import functools

with open('input.txt') as file:
    sequences = file.read().strip().split(',')


@functools.cache
def hash_sequence(s: str):
    hash_value = 0
    for letter in s:
        hash_value = (hash_value + ord(letter)) * 17 % 256
    return hash_value


result = [hash_sequence(s) for s in sequences]
print(sum(result))

# part 2
boxes = {i: {} for i in range(256)}
for s in sequences:
    if s[-1] == '-':
        label = s[:-1]
        boxes[hash_sequence(label)].pop(label, None)
    else:
        label, focal_length = s.split('=')
        boxes[hash_sequence(label)][label] = int(focal_length)

focusing_power = [(box + 1) * i * lens for box, lenses in boxes.items() for i, lens in
                  enumerate(lenses.values(), start=1)]
print(sum(focusing_power))
