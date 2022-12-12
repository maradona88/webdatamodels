from random import randint
import string
import random


file = open("query_examples.xml", "w")

for s in range(1, 200):
    n = randint(1, 30)
    parent_element = random.choice(string.ascii_letters.lower())
    file.write("//" + parent_element)
    for i in range(1, n):
        new_elem = random.choice(string.ascii_letters.lower())
        file.write("/" + new_elem)
    file.write("\n")
file.close()
