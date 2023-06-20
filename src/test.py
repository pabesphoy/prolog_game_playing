import os
from pyswip import Prolog



c1 = Prolog()


c1.assertz("padre(pablo)")
del c1
c2 = Prolog()
for padre in c2.query("padre(X)"):
    print(padre["X"])


import itertools

def create_combinations(*lists):
    return list(itertools.product(*lists))

# Ejemplo de uso
list1 = [1, 2, 3, 4]
list2 = ['a', 'b', 'c']
list3 = ['x', 'y', 'z']

combinations = create_combinations(list1, list2, list3)
print(combinations)