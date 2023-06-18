
from pyswip import Prolog
from pyswip.prolog import PrologError
from random import randint
from minimax import findbestmove
import os

prolog = None

class Match:
    def __init__(self, id, sc, pc, game, role, current_state = None):
        self.id = id
        self.sc = sc
        self.pc = pc
        self.role = role
        self.game = game
        self.generate_file(game)
        self.roles = self.findroles()
        self.current_state = None
        if current_state:
            self.current_state = current_state
        self.retract_true_and_does()

        

    def __str__(self):
        return f"Match(id={self.id}, sc={self.sc}, pc={self.pc})"
    
    def get_state_str(self):
        res = ""
        if self.current_state:
            for statement in self.current_state:
                res += statement + ", "
        return res
    
    def generate_file(self, game):
        file_name = "game_"+str(self.id)+".pl"
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, "w") as file:
            file.write(self.game.replace(".", ".\n").replace('.\n\n', '.\n'))#.replace("\+", " ~"))
        return file_name
    
    def get_initial_rules(self):
        file_name = "game_"+str(self.id)+".pl"
        rules = Prolog()
        rules.consult(file_name)
        return rules

    def assert_true_and_does(self, rules = None):
        if not rules:
            rules = self.get_initial_rules()
        for state in self.current_state:
            rules.assertz(state)
            
        return rules
    
    def retract_true_and_does(self, rules = None):
        if not rules: 
            rules = self.get_initial_rules()
        rules.retractall("true(_)")
        rules.retractall("does(_,_)")
        return rules


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
        return [role["X"] for role in list(self.get_initial_rules().query("role(X)"))]
    
    def findinits(self):
        res = []
        for init in self.get_initial_rules().query("init(X)"):
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
        self.assert_true_and_does()
        for legal_action in self.get_initial_rules().query("legal("+role+", Y)"):
            action = "does("+role+","+legal_action["Y"]+")"
            res.append(action)
        self.retract_true_and_does()
        return res
    
    def simulate(self, move):
        self.retract_true_and_does()
        if move == ['nil'] or move == 'nil':
            return Match(self.id, self.sc, self.pc, self.game, self.role, current_state=self.findinits())
        else:
            return Match(self.id, self.sc, self.pc, self.game, self.role, current_state=self.findnext(move))

    def findnext(self, move):
        res = set()
        rules = self.get_initial_rules()
        self.assert_true_and_does()
        for action in move:
            rules.assertz(action)
        for n in rules.query("next(X)"):
            res.add("true("+n["X"]+")")
        self.retract_true_and_does()
        return list(res)

    def findreward(self, role):
        result = -1
        rules = self.get_initial_rules()
        rules = self.assert_true_and_does(rules)
        
        for goal in rules.query("goal("+role+",X)"):
            result = int(goal["X"])
            break
        rules = self.retract_true_and_does(rules)
        #self.check_no_statements()
        return result

    def findterminalp(self):
            rules = self.get_initial_rules()
            rules = self.assert_true_and_does(rules)
            query = rules.query("terminal")
            res = bool(list(query))
            rules = self.retract_true_and_does(rules)
            return res
        
    def print_state(self):
        self.print_board()
        print("¿Es terminal?: ", self.findterminalp())
        for role in self.roles: 
            print(role, "reward: ", self.findreward(role))
        #print(self.current_state)
    
    def print_board(self):
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
             
    def check_no_statements(self):
        try:
            for true in self.game.query("true(X)"):
                raise Exception("Statement existente")
            for does in self.game.query("does(X,Y)"):
                raise Exception("Statement existente")
        except PrologError as prologerror:
            #print("Warning: retracting with no does")
            pass '''