import random
import sys
import time
import os

def gen_map(rows: int, cols: int, BLOCK='█', AIR = ' '):
  """
  Inicializa el mapa que representa el calabozo compuesto por bloques (rocas) 
  y espacios vacíos (aire). Cada vez que la función es llamada, se redefine un 
  nuevo calabozo en forma aleatoria (es decir que nunca es el mismo) 
  Arguments:
  ----------
  rows: número de filas (alto)
  cols: número de columnas (ancho)
  BLOCK: caracter que representa un bloque (pared), por defecto '█'
  AIR: caracter que representa espacio libre (aire), por defecto ' '
  Returns
  --------
  Retorna una matriz de dimensiones (rows x cols) con la representación ASCII 
  del calabozo.
  """
  tiles = [[1] * 12 + [0] * (cols - 24) + [1] * 12]  # 0 = air, 1 = rocks
  for r in range(1, rows):
      local = tiles[r - 1][:]
      for i in range(2, cols - 2):
          vecindad = local[i - 1] + local[i] + local[i + 1]
          local[i] = random.choice([0]*100+[1]*(vecindad**3*40+1))
      tiles.append(local)

  for r in range(0, rows):
      for c in range(0, cols):
          tiles[r][c] = AIR if tiles[r][c] == 0 else BLOCK
  return tiles


def get_path(init:tuple, end:tuple, map:list, path = [], visited = [], rec = 0):
    '''
    Obtiene un camino (libre de rocas) que permite unir la coordenada inicial 
    (init) y la final (end) en la matriz mapa que define al calabozo. 
    La función requiere importar el módulo sys.  
    Arguments:
    ----------
    init: tupla (x, y) que guarda las coordenadas del punto inicial. 
    end: tupla (x, y) que guarda las coordenadas del punto final
    mapa: matriz (lista de listas) cuyos elementos son los caracteres 
    que definen el calabozo.
    path: es una lista de tuplas que contiene las coordenadas que pertenecen al
    camino que une los puntos init y end.
    visited: es una lista de tuplas que guarda las posiciones ya recorridas
    y que no conducen a un camino válido.
    rec: es un contador que usa la función internamente para chequear que no se
    haya sobrepasado el máximo de recursiones posibles. En caso de excederse, 
    retorna una lista vacía [].
    Returns
    --------
    La función retorna la lista de tuplas resultante en path con el camino encontrado. 
    En caso que no encuentre un camino que asegure espacios libres entre init y 
    end, la función retorna una lista vacía []. 
    '''
    if rec > int(sys.getrecursionlimit() * 0.8):  
        return []
  
    AIR = '█'  # caracter que define el aire (libre de bloques)
    ROWS = len(map)
    COLS = len(map[0])
    x, y = init 

    if (init in path) or (init in visited) :
        return []

    path.append(init)

    if init == end:
        return path

    dir = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]
    for j,i in dir:
      if (0 <= j < COLS) and (0 <= i < ROWS) and (map[i][j] == AIR):
          r = get_path((j,i), end, map, path, visited, rec+1)
          if r != []:
            return r

    visited.append(init)
    path.remove(init)
    return []

#crear funcion del mapa, con elementos. 
def imprimir_mapa(nivel_activo:dict):
    #defino las variables que voy a usar llamandolas por clave en el diccionario.
    mapa = nivel_activo['mapa']
    pos_jugador = nivel_activo['pos_jugador']
    pos_escalera_ascendente = nivel_activo['pos_escalera_ascendente']
    pos_escalera_descendente = nivel_activo['pos_escalera_descendente']
    pos_gnomo = nivel_activo['pos_gnomo']
    pos_pico = nivel_activo['pos_pico']
    pos_tesoro = nivel_activo['pos_tesoro']
    for num_fila, fila in enumerate(mapa): # Recorro las filas, por eso las enumero
        for num_columna, columna in enumerate(fila):
            if num_fila == pos_jugador[0] and num_columna == pos_jugador[1]:
                print("@", end="")
            elif num_fila == pos_gnomo[0] and num_columna == pos_gnomo[1]:
                print("G", end="")
            elif pos_pico != None and num_fila == pos_pico[0] and num_columna == pos_pico[1]:
                print("(", end="")
            elif pos_tesoro != None and num_fila == pos_tesoro[0] and num_columna == pos_tesoro[1]:
                print("$", end="")
            elif pos_escalera_descendente != None and num_fila == pos_escalera_descendente[0] and num_columna == pos_escalera_descendente[1]:
                print(">", end="")
            elif num_fila == pos_escalera_ascendente[0] and num_columna == pos_escalera_ascendente[1]:
                print("<", end="")
            else:
                print(columna, end="")
        print()

