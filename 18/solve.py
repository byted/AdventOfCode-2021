import sys
import math
import re
from copy import deepcopy

def parse_sn(sn):
    # or just use "from json import loads" ... *facepalm*
    nodes = []
    for ix, c in enumerate(sn):
        if c == '[':
            nodes.append(Node(parent=nodes[-1] if len(nodes) > 0 else None))
        elif c == ']':
            p = nodes.pop()
            if len(nodes) == 0:
                return p
            if sn[ix+1] == ',':
                nodes[-1].left = p
            else:
                nodes[-1].right = p
        elif c == ',':
            pass
        else:
            new_val = Node(parent=nodes[-1], value=int(c))
            if sn[ix+1] == ',':
                nodes[-1].left = new_val
            else:
                nodes[-1].right = new_val


class Node():
    SPLIT_THRESHOLD = 10
    EXPLODE_LEVEL = 4

    def __init__(self, parent=None, pair=(None, None), value=None) -> None:
        self.left = pair[0]
        self.right = pair[1]
        self.value = value
        self.parent = parent
    
    def __str__(self) -> str:
        if self.value is not None:
            return f'{self.value}'
        return f'({self.left}, {self.right})'
    
    def __append_leafs_from_values(self, left_val, right_val):
        self.left = Node(parent=self, value=left_val)
        self.right = Node(parent=self, value=right_val)
        self.value = None
    
    def __remove_leaves(self, value=0):
        self.value = value
        self.left = None
        self.right = None
    
    def __increase_next_value(self, val, origin=None):
        if origin is None:
            # we're traverseing a subtree to it's left-most element
            if self.value is not None:
                # I'm a value, I need to increase
                self.value += val
                return
            self.left.__increase_next_value(val)
        else:
            # we're still trying to find a right subtree
            if self.right == origin:
                # didn't find a right element yet
                if self.parent is None:
                    # but we're already at the root! Nothing to increase.
                    return
                self.parent.__increase_next_value(val, origin=self)
            else:
                # we found a right subtree we navigate into to find the left-most leaf
                self.right.__increase_next_value(val)
    
    def __increase_prev_value(self, val, origin=None):
        if self.value is not None:
            # I'm a value, I need to increase
            self.value += val
            return
        
        if origin is None:
            # we're traverseing a subtree to it's right-most element
            self.right.__increase_prev_value(val)
        else:
            # we're still trying to find a left subtree
            if self.left == origin:
                # didn't find a left element yet
                if self.parent is None:
                    # but we're already at the root! Nothing to increase.
                    return
                self.parent.__increase_prev_value(val, origin=self)
            else:
                # we found a left subtree we navigate into to find the right-most leaf
                self.left.__increase_prev_value(val)
        
    def magnitude(self):
        if self.value is not None:
            return self.value
        return 3*self.left.magnitude() + 2*self.right.magnitude()
    
    def find_and_execute_explode(self, level=0):
        # print('\t'*level, self)
        if self.value is None and level >= Node.EXPLODE_LEVEL:
            # we know the children are values; it's give from the task description
            self.parent.__increase_next_value(self.right.value, origin=self)
            self.parent.__increase_prev_value(self.left.value, origin=self)
            self.__remove_leaves()
            return True

        if self.value is not None:
            return False # we're at a leaf but there's nothing to do -> return False
        
        if self.left.find_and_execute_explode(level=level+1):
            return True
        else:
            return self.right.find_and_execute_explode(level=level+1)

    def find_and_execute_split(self, level=1):
        # print('\t'*level, self)
        if self.value is not None:
            if self.value >= Node.SPLIT_THRESHOLD:
                # split
                new_val = self.value / 2
                self.__append_leafs_from_values(math.floor(new_val), math.ceil(new_val))
                return True # Something changed -> return True
            return False # we're at a leaf but there's nothing to do -> return False
        
        if self.left.find_and_execute_split(level=level+1):
            return True
        else:
            return self.right.find_and_execute_split(level=level+1)
    
    def reduce(self):
        while True:
            while self.find_and_execute_explode():
                pass
            if not self.find_and_execute_split():
                break
        return self
    
    def add(self, sn2):
        new_self = deepcopy(self)
        new_sn2 = deepcopy(sn2)
        new_root = Node(pair=(new_self, new_sn2))
        new_self.parent = new_root
        new_sn2.parent = new_root
        new_root.reduce()
        return new_root

sailfish_numbers = [parse_sn(line.strip()) for line in sys.stdin.readlines()]

current_sum = sailfish_numbers[0]
for sn in sailfish_numbers[1:]:
    current_sum = current_sum.add(sn)

print(f'Part 1: {current_sum.magnitude()}')
print(f'Part 2: {max(sn1.add(sn2).magnitude() for sn1 in sailfish_numbers for sn2 in sailfish_numbers if sn1 != sn2)}')
