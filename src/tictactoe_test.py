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