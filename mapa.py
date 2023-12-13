import random
import sys
import os

AIR = ' '
BLOCK = '█'

# --------------- Funciones dadas por la cátedra -----------------

def gen_map(rows: int, cols: int):
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

def get_path(init:tuple, end:tuple, map:list):
    return get_path_rec(init, end, map, [], [], 0)

def get_path_rec(init:tuple, end:tuple, map:list, path, visited, rec):
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
  
    y, x = init 

    # Ya pasé por este lugar
    if (init in path) or (init in visited) :
        return []

    path.append(init)

    # Llegué al destino
    if init == end:
        return path

    ROWS = len(map)
    COLS = len(map[0])
    # Busco en las 4 direcciones posibles
    dir = [(y, x+1),(y+1, x),(y, x-1),(y-1, x)]
    for y1, x1 in dir:
      if (0 <= x1 < COLS) and (0 <= y1 < ROWS) and (map[y1][x1] == AIR):
          r = get_path_rec((y1,x1), end, map, path, visited, rec+1)
          if r != []:
            return r

    visited.append(init)
    path.remove(init)
    return []

# --------------- Fin de funciones dadas por la cátedra -----------------

def generate_level(nivel):
    mapa = gen_map(25, 80)
    pos_jugador = posicion_aleatoria(mapa)
    pos_pico = posicion_aleatoria(mapa)
    pos_gnomo = posicion_aleatoria(mapa)
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

    level = {
        'mapa': mapa,
        'pos_jugador': pos_jugador,
        'pos_gnomo': pos_gnomo,
        'pos_pico': pos_pico,
        'pos_escalera_descendente': pos_escalera_descendente,
        'pos_escalera_ascendente': pos_escalera_ascendente,
        'pos_tesoro': pos_tesoro,
        'tiene_pico': tiene_pico,
    }
    
    return level

def posicion_aleatoria(mapa):
    """
    Genera una posición random en el mapa que corresponda a un espacio vacío.

    Parametros:
    mapa (lista): Una matriz que representa el mapa del calabozo.

    Returns:
    tupla: Una tupla con las coordenadas (fila, columna) de un espacio vacío en el mapa.
    """
    ROWS = len(mapa)
    COLS = len(mapa[0])

    fila = random.randint(0,ROWS-1)
    columna = random.randint(0,COLS-1)
    while mapa[fila][columna] != AIR:
        fila = random.randint(0,ROWS-1)
        columna = random.randint(0,COLS-1)
    return fila,columna

def imprimir_mapa(nivel_activo:dict):
    for num_fila, fila in enumerate(nivel_activo['mapa']): # Recorro las filas, por eso las enumero
        for num_columna, columna in enumerate(fila):
            coord = (num_fila, num_columna)
            if coord == nivel_activo['pos_jugador']:
                print("@", end="")
            elif coord == nivel_activo['pos_gnomo']:
                print("G", end="")
            elif coord == nivel_activo['pos_pico']:
                print("(", end="")
            elif coord == nivel_activo['pos_tesoro']:
                print("$", end="")
            elif coord == nivel_activo['pos_escalera_descendente']:
                print(">", end="")
            elif coord == nivel_activo['pos_escalera_ascendente']:
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
