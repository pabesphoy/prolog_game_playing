from match import Match
from message_handler import read_file_lines
from Montecarlo import Montecarlo

white_wins = 0
black_wins = 0
ties = 0
for _ in range(10):
    game = read_file_lines("tictactoe.pl")
    match = Match("ttt3", 10, 10, game, "white")
    match = match.simulate(["nil"])
    #match = match.simulate(["does(white, mark(1,1))", "does(black, noop)"])
    #match = match.simulate(["does(white, noop)", "does(black, mark(2,2))"])
    match = match.simulate([match.findlegalr("white"), match.findlegalr("black")])
    match = match.simulate([match.findlegalr("white"), match.findlegalr("black")])
    match.print_tictactoe_board()
    while not match.findterminalp():
        move = []
        move.append(Montecarlo(3,10).findbestmove("white", match, 10))
        #move.append(Montecarlo(5,3).findbestmove("black", match, 10))
        move.append(match.findlegalr("black"))
        match = match.simulate(move)
        match.print_tictactoe_board()
        print("----------------------------------------------")
    if match.findreward("white") == 100:
        white_wins += 1
    elif match.findreward("black") == 100:
        black_wins += 1
    else:
        ties += 1
    print(f"White wins: {white_wins}, Black wins: {black_wins}, Ties: {ties}")