
from pyswip import Prolog, Query, Functor, Variable
from random import choice
import os

prolog = Prolog()

class Match:
    def __init__(self, id, sc, pc, role, current_state = None, game = None, roles = None):
        self.id = id
        self.sc = sc
        self.pc = pc
        self.role = role
        if game:
            self.generate_file(game)
            prolog.consult(self.get_file_name(), catcherrors=True)
            prolog.assertz("set_prolog_stack(global, limit(100000000000))", catcherrors=True)
            prolog.assertz("set_prolog_stack(trail,  limit(20000000000))", catcherrors=True)
            prolog.assertz("set_prolog_stack(local,  limit(2000000000))", catcherrors=True)
        if roles:
            self.roles = roles
        else:
            self.roles = self.findroles()
        self.current_state = current_state
        self.retract_true_and_does()

    def __str__(self):
        return f"Match(id={self.id}, sc={self.sc}, pc={self.pc})"
    
    def get_state_str(self):
        res = ""
        if self.current_state:
            for statement in sorted(self.current_state):
                res += statement + ", "
        return res
    
    def generate_file(self, game):
        file_name = self.get_file_name()
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, "w") as file:
            file.write(game.replace(".", ".\n").replace('.\n\n', '.\n'))
    
    def get_file_name(self):
        return "game_"+str(self.id)+".pl"

    def assert_current_state(self):
        for state in self.current_state:
            prolog.assertz(state, catcherrors=True)
    
    def retract_true_and_does(self):
        prolog.retractall("true(_)", catcherrors=True)
        prolog.retractall("does(_,_)", catcherrors=True)


    #GAME METHODS
    
    def findroles(self):
        roles = []
        X = Variable()
        role = Functor("role", 1)
        q = Query(role(X))
        while q.nextSolution():
            roles.append(str(X.value))
        q.closeQuery()
        return roles
            
    def findlegals(self, role):
        res = []
        self.assert_current_state()
        Y = Variable()
        legal = Functor("legal", 2)
        q = Query(legal(role,Y))
        while q.nextSolution():
            action = "does("+role+","+str(Y.value)+")"
            if action not in res:
                res.append(action)
        q.closeQuery()
        self.retract_true_and_does()
        return res
    
    def findinits(self):
        inits = []
        X = Variable()
        init = Functor("init", 1)
        q = Query(init(X))
        while q.nextSolution():
            inits.append(f"true({str(X.value)})")
        q.closeQuery()
        return inits
    
    def findlegalx(self, role):
        return self.findlegals(role)[0]
    
    def findlegalr(self, role):
        actions = self.findlegals(role)
        return choice(actions)
    
    def simulate(self, move):
        if move == ['nil'] or move == 'nil':
            return Match(self.id, self.sc, self.pc, self.role, current_state=self.findinits(), roles=self.roles)
        else:
            return Match(self.id, self.sc, self.pc, self.role, current_state=self.findnext(move), roles=self.roles)

    def findnext(self, move):
        res = []
        self.assert_current_state()
        for action in move:
            prolog.assertz(action, catcherrors=True)
        X = Variable()
        query = Query(Functor("next", 1)(X))
        while query.nextSolution():
            true = "true("+str(X.value)+")"
            if true not in res:
                res.append(true)
        query.closeQuery()
        self.retract_true_and_does()
        return list(res)

    def findreward(self, role):
        result = -1
        self.assert_current_state()
        X = Variable()
        goal = Functor("goal", 2)
        q = Query(goal(role, X))
        while q.nextSolution():
            result = int(str(X.value))
            q.closeQuery()
            self.retract_true_and_does()
            return result

    def findterminalp(self):
            self.assert_current_state()
            query = prolog.query("terminal", catcherrors=True)
            res = bool(list(query))
            query.close()
            self.retract_true_and_does()
            return res