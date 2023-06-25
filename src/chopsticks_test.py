from match import Match
from message_handler import read_file_lines
from Montecarlo import Montecarlo
import time

def print_chopsticks_game(match):
        sorted_state = sorted(match.current_state)
        res = '''
                 O
                /|\\
                / \\ \n'''
        res += "Jugador 1:   " + sorted_state[2][-3] + "          " + sorted_state[1][-3] + "\n\n\nJugador 2:   " + sorted_state[3][-3] + "          " + sorted_state[4][-3]
        res += '''
                 \\/
                 \\|/
                  O\n'''
        print(res)
'''
game = read_file_lines("chopsticks.pl")
match = Match("c2", 10, 10, "jugador1", game=game)
match = match.simulate(["nil"])
print_chopsticks_game(match)
print("----------------------------------------------")
while not match.findterminalp():
    move = []
    move.append(Montecarlo(5,10).findbestmove("jugador1", match, 10))
    move.append(match.findlegalr("jugador2"))
    print(move)
    match = match.simulate(move)
    print_chopsticks_game(match)
    print("----------------------------------------------")
    time.sleep(5)

'''