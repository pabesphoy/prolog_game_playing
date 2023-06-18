from match import Match
from random import randint
from pyswip import Prolog

limit = 2
count = 5


def findbestmove(role, match):
    actions = match.findlegals(role)
    action = actions[0]
    score = 0
    for i in range(0, len(actions)):
        #print("Action", i, ":", actions[i])
        result = minscore(role, actions[i], match, 0)
        #print(result)
        if result == 100:
            return actions[i]
        if result > score:
            score = result
            action = actions[i]
    return action

def minscore(role, action, match, level):
    opponent = findopponent(role, match)
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
        result = maxscore(role, newmatch, level+1)
        if result == 0:
            return 0
        elif result < score:
            score = result
    return score
    
def maxscore(role, match, level):
    if match.findterminalp():
        #print("Encontrado terminal:")
        #match.print_state()
        #print(match.findreward(role))
        return match.findreward(role)
    if level >= limit:
        #print("Simulando desde posición:")
        #match.print_board()
        return montecarlo(role, match, count)
    actions = match.findlegals(role)
    score = 0
    for i in range(len(actions)):
        result = minscore(role, actions[i], match, level)
        if result == 100:
            return 100
        elif result > score:
            score = result
    return score

def findopponent(role, match):
    for other_role in match.roles:
        if other_role != role:
            return other_role
        
def montecarlo(role, state, count):
    total = 0
    for i in range(count): #Simulaciones por estado final
        total = total + depthcharge(role,state)
    return total/count

def depthcharge(role, state):
    if state.findterminalp():
        #print("Estado terminal: ")
        #state.print_board()
        #print(state.findreward(role))
        return state.findreward(role)
    move = []
    for i in range(len(state.roles)):
        move.append(state.findlegalr(state.roles[i]))
    newstate = state.simulate(move)
    return depthcharge(role, newstate)
'''

def findbestmove(role, match):
    actions = match.findlegals(role)
    action = actions[0]
    score = 0
    for i in range(len(actions)):
        print("Action:", actions[i])
        result = minscore(role, actions[i], match, 0)
        print("Action:", actions[i], "| Result:",result)
        if result == 100:
            return actions[i]
        elif result > score:
            action = actions[i]
            score = result    
    return action

def minscore(role, action, match, level):
    opponent = findopponent(role, match)
    actions = match.findlegals(opponent)
    score = 100    
    for i in range(0, len(actions)):
        move = [action, actions[i]]
        #print("Movimiento: ", move)
        newmatch = match.simulate(move)
        result = maxscore(role, newmatch, level)
        if result == 0:
            return 0
        elif result < score:
            score = result
    return score



def maxscore(role, state, level):
    if state.findterminalp():
        #print("Estado final:" , state.findreward(role))
        return state.findreward(role)
    if level > levels:
        #print("Montecarlo nivel", level)
        return montecarlo(role, state, count)
    actions = state.findlegals(role)
    score = 0
    for i in range(len(actions)):
        result = minscore(role, actions[i], state, level+1)
        if result == 100:
            return 100
        elif result > score:
            score = result
    return score



    



def findopponent(role, match):
    for other_role in match.roles:
        if other_role != role:
            return other_role
        
'''