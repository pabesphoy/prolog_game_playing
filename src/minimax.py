from random import randint

def findbestmove(role, match):
    actions = match.findlegals(role)
    action = actions[0]
    score = 0
    move_score = {}
    for i in range(0, len(actions)):
        result = minscore(role, actions[i], match)
        move_score[actions[i]] = result
        '''
        if result == 100:
            print(move_score)
            return actions[i]
        '''
        if result > score:
            score = result
            action = actions[i]
    print(move_score)
    return action

def minscore(role, action, match):
    opponent = findopponent(role, match)
    actions = match.findlegals(opponent)
    score = 100    
    for i in range(0, len(actions)):
        move = [action, actions[i]]
        newmatch = match.simulate(move)
        result = maxscore(role, newmatch)
        if result == 0:
            return 0
        elif result < score:
            score = result
    return score
    
def maxscore(role, match):
    if match.findterminalp():
        return match.findreward(role)
    actions = match.findlegals(role)
    score = 0
    for i in range(0, len(actions)):
        result = minscore(role, actions[i], match)
        if result == 100:
            return 100
        elif result > score:
            score = result
    return score

def findopponent(role, match):
    for other_role in match.roles:
        if other_role != role:
            return other_role