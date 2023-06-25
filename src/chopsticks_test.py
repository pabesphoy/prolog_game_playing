from .match import Match
from .message_handler import read_file_lines
from .Montecarlo import Montecarlo

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

