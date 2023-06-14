from match import Match

matches = []

def answer(message):
    print("ANSWER TO GAME MANAGER: ", message)

def get_arguments(message):
    res = []
    args = message.replace(message.split("(")[0], "")
    args_splitted = args.split(",")
    if "[" and "]" in args:
        res.append(args_splitted[0][1:])
        res.append(args_splitted[1])
        str_aux = args.split('[')[1]
        str_aux = str_aux.split(']')[0]
        res.append(str_aux)
        res.append(args_splitted[-2])
        res.append(args_splitted[-1][:-1])
        return res
    else:
        return args_splitted

def handle(message):
    command = message.split("(")[0]
    arguments = get_arguments(message)
    if command == 'info':
        answer(info())
    elif command == 'start':
        answer(start(arguments[0], arguments[1], arguments[2], arguments[3], arguments[4]))
    elif command == 'play':
        play(arguments[0], arguments[1])
    elif command == 'stop':
        answer(stop(arguments[0], arguments[1]))
    elif command == 'abort':
        answer(abort(arguments[0]))
    else:
        raise Exception("Unexpected command: ", command)

def read_file_lines(filename):
    lines = ""
    with open(filename, 'r') as file:
        for line in file:
            line = line.rstrip('\n')
            if line and not line.startswith('%'):
                lines += line
    return lines


def info():
    return "ready"

def start(id, player, rules, sc, pc):
    matches.append(Match(id, sc, pc, rules, player))
    return "ready"

def play(id, move):
    for match in matches:
        if match.id == id:
            match.simulate(move)
            break

def stop(id, move):
    return "done"

def abort(id):
    return "done"





game = read_file_lines("tictactoe.pl")
match = Match("m3", 10, 10, game, "white")
match = match.simulate(["nil"])

while not match.findterminalp():
    move = []
    for role in match.roles:
        if role == "white":
            move.append(match.findlegalminimax(role))
        else:
            move.append(match.findlegalr(role))
    print(move)
    match = match.simulate(move)
    match.print_state()
    print("------------------------------------------------------------------------")



'''
while not match.findterminalp():
    move = []
    for role in match.roles:
        if role == "white":
            move.append(match.findlegalminimax(role))
        else:
            move.append(match.findlegalr(role))
    print(move)
    match = match.simulate(move)
    match.print_state()
    print("------------------------------------------------------------------------")


if match.findreward("white") == 100:
    marcador["white"] = marcador["white"] + 1
elif match.findreward("white") == 0:
    marcador["black"] = marcador["black"] + 1
elif match.findreward("white") == 50:
    marcador["empates"] = marcador["empates"] + 1
else:
    raise Exception("Puntuacion no esperada: ", match.findreward("white"))
    
print(marcador)
'''