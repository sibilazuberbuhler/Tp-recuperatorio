import random
from mapa import AIR

def inteligencia_gnomo(mapa, pos_jugador, pos_gnomo):
    distancia = abs(pos_jugador[0] - pos_gnomo[0]) + abs(pos_jugador[1] - pos_gnomo[1]) #nunca la distancia va a ser negativa.
    #si el jugador esta menos de 15 pasos del gnomo, este lo detecta , y los sale a buscar
    if distancia <= 15:
        #posicion del jugador y el gnomo en las filas:
        direccion_fila = 0
        direccion_columna = 0
        if pos_jugador[0] > pos_gnomo[0] and mapa[pos_gnomo[0] + 1][pos_gnomo[1]] == AIR:
            direccion_fila = 1 #se mueve para la derecha
        elif pos_jugador[0] < pos_gnomo[0] and mapa[pos_gnomo[0] - 1][pos_gnomo[1]] == AIR:
            direccion_fila = -1 #se mueve para la izquierda
        elif pos_jugador[1] > pos_gnomo[1] and mapa[pos_gnomo[0]][pos_gnomo[1] + 1] == AIR:
            direccion_columna = 1 #se mueve para arriba
        elif pos_jugador[1] < pos_gnomo[1] and mapa[pos_gnomo[0]][pos_gnomo[1] - 1] == AIR:
            direccion_columna = -1 #se mueve para abajo


        # Calcular la nueva posición del gnomo
        nueva_posicion_gnomo = (pos_gnomo[0] + direccion_fila, pos_gnomo[1] + direccion_columna) 
        return nueva_posicion_gnomo
    else:
    #si el jugador está más lejos, el gnomo se mueve aleatoriamente
        opciones_movimiento = [(0,0)]
        if pos_gnomo[0] != len(mapa) -1 and mapa[pos_gnomo[0] + 1][pos_gnomo[1]] == AIR:
            opciones_movimiento.append((1, 0))
        if pos_gnomo[0] != 0 and mapa[pos_gnomo[0] - 1][pos_gnomo[1]] == AIR:
            opciones_movimiento.append((-1, 0))
        if pos_gnomo[1] != len(mapa[0]) -1 and mapa[pos_gnomo[0]][pos_gnomo[1] + 1] == AIR:
            opciones_movimiento.append((0, 1))
        if pos_gnomo[1] != 0 and mapa[pos_gnomo[0]][pos_gnomo[1] - 1] == AIR:
            opciones_movimiento.append((0, -1))

        movimiento = random.choice(opciones_movimiento)
        nueva_posicion_gnomo = (pos_gnomo[0] + movimiento[0], pos_gnomo[1] + movimiento[1])
        return nueva_posicion_gnomo
