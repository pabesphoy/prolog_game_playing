from pyswip import Prolog
from pyswip.prolog import PrologError
import os
from random import randint
from minimax import findbestmove


class Match:
    def __init__(self, id, sc, pc, game, role, current_state = None):
        self.id = id
        self.sc = sc
        self.pc = pc
        self.role = role
        if (type(game) == str):
            self.game = self.get_rules(game)
        else:
            self.game = game
        self.roles = self.findroles()
        self.current_state = None
        if current_state:
            self.current_state = current_state

        

    def __str__(self):
        return f"Match(id={self.id}, sc={self.sc}, pc={self.pc})"
    
    def get_rules(self, game):
        rules = Prolog()
        for statement in game.split("."):
            if statement != "":
                rules.assertz(statement)
        return rules
    
    def clear_statements(self):
        retracts = []
        try:
            print("Primer try")
            for true in self.game.query("true(X)"):
                retracts.append("true("+true["X"]+")")
        except PrologError as prologerror:
            #print("Warning: retracting with no trues")
            pass
        try:
            print("Segundo try")
            for does in self.game.query("does(X,Y)"):
                retracts.append("does("+true["X"]+","+does["Y"]+")")
        except PrologError as prologerror:
            #print("Warning: retracting with no does")
            pass
        for r in retracts:
            print("Retractando", r)
            self.game.retract(r)

    '''
    def generate_file(self):
        file_name = "game_"+str(self.id)+".pl"
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, "w") as file:
            file.write(self.game.replace(".", ".\n").replace('.\n\n', '.\n').replace("\+", "~ "))
        return file_name
    
    def update_file(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        with open(self.file_name, "w") as file:
            file.write(self.get_rules().replace(".", ".\n").replace('.\n\n', '.\n').replace("\+", "~ "))
            file.write(self.current_state)

 '''

    #GAME METHODS
    
    def findroles(self):
        return [role["X"] for role in list(self.game.query("role(X)"))]
    
    def findinits(self):
        res = []
        for init in self.game.query("init(X)"):
            res.append("true(" + init["X"] + ")")
        return res
    
    def findlegalx(self, role):
        return self.findlegals(role)[0]
    
    def findlegalr(self, role):
        actions = self.findlegals(role)
        if 'does(black,noop)' in actions and len(actions) > 1:
            print("\n\n\n\n\n\n\n")
            print("Opciones de", role, ":", actions)
            print("¿Hay statements verdaderos? ", bool(list(self.game.query("true(X)"))))
            try:
                for true in self.game.query("true(X)"):
                    print("true(" + true["X"] + ")")
            except:
                print("NO HAY STATEMENTS QUE SEAN TRUE")
        
        return actions[randint(0, len(actions)-1)]
    
    def findlegalmcts(self, role):
        return 
    
    def findlegalminimax(self, role):
        return findbestmove(self, role)

    def findlegals(self, role):
        res = []
        self.clear_statements()
        for statement in sorted(self.current_state):
            try:
                if not bool(list(self.game.query(statement))):
                    self.game.assertz(statement)
            except:
                self.game.assertz(statement)
        #for true in self.game.query("true(X)"):
        #    print(true["X"])
        #print("COMPROBANDO ACCIONES DE " + role)
        #print("Es el turno de " + role + "? " + str(bool(list(self.game.query("true(control("+role+"))")))))
        for legal_action in self.game.query("legal("+role+", Y)"):
            action = "does("+role+","+legal_action["Y"]+")"
            if action not in res:
                res.append(action)
                #input(action["Y"])
        
        
        #print("Legales para ", role, ":", res)
        return res
    
    def simulate(self, move):
        print("A punto de limpiar statements")
        self.clear_statements()
        print("Statements limpios")
        if move == ['nil'] or move == 'nil':
            return Match(self.id, self.sc, self.pc, self.game, self.role, current_state=self.findinits())
        else:
            return Match(self.id, self.sc, self.pc, self.game, self.role, current_state=self.findnext(move))

    def findnext(self, move):
        res = set()
        statements = []
        statements.extend(self.current_state)
        statements.extend(move)
        for statement in statements:
            self.game.assertz(statement)
        for n in self.game.query("next(X)"):
            next = n["X"]
            res.add("true("+next+")")
        [self.game.retract(s) for s in statements]
        return list(res)

    def findreward(self, role):
        for true_statement in self.current_state:
            self.game.assertz(true_statement)
        for goal in self.game.query("goal("+role+",X)"):
            return int(goal["X"])
        return -1

    def findterminalp(self):
        try:
            statements = []
            statements.extend(self.current_state)
            for statement in statements:
                self.game.assertz(statement)
            query = self.game.query("terminal")
            res = bool(list(query))
            return res
        except:
            return False
    
    

    
    '''
    
    def findpropositions(game):
        return 0 #TODO: DE MOMENTO NO LO IMPLEMENTAREMOS POR INUTILIDAD

    def findactions(role, game):
        return 0 #TODO: DE MOMENTO NO LO IMPLEMENTAREMOS POR INUTILIDAD
    '''
    

    
    