def limpiar_terminal():
    # Función para limpiar la terminal
    os.system('cls' if os.name == 'nt' else 'clear') 

def imprimir_mapa_en_vivo(nivel_activo):
    limpiar_terminal()
    imprimir_mapa(nivel_activo)
    time.sleep(0.1)  #Tiempo que se muestra cada mapa nuevo. 


def posicion_aleatoria(mapa):
    """
    Genera una posición random en el mapa que corresponda a un espacio vacío.

    Parametros:
    mapa (lista): Una matriz que representa el mapa del calabozo.

    Returns:
    tupla: Una tupla con las coordenadas (fila, columna) de un espacio vacío en el mapa.
    """
    while True:
        fila = random.randint(0,24)
        columna = random.randint(0,79)
        if mapa[fila][columna] == " ": #quiero que me ubique el elemento que yo le pido en un espacio vacio
            return fila,columna

#funcion para poder mover al jugador hacia todos los lados, lo hicimos manual (apretar enter entre cada tecla).
def mover_jugador(mapa, pos_jugador, direccion, tiene_pico):
    if direccion == "W" or direccion == "w" : # Arriba
        nueva_posicion = (pos_jugador[0] - 1, pos_jugador[1])
    elif direccion == "A" or direccion == "a": # Izquierda
        nueva_posicion = (pos_jugador[0], pos_jugador[1] - 1)
    elif direccion == "S" or direccion == "s": # Abajo
        nueva_posicion = (pos_jugador[0] + 1, pos_jugador[1])
    elif direccion == "D" or direccion == "d": # Derecha
        nueva_posicion = (pos_jugador[0], pos_jugador[1] + 1)
    else: 
        return pos_jugador
    #cuando no reconoce la direccion ingresada, retorna la posicion actual del jugador (osea no lo mueve)
        
    #necesito hacer una condicion para que no se pueda mover el jugador afuera del mapa 
    if nueva_posicion[0] < 0 or nueva_posicion[0] > 24:
        return pos_jugador
    if nueva_posicion[1] < 0 or nueva_posicion[1] > 79:
        return pos_jugador
    
    #necesito que el jugador se pueda mover en los espacios vacios " ", el jugador no se puede mover sobre las paredes de roca
    if mapa[nueva_posicion[0]][nueva_posicion[1]] == " ":
        return nueva_posicion
    #si el jugador tiene el pico, puede romper paredes
    elif tiene_pico == True and mapa[nueva_posicion[0]][nueva_posicion[1]] == "█":
        mapa[nueva_posicion[0]][nueva_posicion[1]] = " " 
        return nueva_posicion
    else: #si el jugador no tiene el pico, no puede romper paredes, el jugador se queda en su posicion
        return pos_jugador

#funciones del jugador:

def pedir_accion_jugador(mapa, posicion_jugador):
    while True:
        accion = input("Presione la tecla W: ir hacia arriba, A: ir hacia la izquierda, S: ir hacia abajo, D: ir hacia la derecha, E: usar las escaleras, P: agarrar pico o tesoro y Q: si quieres salir del juego  ")
        if accion in "WASDEPwasdepq":
            return accion

#Funcion para que el jugador agarre el pico.       
def agarrar_pico(pos_jugador, pos_pico, tiene_pico):
    if tiene_pico == True:
        return True #tiene el pico, puede romper paredes
    elif pos_pico == None:
        return False
    elif pos_jugador[0] == pos_pico[0] and pos_jugador[1] == pos_pico[1]:
        return True
    else:
        return False

def agarrar_tesoro(pos_jugador, pos_tesoro, tiene_tesoro):
    if tiene_tesoro == True: # Ya tiene el tesoro
        return True
    elif pos_tesoro == None: # No había tesoro
        return False
    elif pos_jugador[0] == pos_tesoro[0] and pos_jugador[1] == pos_tesoro[1]: # Agarra el tesoro
        return True
    else: #Existia tesoro pero no fue agarrado
        return False

#funciones del gnomo:

