from mapa import AIR, BLOCK

def mover_jugador(mapa, pos_jugador, direccion, tiene_pico):
    if direccion == "W": # Arriba
        nueva_posicion = (pos_jugador[0] - 1, pos_jugador[1])
    elif direccion == "A": # Izquierda
        nueva_posicion = (pos_jugador[0], pos_jugador[1] - 1)
    elif direccion == "S": # Abajo
        nueva_posicion = (pos_jugador[0] + 1, pos_jugador[1])
    elif direccion == "D": # Derecha
        nueva_posicion = (pos_jugador[0], pos_jugador[1] + 1)
    else: 
        return pos_jugador
        
    ROWS = len(mapa)
    COLS = len(mapa[0])

    if nueva_posicion[0] < 0 or nueva_posicion[0] > ROWS - 1:
        return pos_jugador
    if nueva_posicion[1] < 0 or nueva_posicion[1] > COLS - 1:
        return pos_jugador
    
    if mapa[nueva_posicion[0]][nueva_posicion[1]] == AIR:
        return nueva_posicion
    elif tiene_pico and mapa[nueva_posicion[0]][nueva_posicion[1]] == BLOCK:
        mapa[nueva_posicion[0]][nueva_posicion[1]] = AIR 
        return nueva_posicion
    else:
        return pos_jugador

def pedir_accion_jugador():
    accion = ""
    print("WASD: moverse")
    print("E: usar las escaleras")
    print("P: agarrar pico o tesoro")
    print("Q: si quieres salir del juego")
    while len(accion) != 1 or accion not in "WASDEPQ":
        accion = input("Ingresa una acción: ")
        accion = accion.upper()
    return accion

def agarrar(pos_jugador, pos_objeto, tiene_objeto):
    return tiene_objeto or (pos_objeto != None and pos_jugador == pos_objeto)

def cambiar_nivel(indice_nivel_activo, pos_jugador, pos_escalera_ascendente, pos_escalera_descendente):
    if pos_jugador == pos_escalera_ascendente:
        indice_nivel_activo -= 1
    elif pos_jugador == pos_escalera_descendente:
        indice_nivel_activo += 1
    return indice_nivel_activo
