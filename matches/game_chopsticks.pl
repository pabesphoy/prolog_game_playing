role(jugador1).
role(jugador2).
handof(jugador1,rightj1).
handof(jugador1,leftj1).
handof(jugador2,rightj2).
handof(jugador2,leftj2).
fingers(0).
fingers(1).
fingers(2).
fingers(3).
fingers(4).
maxturns(30).
base(handup(R, H, F)) :- role(R), handof(R,H), fingers(F).
base(control(jugador1)).
base(control(jugador2)).
base(turn(N)) :- maxturns(M), N < M.
input(R, hit(H1, H2)) :- role(R), handof(R,H1), \+handof(R,H2).
input(R, revive) :- role(R).
input(R, noop) :- role(R).
init(handup(R, H, 1)) :- role(R), handof(R,H).
init(control(jugador1)).
init(turn(0)).
legal(R, hit(H1, H2)) :- true(control(R)), alive(H1), alive(H2), input(R, hit(H1,H2)).
legal(jugador1, revive) :- true(control(jugador1)),                                 (                                    (\+alive(rightj1),                                     alive(leftj1),                                     true(handup(jugador1, leftj1, F2)),                                     ((F2 = 4) ; F2 = 2))                                    ;                                    (alive(rightj1),                                     \+alive(leftj1),                                     true(handup(jugador1, rightj1, F1)),                                     ((F1 = 4) ; F1 = 2))                                ).
legal(jugador2, revive) :- true(control(jugador2)),                                 (                                    (\+alive(rightj2),                                     alive(leftj2),                                     true(handup(jugador2, leftj2, F2)),                                     ((F2 = 4) ; F2 = 2))                                    ;                                    (alive(rightj2),                                     \+alive(leftj2),                                     true(handup(jugador2, rightj2, F1)),                                     ((F1 = 4) ; F1 = 2))                                ).
legal(jugador1, noop) :- true(control(jugador2)).
legal(jugador2, noop) :- true(control(jugador1)).
next(handup(R, H, F)) :- true(handup(R, H, F)), \+does(_, hit(_, H)), \+does(R, revive).
next(handup(R, H, NewFingers)) :-    does(R2, hit(Hitterhand, H)),    true(handup(R, H, Fingers)),    true(handup(R2, Hitterhand, HitFingers)),    NewFingers is Fingers + HitFingers,     NewFingers < 5.
next(handup(R, H, 0)) :-    does(R2, hit(Hitterhand, H)),    true(handup(R, H, Fingers)),    true(handup(R2, Hitterhand, HitFingers)),    NewFingers is Fingers + HitFingers,     NewFingers > 4.
next(handup(jugador1, H, 2)) :- does(jugador1, revive), true(handup(jugador1, rightj1, F1)), true(handup(jugador1, leftj1, F2)), (F1 + F2 =:= 4), handof(jugador1,H).
 next(handup(jugador1, H, 1)) :- does(jugador1, revive), true(handup(jugador1, rightj1, F1)), true(handup(jugador1, leftj1, F2)), (F1 + F2 =:= 2), handof(jugador1,H).
 next(handup(jugador2, H, 2)) :- does(jugador2, revive), true(handup(jugador2, rightj2, F1)), true(handup(jugador2, leftj2, F2)), (F1 + F2 =:= 4), handof(jugador2,H).
 next(handup(jugador2, H, 1)) :- does(jugador2, revive), true(handup(jugador2, rightj2, F1)), true(handup(jugador2, leftj2, F2)), (F1 + F2 =:= 2), handof(jugador2,H).
 next(control(jugador1)) :- true(control(jugador2)).
next(control(jugador2)) :- true(control(jugador1)).
next(turn(N1)) :- true(turn(N)), N1 is N+1.
terminal :- \+ j1alive ; \+ j2alive; true(turn(N)), maxturns(N).
goal(jugador1, 100) :- \+ j2alive.
goal(jugador1, 50) :- j1alive, j2alive.
goal(jugador1, 0) :- \+ j1alive.
goal(jugador2, 100) :- goal(jugador1, 0).
goal(jugador2, 50) :- goal(jugador1, 50).
goal(jugador2, 0) :- goal(jugador1, 100).
alive(Hand) :- handof(R, Hand), true(handup(R, Hand, Fingers)), (Fingers < 5), (Fingers > 0).
j1alive :- alive(rightj1) ; alive(leftj1).
j2alive :- alive(rightj2) ; alive(leftj2).
