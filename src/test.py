from message_handler import read_file_lines
from match import Match
from Montecarlo import Montecarlo
from tictactoe_test import print_tictactoe_board
from main import selectaction

white_wins = 0
black_wins = 0

for _ in range(10):
    game = read_file_lines("rules/tictactoe.pl")
    match = Match("tictactoe", 10, 60, "white", game=game)
    match = match.simulate(["nil"])
    print_tictactoe_board(match)
    while not match.findterminalp():
        white_action = Montecarlo(2, 30).findbestmove(match.role, match)
        black_action = selectaction(match, "black")
        match = match.simulate([white_action, black_action])
        print_tictactoe_board(match)
    if match.findreward("white") == 100:
        white_wins += 1
    elif match.findreward("black") == 100:
        black_wins += 1

    print(f"White wins: {white_wins}\nBlack wins: {black_wins}")