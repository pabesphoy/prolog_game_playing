from match import Match
from message_handler import read_file_lines
from Montecarlo import Montecarlo

def get_random_match_state(role, time_limit):

    game = read_file_lines("connect4.pl")
    match = Match("c4", 10, time_limit, role, game=game)
    match = match.simulate(["nil"])
    for _ in range(11):
        random_move = [match.findlegalr("red"), match.findlegalr("black")]
        if not match.simulate(random_move).findterminalp():
            match = match.simulate(random_move)
    while len(match.findlegals(role)) == 1:
        random_move = [match.findlegalr("red"), match.findlegalr("black")]
        if not match.simulate(random_move).findterminalp():
            match = match.simulate(random_move)
    return match

def get_initial_match_state():
    game = read_file_lines("connect4.pl")
    match = Match("c4", 10, 10, "jugador1", game=game)
    match = match.simulate(["nil"])

def print_connect_4_board(match):
        rows = []
        for i in range(1,7):
            row = "|"
            for j in range(1,6):
                if f"true(cell({i}, {j}, red))" in match.current_state:
                    row += "r |"
                elif f"true(cell({i}, {j}, black))" in match.current_state:
                    row += "b |"
                else:
                    row += "  |"
            rows.append(row)
        for i in range(len(rows)-1, -1, -1):
            print(rows[i])
        print("----------------------------------------")

'''
match = get_random_match_state()
print_connect_4_board(match)
move = []
move.append(Montecarlo(3,8).findbestmove("red", match, 60))
move.append(match.findlegalr("black"))
match = match.simulate(move)
print_connect_4_board(match)

'''
