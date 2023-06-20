role(red).
role(black).

base(cell(X, Y, P)) :- column(X), height(Y), role(P).
base(control(red)).
base(control(black)).

input(R, drop(X)) :- column(X), role(R).

init(control(red)).

legal(R, drop(X)) :- columnopen(X), true(control(R)).
legal(R, noop) :- \+ true(control(R)).

next(cell(X, Y, red)) :- true(cell(X, Y, red)).
next(cell(X, Y, black)) :- true(cell(X, Y, black)).
next(cell(1, Y, P)) :- does(P, drop(Y)), columnempty(Y).
next(cell(X, Y, P)) :-  Xup is X + 1,
                        Xdown is X - 1,
                        does(P, drop(Y)),
                        height(X),
                        column(Y),
                        cellopen(Xup, Y),
                        \+ cellopen(Xdown, Y).


next(control(black)) :- does(red, drop(_)).
next(control(red)) :- does(black, drop(_)).

goal(red, 100) :- line(red).
goal(red, 50) :- \+ line(red), \+ line(black), \+ boardopen.
goal(red, 0) :- line(black).
goal(red, 0) :- \+ line(red), \+ line(black), boardopen.

goal(black, 100) :- line(black).
goal(black, 50) :- \+ line(red), \+ line(black), \+ boardopen.
goal(black, 0) :- line(red).
goal(black, 0) :- \+ line(red), \+ line(black), boardopen.

terminal :- line(red).
terminal :- line(black).
terminal :- \+ boardopen.

cellopen(X, Y) :- column(X), height(Y), \+ true(cell(X, Y, red)), \+ true(cell(X, Y, black)).
columnopen(X) :- cellopen(X, 6).
columnempty(X) :- cellopen(X, 1).
boardopen :- columnopen(_).

line(Player) :-
    cell(X1, Y, Player),
    succ(X1, X2),
    succ(X2, X3),
    succ(X3, X4),
    cell(X2, Y, Player),
    cell(X3, Y, Player),
    cell(X4, Y, Player).

line(Player) :-
    cell(X, Y1, Player),
    succ(Y1, Y2),
    succ(Y2, Y3),
    succ(Y3, Y4),
    cell(X, Y2, Player),
    cell(X, Y3, Player),
    cell(X, Y4, Player).

line(Player) :-
    cell(X1, Y1, Player),
    succ(X1, X2),
    succ(X2, X3),
    succ(X3, X4),
    succ(Y1, Y2),
    succ(Y2, Y3),
    succ(Y3, Y4),
    cell(X2, Y2, Player),
    cell(X3, Y3, Player),
    cell(X4, Y4, Player).

line(Player) :-
    cell(X1, Y4, Player),
    succ(X1, X2),
    succ(X2, X3),
    succ(X3, X4),
    succ(Y3, Y4),
    succ(Y2, Y3),
    succ(Y1, Y2),
    cell(X2, Y3, Player),
    cell(X3, Y2, Player),
    cell(X4, Y1, Player).

succ(1, 2).
succ(2, 3).
succ(3, 4).
succ(4, 5).
succ(5, 6).
succ(6, 7).
succ(7, 8).

column(1).
column(2).
column(3).
column(4).
column(5).
column(6).
column(7).
column(8).

height(1).
height(2).
height(3).
height(4).
height(5).
height(6).
