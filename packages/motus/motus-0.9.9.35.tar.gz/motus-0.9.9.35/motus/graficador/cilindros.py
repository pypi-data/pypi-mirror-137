import numpy as np


def calcula_alturas_volumenes_circulares_objetos_relevantes(posiciones_x,
                                                            posiciones_y,
                                                            lista_objetos_relevantes,
                                                            tamanio=24,
                                                            divisiones=2,
                                                            tipo="cilindros"):

    if len(posiciones_x) == len(posiciones_y):

        objeto_relevante_1 = lista_objetos_relevantes[0]
        objeto_relevante_2 = lista_objetos_relevantes[1]
        objeto_relevante_3 = lista_objetos_relevantes[2]
        objeto_relevante_4 = lista_objetos_relevantes[3]

        longitud_movimientos = len(posiciones_x)
        valor_min_divivido = int(tamanio / divisiones)
        radios_figuras = list(range(valor_min_divivido, tamanio + 1, valor_min_divivido))
        cantidad_posiciones_volumen_1 = list(np.zeros(len(radios_figuras)))
        cantidad_posiciones_volumen_2 = list(np.zeros(len(radios_figuras)))
        cantidad_posiciones_volumen_3 = list(np.zeros(len(radios_figuras)))
        cantidad_posiciones_volumen_4 = list(np.zeros(len(radios_figuras)))

        for i in range(0, longitud_movimientos):
            x_pos = posiciones_x[i]
            y_pos = posiciones_y[i]
            dist_1 = calcula_distancia_entre_puntos(objeto_relevante_1[0], x_pos, objeto_relevante_1[1],
                                                    y_pos)
            dist_2 = calcula_distancia_entre_puntos(objeto_relevante_2[0], x_pos, objeto_relevante_2[1],
                                                    y_pos)
            dist_3 = calcula_distancia_entre_puntos(objeto_relevante_3[0], x_pos, objeto_relevante_3[1],
                                                    y_pos)
            dist_4 = calcula_distancia_entre_puntos(objeto_relevante_4[0], x_pos, objeto_relevante_4[1],
                                                    y_pos)
            if dist_1 < tamanio:
                cantidad_posiciones_volumen_1 = \
                    modificar_lista_para_cilindros(cantidad_posiciones_volumen_1,
                                                   radios_figuras,
                                                   dist_1,
                                                   tipo=tipo)
            if dist_2 < tamanio:
                cantidad_posiciones_volumen_2 = \
                    modificar_lista_para_cilindros(cantidad_posiciones_volumen_2,
                                                   radios_figuras,
                                                   dist_2,
                                                   tipo=tipo)
            if dist_3 < tamanio:
                cantidad_posiciones_volumen_3 = \
                    modificar_lista_para_cilindros(cantidad_posiciones_volumen_3,
                                                   radios_figuras,
                                                   dist_3,
                                                   tipo=tipo)
            if dist_4 < tamanio:
                cantidad_posiciones_volumen_4 = \
                    modificar_lista_para_cilindros(cantidad_posiciones_volumen_4,
                                                   radios_figuras,
                                                   dist_4,
                                                   tipo=tipo)

        print("Cantidad de posiciones para volumen 1:")
        print(cantidad_posiciones_volumen_1)
        print("Cantidad de posiciones para volumen 2:")
        print(cantidad_posiciones_volumen_2)
        print("Cantidad de posiciones para volumen 3:")
        print(cantidad_posiciones_volumen_3)
        print("Cantidad de posiciones para volumen 4:")
        print(cantidad_posiciones_volumen_4)

        lista_cantidad_posiciones_volumenes = [cantidad_posiciones_volumen_1, cantidad_posiciones_volumen_2,
                                               cantidad_posiciones_volumen_3, cantidad_posiciones_volumen_4]

        return lista_cantidad_posiciones_volumenes, radios_figuras


def calcula_distancia_entre_puntos(x_1, x_2, y_1, y_2):
    return np.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)


def modificar_lista_para_cilindros(lista_a_modificar, lista_radios_cilindros, distancia, tipo="cilindros"):
    if tipo == "cilindros":
        for i in range(0, len(lista_radios_cilindros)):
            if distancia < lista_radios_cilindros[i]:
                lista_a_modificar[i] += 1
    elif tipo == "arandelas":
        for i in range(0, len(lista_radios_cilindros)):
            if distancia < lista_radios_cilindros[i]:
                lista_a_modificar[i] += 1
                break
    return lista_a_modificar