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

def myfind(s, char):
    pos = s.find(char)
    if pos == -1:  # not found
        return len(s) + 1
    else:
        return pos

def print_tree(root, indent=0):
    print(' ' * indent, root)
    if len(root.children) > 0:
        for child in root.children:
            print_tree(child, indent+4)

def next_tok(s):  # returns tok, rest_s
    if s == '':
        return (None, None)
    # normal cases
    poss = [myfind(s, ' '), myfind(s, '['), myfind(s, ']')]
    min_pos = min(poss)
    if poss[0] == min_pos:  # separator is a space
        tok, rest_s = s[: min_pos], s[min_pos + 1:]  # skip the space
        if tok == '':  # more than 1 space
            return next_tok(rest_s)
        else:
            return (tok, rest_s)
    else:  # separator is a [ or ]
        tok, rest_s = s[: min_pos], s[min_pos:]
        if tok == '':  # the next char is [ or ]
            return (rest_s[:1], rest_s[1:])
        else:
            return (tok, rest_s)


def str_to_tokens(str_tree):
    # remove \n first
    str_tree = str_tree.replace('\n', '')
    out = []

    tok, s = next_tok(str_tree)
    while tok is not None:
        out.append(tok)
        tok, s = next_tok(s)
    return out


str_tree = '''
1 [2 [3 4       5          ] 
   6 [7 8 [9]   10 [11 12] ] 
   13
  ]
'''

def max_depth(root):  # do not change the heading of the function
    if not root.children:
        return 1
    else:
        depth = max([max_depth(child) for child in root.children])
        return depth+1



def nsqrt(x):  # do not change the heading of the function
    front = 0
    end = x
    while 1:
        mid = (front+end)//2
        if mid ** 2 <= x and (mid+1) ** 2 > x:
            break
        elif (mid+1) ** 2 == x:
            return mid+1
        elif mid ** 2 > x:
            end = mid
        elif (mid+1) ** 2 < x:
            front = mid
    return mid


print(nsqrt(0))
print(nsqrt(11))
print(nsqrt(1369))