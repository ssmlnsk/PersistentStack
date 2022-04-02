import cProfile

from stack import Stack
import random

import logging
logging.disable(logging.INFO)

def a():
    stack = Stack()
    inumbers = list(range(1000000))
    jnumbers = list(range(1000000))
    random.shuffle(inumbers)
    random.shuffle(jnumbers)
    for i in inumbers:
        stack.push(jnumbers, i)

    random.shuffle(inumbers)
    for i in inumbers:
        stack = stack.pop(i)