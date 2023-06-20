from match import Match
from message_handler import read_file_lines
from Montecarlo import Montecarlo

white_wins = 0
black_wins = 0
ties = 0
for _ in range(1):
    game = read_file_lines("connect4.pl")
    match = Match("c4", 10, 10, game, "jugador1")
    match = match.simulate(["nil"])
    for _ in range(0,10):
        move = []
        for role in match.roles:
            move.append(match.findlegalx(role))
        print(move)
        match = match.simulate(move)
        match.print_connect_4_board()