import os
from pyswip import Prolog

def run_queries():
    prolog = Prolog()
    prolog.assertz('father(john)')
    for father in prolog.query("father(X)"):
        print(father["X"])

    # Perform Prolog queries

    # The `prolog` instance will be garbage collected when the function returns
    # or when it goes out of scope, and the stacked strings will be cleared.

run_queries()
prolog = Prolog()
for father in prolog.query("father(X)"):
        print(father["X"])