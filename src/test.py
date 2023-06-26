from message_handler import read_file_lines
from match import Match
from connect_4_test import print_connect_4_board_6_7
from Montecarlo import Montecarlo

game = read_file_lines("rules/connect4 67.pl")

puzzle1 = ["true(cell(1, 1, black))",
           "true(cell(2, 1, red))",
           "true(cell(1, 2, red))",
           "true(cell(2, 2, red))",
           "true(cell(1, 3, black))",
           "true(cell(2, 3, black))",
           "true(cell(1, 4, red))",
           "true(cell(2, 4, black))",
           "true(cell(3, 4, red))",
           "true(cell(1, 5, black))",
           "true(cell(2, 5, red))",
           "true(cell(1, 6, red))",
           "true(cell(2, 6, red))",
           "true(cell(3, 6, black))",
           "true(cell(1, 7, black))",
           "true(cell(2, 7, black))",
           "true(cell(3, 7, black))",
           "true(cell(4, 7, red))",
           "true(control(red))"]

puzzle2 = ["true(cell(1, 1, red))",
           "true(cell(2, 1, black))",
           "true(cell(3, 1, red))",
           "true(cell(4, 1, red))",
           "true(cell(1, 2, black))",
           "true(cell(1, 3, black))",
           "true(cell(2, 3, red))",
           "true(cell(3, 3, red))",
           "true(cell(1, 4, black))",
           "true(cell(2, 4, black))",
           "true(cell(3, 4, red))",
           "true(cell(1, 5, red))",
           "true(cell(2, 5, black))",
           "true(cell(1, 6, red))",
           "true(cell(2, 6, black))",
           "true(cell(3, 6, black))",
           "true(cell(4, 6, black))",
           "true(cell(5, 6, red))",
           "true(control(red))"]

puzzle3 = ["true(cell(1, 2, red))",
           "true(cell(2, 2, black))",
           "true(cell(3, 2, black))",
           "true(cell(4, 2, red))",
           "true(cell(1, 3, black))",
           "true(cell(2, 3, red))",
           "true(cell(3, 3, black))",
           "true(cell(4, 3, black))",
           "true(cell(1, 4, red))",
           "true(cell(2, 4, black))",
           "true(cell(1, 5, black))",
           "true(cell(2, 5, red))",
           "true(cell(1, 6, red))",
           "true(cell(2, 6, red))",
           "true(cell(1, 7, red))",
           "true(cell(2, 7, black))",
           "true(cell(3, 7, red))",
           "true(cell(4, 7, black))",
           "true(control(red))"]

puzzle4 = ["true(cell(1, 1, red))",
           "true(cell(2, 1, red))",
           "true(cell(3, 1, black))",
           "true(cell(1, 2, black))",
           "true(cell(2, 2, black))",
           "true(cell(3, 2, red))",
           "true(cell(4, 2, red))",
           "true(cell(1, 3, black))",
           "true(cell(2, 3, black))",
           "true(cell(3, 3, red))",
           "true(cell(1, 4, red))",
           "true(cell(2, 4, red))",
           "true(cell(3, 4, black))",
           "true(cell(1, 5, black))",
           "true(cell(2, 5, red))",
           "true(cell(1, 6, black))",
           "true(cell(2, 6, black))",
           "true(cell(3, 6, red))",
           "true(cell(1, 7, red))",
           "true(cell(2, 7, black))",
           "true(control(red))"]

puzzle5 = ["true(cell(1, 2, red))",
           "true(cell(1, 3, black))",
           "true(cell(2, 3, black))",
           "true(cell(1, 4, red))",
           "true(cell(2, 4, red))",
           "true(cell(3, 4, red))",
           "true(cell(4, 4, black))",
           "true(cell(5, 4, black))",
           "true(cell(1, 5, black))",
           "true(cell(2, 5, red))",
           "true(cell(3, 5, red))",
           "true(cell(4, 5, red))",
           "true(cell(5, 5, black))",
           "true(cell(1, 7, black))",
           "true(cell(2, 7, black))",
           "true(cell(3, 7, black))",
           "true(cell(4, 7, red))",
           "true(cell(5, 7, red))",
           "true(control(red))"]

puzzles = [(puzzle1, ["does(red,drop(2))", "does(red,drop(3))"]),
           (puzzle2, ["does(red,drop(5))"]),
           (puzzle3, ["does(red,drop(6))"]),
           (puzzle4, ["does(red,drop(1))", "does(red,drop(3))"]),
           (puzzle5, ["does(red,drop(6))"])]

success = 0
fails = 0
puzzle = puzzles[4]
print(f"Puzzle {puzzles.index(puzzle) + 1}")
match = Match("p", 10, None, "red", game=game, current_state=puzzle[0])
print_connect_4_board_6_7(match)
move = Montecarlo(3,8).findbestmove(match.role, match)
print(move)
if move in puzzle[1]:
    success += 1
else:
    fails += 1
print(f"Success: {success}, Fails: {fails}")