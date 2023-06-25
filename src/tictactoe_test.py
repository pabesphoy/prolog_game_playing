from match import Match
from message_handler import read_file_lines
from Montecarlo import Montecarlo

def print_tictactoe_board(match):
        res = "|"
        i = 0
        for state in sorted(match.current_state):
            if state[-3] == "b":
                res += "  |"
                i+=1
            elif state[-3] == "x":
                res += "X |"
                i+=1
            elif state[-3] == "o":
                res += "O |"
                i+=1
            if(i % 3 == 0):
                res+="\n|"
        print(res[:-4])
        print("----------------------------------------------")


'''
game = read_file_lines("tictactoe.pl")
match = Match("tictactoe", 10, 10, "white", game=game)
match = match.simulate(["nil"])
print_tictactoe_board(match)

while not match.findterminalp():
    move = []
    move.append(Montecarlo(2,30).findbestmove("white", match, 10))
    move.append(match.findlegalr("black"))
    match = match.simulate(move)
    print_tictactoe_board(match)
    print("----------------------------------------------")
    '''