from collections import deque
import doctest

"""
    Dependency creation based on parent->child relations between objects
    All dependent objects are to be placed after the dependencies

    input -> dict 
    output list

    Example: 
    input : {
        'A':['C','E'],
        'B': [],
        'C': ['B', 'E'],
        'D': ['C'],
        'E':[]
    }
    output: ['B', 'E', 'C', 'A', 'D']
"""

def walkdeps(d, inp: dict, stack: deque, visited: set):
    for k in inp[d]:
        if k not in visited:
            walkdeps(k, inp, stack, visited)
            visited.add(k)

    if d not in stack:
        stack.append(d)
    
    return stack
    
def build_deps(input: dict) -> list:
    """
        >>> build_deps({'A':['C','E'],'B': [],'C': ['B', 'E'],'D': ['C'],'E':[]})
        ['B', 'E', 'C', 'A', 'D']

        >>> build_deps( \
            {'A':['C','E','D'], \
            'B': [], \
            'C': ['B', 'E'], \
            'D': ['C'], \
            'E':[], \
            'F':['A','D']} \
            )
        ['B', 'E', 'C', 'D', 'A', 'F']
    """
    stack = deque()
    result = []
    visited = set()

    for k,v in input.items():
        walkdeps(k, input, stack, visited)
        # if k not in stack:
            # stack.append(k)    

    while stack:
        result.append(stack.popleft())

    return result 


if __name__ == "__main__":
    doctest.testmod()
    input = {
        'A':['C','E'],
        'B': [],
        'C': ['B', 'E'],
        'D': ['C'],
        'E':[]
        }

    print(build_deps(input))
    print(build_deps({'A':['C','E', 'D'], \
        'B': [], \
        'C': ['B', 'E'], \
        'D': ['C'], \
        'E':[], \
        'F':['A','D']
        }))