from random import randint
import string
import random


class Stack:  # Define new class - Stack
    def __init__(self):
        self.stacklist = []

    def size(self):
        return len(self.stacklist)
        # Returns size of the stack e.g. length of a list

    def isEmpty(self):
        return self.size() == 0
        # Check if stack is empty, returns True if stack is empty

    def push(self, newItem):
        self.stacklist.append(newItem)
        # Add element on top of stack

    def pop(self):
        self.stacklist.pop()
        # Take out the top element from stack

    def peek(self):
        return self.stacklist[self.size() -1]
        # Peek, check the element on top of stack but do not remove it from stack


for s in range(1,200):
    filename = "xml_sample" + str(s) + ".xml"
    n = randint(1, 100)
    # print("N is: ", n)
    parent_element = random.choice(string.ascii_letters.lower())
    # print(parent_element)

    file = open(filename, "w")

    file.write("0" + " " + parent_element + "\n")

    stack = Stack()
    stack.push("0" + " " + parent_element)

    for i in range(1, n):
        open_close = randint(0, 1)
        if open_close == 1 and stack.size() > 1:
            closing_elem = stack.peek()
            stack.pop()
            closing_name = closing_elem[2]
            file.write("1" + " " + closing_name + "\n")
        elif open_close == 1 and stack.size() > 1:
            new_elem = random.choice(string.ascii_letters.lower())
            opening_elem = "0" + " " + new_elem
            stack.push(opening_elem)
            file.write(opening_elem + "\n")

        elif open_close == 0:
            new_elem = random.choice(string.ascii_letters.lower())
            opening_elem = "0" + " " + new_elem
            stack.push(opening_elem)
            file.write(opening_elem + "\n")

    while not stack.isEmpty():
        closing_elem = stack.peek()
        stack.pop()
        closing_name = closing_elem[2]
        file.write("1" + " " + closing_name + "\n")
    file.close()






