
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
    
    def findlegalminimax(self, role):
        return findbestmove(role, self)

    def findlegals(self, role):
        res = []
        rules = self.get_initial_rules()
        self.assert_true_and_does(rules)
        for legal_action in rules.query("legal("+role+", Y)"):
            action = "does("+role+","+legal_action["Y"]+")"
            res.append(action)
        self.retract_true_and_does(rules)
        return res
    
    def simulate(self, move):
        self.retract_true_and_does()
        if move == ['nil'] or move == 'nil':
            return Match(self.id, self.sc, self.pc, self.game, self.role, current_state=self.findinits())
        else:
            return Match(self.id, self.sc, self.pc, self.game, self.role, current_state=self.findnext(move))

    def findnext(self, move):
        res = []
        rules = self.get_initial_rules()
        self.assert_true_and_does(rules)
        for action in move:
            rules.assertz(action)
        for n in rules.query("next(X)"):
            if not "true("+n["X"]+")" in res:
                res.append("true("+n["X"]+")")
        self.retract_true_and_does(rules)
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
        self.print_tictactoe_board()
        print("¿Es terminal?: ", self.findterminalp())
        for role in self.roles: 
            print(role, "reward: ", self.findreward(role))
        #print(self.current_state)
    
    def print_tictactoe_board(self):
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
    
    def print_connect_4_board(self):
        rows = []
        for i in range(1,7):
            row = "|"
            for j in range(1,9):
                if f"true(cell({i}, {j}, red))" in self.current_state:
                    row += "r |"
                elif f"true(cell({i}, {j}, black))" in self.current_state:
                    row += "b |"
                else:
                    row += "  |"
            rows.append(row)
        for i in range(len(rows)-1, -1, -1):
            print(rows[i])