def findbestmove(match, role):
    actions = match.findlegals(role)
    action = actions[0]
    score = 0

    for i in range(0, len(actions)):
        print("Acción",i+1,"de",len(actions),":", actions[i])
        #print("Buscando minscore de: ", role, "en bestmove")
        result = minscore(role, actions[i], match)
        if result > score:
            score = result
            action = actions[i]
    print("La mejor acción con score ", score, " es ", action)
    return action

def minscore(role, action, match):
    
    opponent = findopponent(role, match)
    actions = match.findlegals(opponent)
    score = 100
    for i in range(0, len(actions)):
        print("Acción mínima",i+1,"de",len(actions),":", actions[i])
        move = None
        if(role == match.findroles()[0]):
            move = [actions[i], action]
        else:
            move = [action, actions[i]]
        newmatch = match.simulate(move)
        result = maxscore(role, newmatch)
        if result < score:
            score = result
        return score
    
def maxscore(role, match):
    if match.findterminalp():
        return match.findreward(role)
    actions = match.findlegals(role)
    score = 0
    for i in range(0, len(actions)):
        print("Acción maxima",i+1,"de",len(actions),":", actions[i])
        #print("Buscando minscore de: ", role, "en maxscore")
        print("result:")
        result = minscore(role, actions[i], match)
        print("after result:")
        if result > score:
            score = result
    return score

def findopponent(role, match):
    for other_role in match.roles:
        if other_role != role:
            return other_role
