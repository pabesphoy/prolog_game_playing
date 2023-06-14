import os
from pyswip import Prolog
from message_handler import read_file_lines

game = read_file_lines("tictactoe.pl")

def generate_file():
        file_name = "game_"+str(12)+".pl"
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, "w") as file:
            file.write(game.replace(".", ".\n").replace('.\n\n', '.\n').replace("\+", "~ "))
        return file_name

generate_file()

prolog = Prolog()

prolog.consult("game_12.pl")
i=0
while(True):
     prolog.assertz("true(control("+str(i)+"))")
     i += 1
     print(i)