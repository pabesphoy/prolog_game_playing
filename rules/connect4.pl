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
next(cell(X, Y, P)) :-  does(P, drop(Y)), height(X), column(Y), cellopen(X, Y), XDOWN is X-1, XUP is X+1, \+cellopen(XDOWN, Y), (cellopen(XUP, Y) ; \+height(XUP)).
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



cellopen(X, Y) :- column(Y), height(X), \+ true(cell(X, Y, red)), \+ true(cell(X, Y, black)).
columnopen(X) :- cellopen(6, X).
columnempty(X) :- cellopen(1, X).
boardopen :- columnopen(_).

line(Player) :-
        true(cell(M, N, Player)),
        true(cell(M1, N, Player)),
        true(cell(M2, N, Player)),
        true(cell(M3, N, Player)),
        M1 is M + 1,
        M2 is M1 + 1,
        M3 is M2 + 1;
        true(cell(M, N, Player)),
        true(cell(M, N1, Player)),
        true(cell(M, N2, Player)),
        true(cell(M, N3, Player)),
        N1 is N + 1,
        N2 is N1 + 1,
        N3 is N2 + 1;
        true(cell(M, N, Player)),
        true(cell(M1, N1, Player)),
        true(cell(M2, N2, Player)),
        true(cell(M3, N3, Player)),
        M1 is M + 1, N1 is N + 1,
        M2 is M1 + 1, N2 is N1 + 1,
        M3 is M2 + 1, N3 is N2 + 1;
        true(cell(M, N, Player)),
        true(cell(M1, N1, Player)),
        true(cell(M2, N2, Player)),
        true(cell(M3, N3, Player)),
        M1 is M + 1, N1 is N - 1,
        M2 is M1 + 1, N2 is N1 - 1,
        M3 is M2 + 1, N3 is N2 - 1.

terminal :- line(red).
terminal :- line(black).
terminal :- \+ boardopen.

column(1).
column(2).
column(3).
column(4).
column(5).

height(1).
height(2).
height(3).
height(4).
height(5).
height(6).