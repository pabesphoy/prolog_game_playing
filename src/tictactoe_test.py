from match import Match
from message_handler import read_file_lines
import Montecarlo

white_wins = 0
black_wins = 0
ties = 0
for _ in range(10):
    game = read_file_lines("tictactoe.pl")
    match = Match("m3", 10, 10, game, "white")
    match = match.simulate(["nil"])
    match = match.simulate([match.findlegalr("white"), match.findlegalr("black")])
    match = match.simulate([match.findlegalr("white"), match.findlegalr("black")])
    match.print_state()
    while not match.findterminalp():
        move = []
        move.append(match.findlegalr("white"))
        move.append(Montecarlo.findbestmove("black", match))
        print(move)
        match = match.simulate(move)
        match.print_state()
    if match.findreward("white") == 100:
        white_wins += 1
    elif match.findreward("black") == 100:
        black_wins += 1
    else:
        ties += 1
    print(f"White wins: {white_wins}, Black wins: {black_wins}, Ties: {ties}")