import time
from message_handler import read_file_lines
from match import Match
from tictactoe_test import print_tictactoe_board
from chopsticks_test import print_chopsticks_game
from connect_4_test import print_connect_4_board, get_random_match_state
from Montecarlo import Montecarlo

def print_bienvenida():
    print("¡Bienvenid@! Esta es la interfaz de usuario del software de inteligencia artificial utilizando General Game Playing (GGP).")
    time.sleep(1)
    print("A continuación, podrá comprobar el funcionamiento de un agente de GGP, el cual es capaz de jugar a cualquier juego dadas sus reglas en la adaptación a Prolog del lenguaje de descripción de juegos.")
    time.sleep(1)
    print("Para ello, este software incluye las reglas de tres juegos distintos, sobre los que podrá efectuar de primera mano distintas pruebas.")
    time.sleep(1)
    
def elegir_juego():
    print("¿Qué juego le interesa?")
    juego = input("1: Tic-Tac-Toe\n2: Chopsticks\n3: Connect 4\n")
    while(not juego.strip().lower() in ["1", "2", "3"]):
        juego = input("Por favor, responda '1', '2' o '3'.")
    return juego.strip().lower()

def preguntar_reglas(juego):
    reglas = input("¡Fantástico! ¿Desea conocer las reglas? (s/n)\n")
    while True:
        if reglas.strip().lower() == 's':
            if juego == '1': print("Tic-Tac-Toe, o tres en raya, es un juego de mesa en el que dos jugadores se turnan para marcar casillas vacías en un tablero de 3x3, con el objetivo de alinear tres de sus símbolos en línea horizontal, vertical o diagonal antes que el oponente.")
            elif juego == '2': print("Chopsticks es un juego popular cuyo objetivo es eliminar ambas manos del oponente. Una mano se elimina cuando sus dedos levantados igualan o superan 5. Los jugadores toman turnos para añadir los dedos de una de sus manos a una mano del oponente. Además, podemos usar nuestro turno para revivir una de nuestras manos repartiendo equitativamente los dedos de nuestra mano viva siempre que estos sean pares.")
            elif juego == '3': print("El Connect 4 es un juego de mesa en el que dos jugadores se turnan para dejar caer fichas de su color (rojo y negro) en una cuadrícula vertical de 6 filas y 5 columnas, con el objetivo de ser el primero en alinear cuatro de sus fichas en línea horizontal, vertical o diagonal antes que el oponente.")
            else: raise Exception("Juego no existente.")
            time.sleep(4)
            break
        elif reglas.strip().lower() == 'n':
            break
        else:
            reglas = input("Por favor, responda 's' o 'n'.")

def preguntar_prueba(juego):

    print("¿Qué prueba desea realizar?")
    if juego in ["1", "2"]:
        prueba = input("1: Jugar vs IA\n2: IA vs IA\n3: Mejor movimiento dado un estado\n")
        while(not prueba.strip().lower() in ["1", "2", "3"]):
            prueba = input("Por favor, responda '1', '2' o '3'.")
    elif juego == '3':
        prueba = input("1: Mejor movimiento en estado aleatorio\n2: Mejor movimiento en estado dado\n")
        while(not prueba.strip().lower() in ["1", "2"]):
            prueba = input("Por favor, responda '1' o '2'.")
    return prueba.strip().lower()
    
def preguntar_tiempo_limite():
    time_limit = input("¿Cuál será el tiempo límite de la IA para seguir analizando movimientos? Escriba un número entre 10 y 200, o pulse intro para no dar límite.\n")
    if time_limit.strip() == "":
        return None
    while not time_limit.strip().isnumeric() or int(time_limit.strip()) < 10 or int(time_limit.strip()) > 200:
        time_limit = input("Por favor, un número entre 10 y 200 o pulse intro.\n")
    if time_limit.strip() == "":
        return None
    else:
        return int(time_limit.strip())

def selectaction(match, role):
    actions = match.findlegals(role)
    for i in range(1, len(actions)+1):
        print(f"{i}: {actions[i-1]}")
    action = input("Elija una acción: \n")
    while not action.strip().isnumeric() or int(action) > len(actions) or int(action) < 1:
        action = input(f"Elija una acción entre 1 y {len(actions)}: \n")
    return actions[int(action.strip())-1]

