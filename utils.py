def findroles(string):
    substrings = []
    start_index = 0
    while start_index < len(string):
        role_index = string.find("role(", start_index)
        if role_index == -1:
            break

        role_start = role_index + 5
        closing_index = string.find(")", role_start)
        if closing_index == -1:
            break

        substring = string[role_start:closing_index]
        if not substring[0].isupper():
            substrings.append(substring)

        start_index = closing_index + 1

    return substrings

def findpropositions(game):
    return 0

def findactions(role, game):
    return 0

def findinits(game):
    return 0

def findlegalx(role,state,game):
    return 0 #primera acción legal

def findlegals(role,state,game):
    return 0 #todas las acciones legales

def simulate(move, state, roles, game):
    if move == 'nil':
        return state
    return findnext(roles, move, state, game)

def findnext(roles, move, state, game):
    return 0

def findreward(role, state, game):
    return 0

def findterminalp(state,game):
    return 0
