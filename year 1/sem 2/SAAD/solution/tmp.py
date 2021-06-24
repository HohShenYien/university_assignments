import random

locations = ["Gymnasium", "Multipurpose Hall"]

with open("tmp.txt", "r") as file:
    for name in file.readlines():
        print(f'<option data-tokens="Main Hall">Main Hall</option>')
 