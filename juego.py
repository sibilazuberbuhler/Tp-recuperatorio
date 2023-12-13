from mapa import *
from jugador import *
from gnomo import *

def game_over(vidas, accion, indice_nivel_activo):
    return vidas == 0 or accion in "Q" or indice_nivel_activo == -1

def main():
    CANT_NIVELES = 3
    
    niveles = [] 
    for nivel in range(CANT_NIVELES):
        level = generate_level(nivel)
        while get_path(level['pos_jugador'], level['pos_pico'], level['mapa']) == []:
            level = generate_level(nivel) # Si no se puede jugar se regenera el nivel
        niveles.append(level)

    indice_nivel_activo = 0
    nivel_activo = niveles[indice_nivel_activo]
    accion = " "

    vidas = 4
    tiene_tesoro = False

    while not game_over(vidas, accion, indice_nivel_activo):
        nivel_activo = niveles[indice_nivel_activo]
        imprimir_mapa_en_vivo(nivel_activo)
        
        accion = pedir_accion_jugador()
        if accion in "WASD":
            nivel_activo['pos_jugador'] = mover_jugador(nivel_activo['mapa'], nivel_activo['pos_jugador'], accion,
                                                         nivel_activo['tiene_pico'])

        encontrado_por_gnomo = nivel_activo['pos_gnomo'] == nivel_activo['pos_jugador']
        
        nivel_activo['pos_gnomo'] = inteligencia_gnomo(nivel_activo['mapa'], nivel_activo['pos_jugador'],
                                                       nivel_activo['pos_gnomo'])
        
        encontrado_por_gnomo = encontrado_por_gnomo or (nivel_activo['pos_gnomo'] == nivel_activo['pos_jugador'])

        if encontrado_por_gnomo:
            vidas -= 1
            print(f"El gnomo te ha atrapado. Te quedan {vidas} vidas.")

            # Separar al jugador y al gnomo
            nivel_activo['pos_jugador'] = posicion_aleatoria(nivel_activo['mapa'])
            nivel_activo['pos_gnomo'] = posicion_aleatoria(nivel_activo['mapa'])
            if not nivel_activo['tiene_pico']:
                while not get_path(nivel_activo['pos_jugador'], nivel_activo['pos_pico'], nivel_activo['mapa']):
                    nivel_activo['pos_jugador'] = posicion_aleatoria(nivel_activo['mapa'])

        elif accion in "E":
            indice_nivel_activo = cambiar_nivel(indice_nivel_activo, nivel_activo['pos_jugador'],
                                                nivel_activo['pos_escalera_ascendente'],
                                                nivel_activo['pos_escalera_descendente'])
            
        elif accion in "P":
            nivel_activo['tiene_pico'] = agarrar(nivel_activo['pos_jugador'], nivel_activo['pos_pico'],
                                                       nivel_activo['tiene_pico'])
            if nivel_activo['tiene_pico']:
                nivel_activo['pos_pico'] = None

            tiene_tesoro = agarrar(nivel_activo['pos_jugador'], nivel_activo['pos_tesoro'], tiene_tesoro)
            if tiene_tesoro:
                nivel_activo['pos_tesoro'] = None

    if not tiene_tesoro:
        print("Perdiste. Has salido del calabozo sin el tesoro")
    elif vidas == 0:
        print("Perdiste. Te agarro 4 veces el gnomo")
    elif accion in "Q":
        print("Perdiste. Has salido del juego")
    else:
        print("¡FELICITACIONES HAS GANADO!")

if __name__ == "__main__":
    main()

