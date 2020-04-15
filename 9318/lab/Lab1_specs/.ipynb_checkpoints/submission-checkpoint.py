## import modules here
import math


################# Question 0 #################

def add(a, b):  # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x):  # do not change the heading of the function
    return math.floor(x ** 0.5)


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON=1E-7, MAX_ITER=1000):  # do not change the heading of the function
    i = 0
    x_1 = x_0
    while i < MAX_ITER:
        x_0 = x_0 - f(x_0) / fprime(x_0)
        if abs(x_0 - x_1) < EPSILON: break
        x_1 = x_0
        i += 1
    return x_0


################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)

    def __repr__(self):
        return self.name

    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)


def make_tree(tokens):  # do not change the heading of the function
    pass  # **replace** this line with your code


def max_depth(root):  # do not change the heading of the function
    pass  # **replace** this line with your code
