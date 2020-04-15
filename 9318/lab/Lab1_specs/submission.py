## import modules here
import math


################# Question 0 #################

def add(a, b):  # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x):  # do not change the heading of the function
    front = 0
    end = x
    while 1:
        mid = (front + end) // 2
        if mid ** 2 <= x and (mid + 1) ** 2 > x:
            break
        elif (mid + 1) ** 2 == x:
            return mid + 1
        elif mid ** 2 > x:
            end = mid
        elif (mid + 1) ** 2 < x:
            front = mid
    return mid


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
    if not tokens:
        return None
    else:
        cur = Tree(tokens[0])
        parent_ls = []
        child = None
        for i in range(len(tokens[1:])):
            if tokens[i] == '[':
                parent_ls.append(cur)
                cur = child if child is not None else cur
            elif tokens[i] == ']':
                cur = parent_ls.pop()
            else:
                child = Tree(tokens[i])
                cur.add_child(child)
        return cur



def max_depth(root):  # do not change the heading of the function
    if not root.children:
        return 1
    else:
        depth = max([max_depth(child) for child in root.children])
        return depth+1
