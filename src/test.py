import os
from pyswip import Prolog



c1 = Prolog()


c1.assertz("padre(pablo)")
del c1
c2 = Prolog()
for padre in c2.query("padre(X)"):
    print(padre["X"])