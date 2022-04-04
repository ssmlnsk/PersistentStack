import random

from stack import Stack

stack = Stack()
inumbers = list(range(10000))
a = list(range(10000))
jnumbers = []
random.shuffle(inumbers)
for i in inumbers:
    stack.push(jnumbers, i)

for i in a:
    stack.pop(jnumbers)

if __name__ == '__main__':
    pass