def preguntar_rol_ttt():
    rol = input("¿Con qué rol desea que juegue el jugador con el algoritmo de Montecarlo?\n1: White (x)\n2: Black (o)\n")
    while rol not in ['1', '2']:
        rol = input("Por favor, responda '1' o '2'.\n")
    if rol == '1':
        rol = "white"
    else:
        rol = 'black'
    return rol

def preguntar_rol_cp():
    rol = input("¿Con qué rol desea que juegue el jugador con el algoritmo de Montecarlo?\n1: Jugador 1\n2: Jugador 2\n")
    while rol not in ['1', '2']:
        rol = input("Por favor, responda '1' o '2'.\n")
    if rol == '1':
        rol = "jugador1"
    else:
        rol = 'jugador2'
    return rol

def preguntar_rol_c4():
    rol = input("¿Con qué rol desea que juegue el jugador con el algoritmo de Montecarlo?\n1: Red\n2: Black\n")
    while rol not in ['1', '2']:
        rol = input("Por favor, responda '1' o '2'.\n")
    if rol == '1':
        rol = "red"
    else:
        rol = 'black'
    return rol

def get_state(match):
    current_state = []
    base = match.findbase()
    while True:
        for i in range(len(base)):
            print(f"{i+1}: {base[i]}")
        added = input("Elija un estado para añadir o escriba 'exit' para salir:\n")
        if added == "exit":
            break
        elif not added.isnumeric():
            continue
        elif int(added) in range(1, len(base)+1):
            current_state.append(f"true({base[int(added)-1]})")
            base.remove(base[int(added)-1])
        else:
            print(f"Por favor, elija un número entre 1 y {len(base)}")
            time.sleep(2)
    return current_state