def mover_gnomo_aleatorio(mapa, pos_gnomo):
    opciones_movimiento = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movimientos posibles: derecha, izquierda, abajo, arriba
    movimiento = random.choice(opciones_movimiento)
    nueva_posicion_gnomo = (pos_gnomo[0] + movimiento[0], pos_gnomo[1] + movimiento[1])

    # Verificar si la nueva posición del gnomo está dentro del rango del mapa
    if 0 <= nueva_posicion_gnomo[0] < len(mapa) and 0 <= nueva_posicion_gnomo[1] < len(mapa[0]):
        if mapa[nueva_posicion_gnomo[0]][nueva_posicion_gnomo[1]] == " ":
            return nueva_posicion_gnomo

    #Si la nueva posición no es válida, devolver la posición actual del gnomo
    return pos_gnomo

def verificar_gnomo_jugador(nueva_posicion_gnomo, nueva_posicion, mapa): #funcion para verificar si las pos del jugador y gnomo son iguales
    if nueva_posicion_gnomo == nueva_posicion: #hacer con la nueva pocicion
     return True
    return False


def inteligencia_gnomo(mapa, pos_jugador, pos_gnomo):
    distancia = abs(pos_jugador[0] - pos_gnomo[0]) + abs(pos_jugador[1] - pos_gnomo[1]) #nunca la distancia va a ser negativa.
    #si el jugador esta menos de 15 pasos del gnomo, este lo detecta , y los sale a buscar
    if distancia <= 15:
        #posicion del jugador y el gnomo en las filas:

        if pos_jugador[0] > pos_gnomo[0]:
            direccion_fila = 1#se mueve para la derecha
        elif pos_jugador[0] < pos_gnomo[0]:
            direccion_fila = -1#se mueve para la izquierda
        else:
            direccion_fila = 0

        #posicion del jugador y el gnomo en las columnas:
        if pos_jugador[1] > pos_gnomo[1]:
            direccion_columna = 1#se mueve para arriba
        elif pos_jugador[1] < pos_gnomo[1]:
            direccion_columna = -1#se mueve para abajo
        else:
            direccion_columna = 0#no se mueve el jugador, no se mueve el gnomo 

        # Calcular la nueva posición del gnomo
        nueva_posicion_gnomo = (pos_gnomo[0] + direccion_fila, pos_gnomo[1] + direccion_columna) 

        # Verificar si la nueva posición del gnomo está dentro del rango del mapa y es un espacio vacío.
        if 0 <= nueva_posicion_gnomo[0] < len(mapa) and 0 <= nueva_posicion_gnomo[1] < len(mapa[0]) and mapa[nueva_posicion_gnomo[0]][nueva_posicion_gnomo[1]] == " ":
            return nueva_posicion_gnomo

    #si el jugador está más lejos, el gnomo se mueve aleatoriamente
    opciones_movimiento = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Movimientos posibles: derecha, izquierda, abajo, arriba
    movimiento = random.choice(opciones_movimiento)
    nueva_posicion_gnomo = (pos_gnomo[0] + movimiento[0], pos_gnomo[1] + movimiento[1])
    # Si la nueva posición no es válida, devolver la posición actual del gnomo
    return pos_gnomo


def cambiar_nivel(indice_nivel_activo, pos_jugador, pos_escalera_ascendente, pos_escalera_descendente):
    if pos_jugador[0] == pos_escalera_ascendente[0] and pos_jugador[1] == pos_escalera_ascendente[1]:
        nuevo_indice_nivel_activo = indice_nivel_activo - 1
        return nuevo_indice_nivel_activo
    elif pos_jugador[0] == pos_escalera_descendente[0] and pos_jugador[1] == pos_escalera_descendente[1]:
        nuevo_indice_nivel_activo = indice_nivel_activo + 1
        return nuevo_indice_nivel_activo
    else: #Si no esta en ninguna escalera, el nivel va a seguir siendo el indice_nivel_activo
        return indice_nivel_activo


