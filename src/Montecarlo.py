from match import Match
from random import randint
from pyswip import Prolog
import time

class Montecarlo:

    def __init__(self, limit, count):
        self.limit = limit
        self.count = count

    def findbestmove(self, role, match, time_limit):
        actions = match.findlegals(role)
        action = actions[0]
        score = 0
        start_time = time.time()
        if len(actions) == 1:
            return action
        for i in range(0, len(actions)):
            print(f"Comprobando acción {i} para {role}, tiempo pasado: {time.time() - start_time}")
            result = self.minscore(role, actions[i], match, 0)
            if result == 100:
                return actions[i]
                
            if result > score:
                score = result
                action = actions[i]
        return action

    def minscore(self, role, action, match, level):
        opponent = self.findopponent(role, match)
        actions = match.findlegals(opponent)
        score = 100    
        for i in range(len(actions)):
            move = []
            if role == match.roles[0]:
                move = [action, actions[i]]
            else:
                move = [actions[i], action]
            #if level == 1:
                #print("Movimiento", i+1, "de", len(actions), move, "| Nivel 1")
            newmatch = match.simulate(move)
            result = self.maxscore(role, newmatch, level+1)
            if result == 0:
                return 0
            elif result < score:
                score = result
        return score
        
    def maxscore(self, role, match, level):
        if match.findterminalp():
            #print("Encontrado terminal:")
            #match.print_state()
            #print(match.findreward(role))
            return match.findreward(role)
        if level >= self.limit:
            #print("Simulando desde posición:")
            #match.print_board()
            return self.montecarlo(role, match, self.count)
        actions = match.findlegals(role)
        score = 0
        for i in range(len(actions)):
            result = self.minscore(role, actions[i], match, level)
            if result == 100:
                return 100
            elif result > score:
                score = result
        return score

    def findopponent(self, role, match):
        for other_role in match.roles:
            if other_role != role:
                return other_role
            
    def montecarlo(self, role, state, count):
        total = 0
        for i in range(count): #Simulaciones por estado final
            total = total + self.depthcharge(role,state)
        return total/count

    def depthcharge(self, role, state):
        if state.findterminalp():
            #print("Estado terminal: ")
            #state.print_board()
            #print(state.findreward(role))
            return state.findreward(role)
        move = []
        for i in range(len(state.roles)):
            move.append(state.findlegalr(state.roles[i]))
        newstate = state.simulate(move)
        return self.depthcharge(role, newstate)