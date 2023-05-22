%Definimos las preposiciones del juego
role(white).
role(black).

index(1).
index(2).
index(3).

base(cell(M,N,x)) :- index(M) , index(N).
base(cell(M,N,o)) :- index(M) , index(N).
base(cell(M,N,b)) :- index(M) , index(N).

base(control(white)).
base(control(black)).

input(R, mark(M,N)) :- role(R) , index(M) , index(N).
input(R, noop) :- role(R).

%Ahora definimos el estado incial

init(cell(1,1,b)).
init(cell(1,2,b)).
init(cell(1,3,b)).
init(cell(2,1,b)).
init(cell(2,2,b)).
init(cell(2,3,b)).
init(cell(3,1,b)).
init(cell(3,2,b)).
init(cell(3,3,b)).
init(control(white)).

true(cell(1,1,b)).
true(cell(1,2,b)).
true(cell(1,3,b)).
true(cell(2,1,b)).
true(cell(2,2,b)).
true(cell(2,3,b)).
true(cell(3,1,b)).
true(cell(3,2,b)).
true(cell(3,3,b)).
true(control(white)).


%Ahora definimos la legalidad

legal(W, mark(X,Y)) :- true(cell(X,Y,b)) , true(control(W)).
legal(white, noop) :- true(control(black)).
legal(black, noop) :- true(control(white)).

%Ahora definimos las reglas de actualizaci�n

next(cell(M,N,x)) :- does(white,mark(M,N)) , true(cell(M,N,b)).
next(cell(M,N,o)) :- does(black,mark(M,N)) , true(cell(M,N,b)).
next(cell(M,N,W) :- true(cell(M,N,W)) , distinct(W,b)).
next(cell(M,N,b)) :- does(_, mark(J,_)) , true(cell(M,N,b)) , not(M = J).
next(cell(M,N,b)) :- does(_, mark(_,K)) ,true(cell(M,N,b)) , not(N = K).
next(control(white)) :- true(control(black)).
next(control(black)) :- true(control(white)).

%Ahora definimos la puntuaci�n

goal(white, 100) :- line(x) , \+line(o).
goal(white, 50) :- \+line(x) , \+line(o).
goal(white, 0) :- \+line(x) , line(o).

% Ahora habr�a que definir los m�todos line(Z) y los m�todos row, column
line(W) :- row(W).
line(W) :- column(W).
line(W) :- diagonal(W).

row(white) :- true(cell(M,1,x)) , true(cell(M,2,x)) , true(cell(M,3,x)).
column(white) :- true(cell(1,N,x)) , true(cell(2,N,x)) , true(cell(3,N,x)).
diagonal(white) :- true(cell(1,1,x)) , true(cell(2,2,x)) , true(cell(3,3,x)).
diagonal(white) :- true(cell(3,1,x)) , true(cell(2,2,x)) , true(cell(1,3,x)).
row(black) :- true(cell(M,1,o)) , true(cell(M,2,o)) , true(cell(M,3,o)).
column(black) :- true(cell(1,N,o)) , true(cell(2,N,o)) , true(cell(3,N,o)).
diagonal(black) :- true(cell(1,1,o)) , true(cell(2,2,o)) , true(cell(3,3,o)).
diagonal(black) :- true(cell(3,1,o)) , true(cell(2,2,o)) , true(cell(1,3,o)).



%Por �ltimo hay que definir las reglas de acabado

terminal :- line(_).
terminal  :- \+open.

open:- true(cell(_,_,b)).


