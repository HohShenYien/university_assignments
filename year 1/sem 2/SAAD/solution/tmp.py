states = []

with open("tmp.txt", "r") as file:
    for line in file.readlines():
        states.append(line.strip())

states.sort()
for state in states:
    print(f"<option>{state}</option>")