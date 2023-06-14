from pyswip import Prolog
from pyswip.prolog import PrologError, cleanupProlog
import os
from random import randint
from minimax import findbestmove

prolog = None

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
        rules.query("retractall(_)")
        for statement in game.split("."):
            if statement != "":
                rules.assertz(statement)
        return rules
        
        
        prolog.clea

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
        return actions[randint(0, len(actions)-1)]
    
    def findlegalmcts(self, role):
        return 
    
    def findlegalminimax(self, role):
        return findbestmove(role, self)

    def findlegals(self, role):
        res = []
        for statement in self.current_state:
            self.game.assertz(statement)
        for legal_action in self.game.query("legal("+role+", Y)"):
            action = "does("+role+","+legal_action["Y"]+")"
            res.append(action)
        self.game.retractall("true(_)")
        self.game.retractall("does(_, _)")
        return res
    
    def simulate(self, move):
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
        self.game.retractall("true(_)")
        return list(res)

    def findreward(self, role):
        result = -1
        for true_statement in self.current_state:
            self.game.assertz(true_statement)
        for goal in self.game.query("goal("+role+",X)"):
            result = int(goal["X"])
            break
        self.game.retractall("true(_)")
        #self.check_no_statements()
        return result

    def findterminalp(self):
        try:
            for statement in self.current_state:
                self.game.assertz(statement)
            query = self.game.query("terminal")
            res = bool(list(query))
            self.game.retractall("true(_)")
            return res
        except:
            return False
        
    def print_state(self):
        res = "|"
        i = 0
        for state in sorted(self.current_state):
            if state[-3] == "b":
                res += "  |"
                i+=1
            elif state[-3] == "x":
                res += "X |"
                i+=1
            elif state[-3] == "o":
                res += "O |"
                i+=1
            if(i % 3 == 0):
                res+="\n|"
        print(res[:-4])
        print("¿Es terminal?: ", self.findterminalp())
        for role in self.roles: 
            print(role, "reward: ", self.findreward(role))
    

    
    '''
    
    def findpropositions(game):
        return 0 #TODO: DE MOMENTO NO LO IMPLEMENTAREMOS POR INUTILIDAD

    def findactions(role, game):
        return 0 #TODO: DE MOMENTO NO LO IMPLEMENTAREMOS POR INUTILIDAD
   
    

    def print_state(self):
        res = "|"
        i = 0
        for state in sorted(self.current_state):
            if state[-3] == "b":
                res += "  |"
                i+=1
            elif state[-3] == "x":
                res += "X |"
                i+=1
            elif state[-3] == "o":
                res += "O |"
                i+=1
            if(i % 3 == 0):
                res+="\n|"
        print(res[:-4])
        print("¿Es terminal?: ", self.findterminalp())
        for role in self.roles: 
            print(role, "reward: ", self.findreward(role))
    
    def check_no_statements(self):
        try:
            for true in self.game.query("true(X)"):
                raise Exception("Statement existente")
            for does in self.game.query("does(X,Y)"):
                raise Exception("Statement existente")
        except PrologError as prologerror:
            #print("Warning: retracting with no does")
            pass

    def print_statements(self):
        try:
            q_true = self.game.query("true(X)")
            if bool(list(q_true)):
                for true in q_true:
                    print("true("+true["X"]+")")
            else:
                print("NO TRUE STATEMENTS")
            q_does = self.game.query("does(X,Y)")
            if bool(list(q_does)):
                for does in q_does:
                    print("does("+does["X"]+"," + does["Y"] + ")")
            else:
                print("NO DOES STATEMENTS")
        except PrologError as prologerror:
            print("NO STATEMENTS")
             '''