def main():
    niveles = []  # Nivel 1: pos 0, Nivel 2: pos 1, Nivel 3: pos 2
    indice_nivel_activo = 0 

    for nivel in range(3):
        while True:
            mapa = gen_map(25, 80)
            pos_jugador = posicion_aleatoria(mapa)
            pos_gnomo = posicion_aleatoria(mapa)
            pos_pico = posicion_aleatoria(mapa)
            if nivel != 2:
                pos_escalera_descendente = posicion_aleatoria(mapa)
            else:
                pos_escalera_descendente = None #el el nivel 3 no te pone escalera descendente porque no puede seguir bajando
            pos_escalera_ascendente = pos_jugador
            tiene_pico = False
            if nivel == 2:
                pos_tesoro = posicion_aleatoria(mapa)#que el tesoro solo este en el nivel 3
            else:
                pos_tesoro = None #que en el resto de los niveles no haya tesoro
            niveles.append({
                'mapa': mapa,
                'pos_jugador': pos_jugador,
                'pos_gnomo': pos_gnomo,
                'pos_pico': pos_pico,
                'pos_escalera_descendente': pos_escalera_descendente,
                'pos_escalera_ascendente': pos_escalera_ascendente,
                'pos_tesoro': pos_tesoro,
                'tiene_pico': tiene_pico,
                'vidas': 4  # Número de vidas
            })

            break

    tiene_tesoro = False
    nivel_activo = niveles[indice_nivel_activo]

    while True:
        imprimir_mapa_en_vivo(nivel_activo)
        accion = pedir_accion_jugador(nivel_activo['mapa'], nivel_activo['pos_jugador'])
        nivel_activo['pos_gnomo'] = inteligencia_gnomo(nivel_activo['mapa'], nivel_activo['pos_jugador'],
                                                       nivel_activo['pos_gnomo'])

        encontrado_por_gnomo = verificar_gnomo_jugador(nivel_activo['pos_gnomo'], nivel_activo['pos_jugador'],
                                                       nivel_activo['mapa'])

        if encontrado_por_gnomo:
            nivel_activo['vidas'] -= 1
            print(f"El gnomo te ha atrapado. Te quedan {nivel_activo['vidas']} vidas.")
            if nivel_activo['vidas'] == 0:
                print("¡Game over!")
                break

            # Separar al jugador y al gnomo
            nivel_activo['pos_jugador'] = posicion_aleatoria(nivel_activo['mapa'])
            nivel_activo['pos_gnomo'] = posicion_aleatoria(nivel_activo['mapa'])

        nivel_activo['pos_gnomo'] = mover_gnomo_aleatorio(nivel_activo['mapa'], nivel_activo['pos_gnomo'])
        nivel_activo['pos_gnomo'] = inteligencia_gnomo(nivel_activo['mapa'], nivel_activo['pos_jugador'],
                                                       nivel_activo['pos_gnomo'])

        if accion == "q" or accion=="Q":
            print("Fin del Juego. Gracias por Jugar")
            break

        if accion in "WASD" or accion in "wasd":
            nivel_activo['pos_jugador'] = mover_jugador(nivel_activo['mapa'], nivel_activo['pos_jugador'], accion,
                                                         nivel_activo['tiene_pico'])

        elif encontrado_por_gnomo:
            # Separar al jugador y al gnomo
            nivel_activo['pos_jugador'] = posicion_aleatoria(nivel_activo['mapa'])
            nivel_activo['pos_gnomo'] = posicion_aleatoria(nivel_activo['mapa'])

        elif accion == "e" or accion=="E":
            indice_nivel_activo = cambiar_nivel(indice_nivel_activo, nivel_activo['pos_jugador'],
                                                nivel_activo['pos_escalera_ascendente'],
                                                nivel_activo['pos_escalera_descendente'])
            if indice_nivel_activo == -1:
                break
            nivel_activo = niveles[indice_nivel_activo]

        elif accion == "p" or accion=="P":
            nivel_activo['tiene_pico'] = agarrar_pico(nivel_activo['pos_jugador'], nivel_activo['pos_pico'],
                                                       nivel_activo['tiene_pico'])
            if nivel_activo['tiene_pico'] == True:
                nivel_activo['pos_pico'] = None

            tiene_tesoro = agarrar_tesoro(nivel_activo['pos_jugador'], nivel_activo['pos_tesoro'], tiene_tesoro)
            if tiene_tesoro == True:
                nivel_activo['pos_tesoro'] = None

    if tiene_tesoro == False:
        print("Has perdido. Has salido del calabozo sin el tesoro")
    elif nivel_activo["vidas"] == 0:
        print("perdiste te agarro 4 veces el gnomo") 
    else:
        print("¡FELICITACIONES HAS GANADO!")

main()