def ejecutar_prueba(prueba, juego):
    def ttt_p_vs_ia():
        rol = preguntar_rol_ttt()
        time_limit = preguntar_tiempo_limite()
        game = read_file_lines("rules/tictactoe.pl")
        match = Match("tictactoe", 10, time_limit, rol, game=game)
        match = match.simulate(["nil"])
        print_tictactoe_board(match)
        while not match.findterminalp():
            move = []
            if rol == 'white':
                move.append(selectaction(match, "black"))
                move.append(Montecarlo(2,30).findbestmove(rol, match))
            else:
                move.append(selectaction(match, "white"))
                move.append(Montecarlo(2,30).findbestmove(rol, match))
            match = match.simulate(move)
            print_tictactoe_board(match)

    def ttt_ia_vs_ia():
        print("Va a presenciar una partida entre dos jugadores artificiales. Un jugador usará el algoritmo de Montecarlo. Otro jugará movimientos aleatorios.")
        rol = input("¿Con qué rol desea que juegue el jugador con el algoritmo de Montecarlo?\n1: White (x)\n2: Black (o)\n")
        while rol not in ['1', '2']:
            rol = input("Por favor, responda '1' o '2'.\n")
        if rol == '1':
            rol = "white"
        else:
            rol = 'black'
        time_limit = preguntar_tiempo_limite()
        game = read_file_lines("rules/tictactoe.pl")
        match = Match("tictactoe", 10, time_limit, rol, game=game)
        match = match.simulate(["nil"])
        print_tictactoe_board(match)
        while not match.findterminalp():
            move = []
            if rol == 'white':
                move.append(match.findlegalr("black"))
                move.append(Montecarlo(2,30).findbestmove("white", match))
            else:
                move.append(match.findlegalr("white"))
                move.append(Montecarlo(2,30).findbestmove("black", match))
            match = match.simulate(move)
            print_tictactoe_board(match)

    def ttt_best_move():
        print("Ha accedido al menú de introducción de un estado de partida. Recuerde introducir un estado plausible y no terminal para un funcionamiento adecuado.")
        rol = preguntar_rol_ttt()
        time_limit = preguntar_tiempo_limite()
        game = read_file_lines("rules/tictactoe.pl")
        match = Match("tictactoe", 10, time_limit, rol, game=game)
        match = match.simulate(["nil"])
        current_state = get_state(match)
        match = Match("tictactoe", 10, time_limit, rol, game=game, current_state=current_state)
        print_tictactoe_board(match)
        try:
            print(Montecarlo(2,30).findbestmove(rol, match))
        except:
            print("Estado no válido")

    def cp_p_vs_ia():
        rol = preguntar_rol_cp()
        time_limit = preguntar_tiempo_limite()
        game = read_file_lines("rules/chopsticks.pl")
        match = Match("chopsticks", 10, time_limit, rol, game=game)
        match = match.simulate(["nil"])
        print_chopsticks_game(match)
        while not match.findterminalp():
            move = []
            if rol == 'jugador1':
                move.append(selectaction(match, "jugador2"))
                move.append(Montecarlo(2,30).findbestmove(rol, match))
            else:
                move.append(selectaction(match, "jugador1"))
                move.append(Montecarlo(2,30).findbestmove(rol, match))
            match = match.simulate(move)
            print_chopsticks_game(match)

    def cp_ia_vs_ia():
        print("Va a presenciar una partida entre dos jugadores artificiales. Un jugador usará el algoritmo de Montecarlo. Otro jugará movimientos aleatorios.")
        rol = preguntar_rol_cp()
        time_limit = preguntar_tiempo_limite()
        game = read_file_lines("rules/chopsticks.pl")
        match = Match("chopsticks", 10, time_limit, rol, game=game)
        match = match.simulate(["nil"])
        print_chopsticks_game(match)
        while not match.findterminalp():
            move = []
            if rol == 'jugador1':
                move.append(match.findlegalr("jugador2"))
                move.append(Montecarlo(2,30).findbestmove("jugador1", match))
            else:
                move.append(match.findlegalr("jugador1"))
                move.append(Montecarlo(2,30).findbestmove("jugador2", match))
            match = match.simulate(move)
            print_chopsticks_game(match)

    def cp_best_move():
        print("Ha accedido al menú de introducción de un estado de partida. Recuerde introducir un estado plausible y no terminal para un funcionamiento adecuado.")
        rol = preguntar_rol_cp()
        time_limit = preguntar_tiempo_limite()
        game = read_file_lines("rules/chopsticks.pl")
        match = Match("chopsticks", 10, time_limit, rol, game=game)
        match = match.simulate(["nil"])
        current_state = get_state(match)
        match = Match("chopsticks", 10, time_limit, rol, game=game, current_state=current_state)
        print_chopsticks_game(match)
        try:
            print(Montecarlo(2,30).findbestmove(rol, match))
        except:
            print("Estado no válido")

    def c4_random_state_best_move():
        rol = preguntar_rol_c4()
        time_limit = preguntar_tiempo_limite()
        match = get_random_match_state(rol, time_limit)
        print("Estado aleatorio: ")
        print_connect_4_board(match)
        move = []
        if rol == 'red':
            move.append(match.findlegalr("black"))
            move.append(Montecarlo(3,8).findbestmove("red", match))
        else:
            move.append(match.findlegalr("red"))
            move.append(Montecarlo(3,8).findbestmove("black", match))
        match = match.simulate(move)
        print_connect_4_board(match)

    def c4_given_state_best_move():
        print("Ha accedido al menú de introducción de un estado de partida. Recuerde introducir un estado plausible y no terminal para un funcionamiento adecuado.")
        rol = preguntar_rol_c4()
        time_limit = preguntar_tiempo_limite()
        game = read_file_lines("rules/connect4.pl")
        match = Match("connect4", 10, time_limit, rol, game=game)
        match = match.simulate(["nil"])
        current_state = get_state(match)
        match = Match("connect4", 10, time_limit, rol, game=game, current_state=current_state)
        print_connect_4_board(match)
        try:
            print(Montecarlo(3,8).findbestmove(rol, match))
        except:
            print("Estado no válido")

    if prueba == '1' and juego == '1':
        ttt_p_vs_ia()
    elif prueba == '2' and juego == '1':
        ttt_ia_vs_ia()
    elif prueba == '3' and juego == '1':
        ttt_best_move()
    elif prueba == '1' and juego == '2':
        cp_p_vs_ia()
    elif prueba == '2' and juego == '2':
        cp_ia_vs_ia()
    elif prueba == '3' and juego == '2':
        cp_best_move()
    elif prueba == '1' and juego == '3':
        c4_random_state_best_move()
    elif prueba == '2' and juego == '3':
        c4_given_state_best_move()

    


if __name__ == "__main__":
    print_bienvenida()
    juego = elegir_juego()
    preguntar_reglas(juego)
    prueba = preguntar_prueba(juego)
    ejecutar_prueba(prueba, juego)
    
    



