from connect_4_test import print_connect_4_board_6_7

def findbestmove(role, match, max_level):
    actions = match.findlegals(role)
    action = actions[0]
    score = 0
    for i in range(0, len(actions)):
        result = minscore(role, actions[i], match, 1, max_level)
        if result == 100:
            return actions[i]
        if result > score:
            score = result
            action = actions[i]
    return action

def minscore(role, action, match, level, max_level):
    opponent = findopponent(role, match)
    actions = match.findlegals(opponent)
    score = 100    
    for i in range(0, len(actions)):
        move = [action, actions[i]]
        newmatch = match.simulate(move)
        result = maxscore(role, newmatch, level+1, max_level)
        if result == 0:
            return 0
        if result < score:
            score = result
    return score
    
def maxscore(role, match, level, max_level):
    if match.findterminalp():
        return match.findreward(role)
    if level >= max_level:
        return 0
    actions = match.findlegals(role)
    score = 0
    for i in range(0, len(actions)):
        result = minscore(role, actions[i], match, level, max_level)
        if result == 100:
            return 100
        elif result > score:
            score = result
    return score

def findopponent(role, match):
    for other_role in match.roles:
        if other_role != role:
            return other_role