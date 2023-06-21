from match import Match
from message_handler import read_file_lines
from Montecarlo import Montecarlo

def get_random_match_state():
    game = read_file_lines("connect4.pl")
    match = Match("c4", 10, 10, game, "jugador1")
    match = match.simulate(["nil"])
    for i in range(10):
        random_move = [match.findlegalr("red"), match.findlegalr("black")]
        if not match.simulate(random_move).findterminalp():
            match = match.simulate(random_move)
    return match


print("Estado aleatorio:")
match = get_random_match_state()
'''
game = read_file_lines("connect4.pl")
match = Match("c4", 10, 10, game, "jugador1")
match = match.simulate(["nil"])
'''
match.print_connect_4_board()
move = []
move.append(Montecarlo(2,10).findbestmove("red", match, 10))
move.append(match.findlegalr("black"))
match = match.simulate(move)
match.print_connect_4_board()
print("----------------------------------------")
'''
if match.findreward("red") == 100:
    ganador = "red" 
elif match.findreward("black") == 100:
    ganador = "black"
else:
    ganador = "EMPATE"

print("FIN. Ganador:", ganador)
'''


