import numpy as np
import pandas as pd


def obtener_valor_promediado_para_distancia_a_objeto(arreglo, indice, tamanio_intervalo):
    if indice - tamanio_intervalo < 0:
        left = arreglo[0:indice]
    else:
        left = arreglo[(indice - tamanio_intervalo):indice]
    if indice + tamanio_intervalo > len(arreglo):
        right = arreglo[(indice + 1):len(arreglo)]
    else:
        right = arreglo[indice + 1:(indice + tamanio_intervalo) + 1]
    arreglo_final = left + [arreglo[indice]] + right
    promedio = sum(arreglo_final) / len(arreglo_final)
    return promedio


def obtener_arreglo_con_valores_promediados_para_distancia_a_objeto(arreglo, tamanio_intervalo):
    arreglo_con_promedio = []
    for i in range(len(arreglo)):
        valor_promediado = obtener_valor_promediado_para_distancia_a_objeto(arreglo, i, tamanio_intervalo)
        arreglo_con_promedio.append(valor_promediado)
    return arreglo_con_promedio


def obtener_vectores_posicion_flechas(vector_x, vector_y):
    x_direct = []
    y_direct = []

    for i in range(0, len(vector_x) - 1):
        x1 = vector_x[i]
        x2 = vector_x[i + 1]
        y1 = vector_y[i]
        y2 = vector_y[i + 1]
        x_punta, y_punta = obtener_punta_vector(x1, x2, y1, y2)
        x_direct.append(x_punta)
        y_direct.append(y_punta)

    return x_direct, y_direct





def obtener_punta_vector(x_1, x_2, y_1, y_2):
    return x_2 - x_1, y_2 - y_1


def pintar_cilindro(x_centro, y_centro, radio, altura, ax):
    angulos = np.linspace(0, 2 * np.pi, 1000)

    x = x_centro + radio * np.cos(angulos)
    y = y_centro + radio * np.sin(angulos)

    x[x < 0] = np.nan
    y[y < 0] = np.nan

    x[x > 100] = np.nan
    y[y > 100] = np.nan

    z = np.linspace(0, altura, 1000)

    x_cilindro, z_cilindro = np.meshgrid(x, z)

    ax.plot_surface(x_cilindro, y, z_cilindro)


def determinar_rectangulo_por_base_altura_centro(base, altura, centro):
    mitad_base = base/2
    mitad_altura = altura/2

    coordenada_x = centro[0]
    coordenada_y = centro[1]

    x1 = coordenada_x - mitad_base
    x2 = coordenada_x + mitad_base
    y1 = coordenada_y - mitad_altura
    y2 = coordenada_y + mitad_altura

    return [x1, x2], [y1, y2]


def determinar_regiones_importantes_por_cuadrado(x, y, dimension_caja, numero_filas, numero_columnas):

    tamanio_horizontal = dimension_caja[0]/numero_columnas
    tamanio_vertical = dimension_caja[1]/numero_filas

    print("Tamanio horizontal: "+str(dimension_caja[0])+"/"+str(numero_columnas)+"=", str(tamanio_horizontal))
    print("Tamanio vertical: "+str(dimension_caja[1])+"/"+str(numero_filas)+"=", str(tamanio_vertical))

    x1 = x[0]
    x2 = x[1]
    y1 = y[0]
    y2 = y[1]

    limite_inf_x = obtener_limite_sobre_eje_verificando_modulo(x1, tamanio_horizontal)
    limite_sup_x = obtener_limite_sobre_eje_verificando_modulo(x2, tamanio_horizontal)
    limite_inf_y = obtener_limite_sobre_eje_verificando_modulo(y1, tamanio_horizontal)
    limite_sup_y = obtener_limite_sobre_eje_verificando_modulo(y2, tamanio_horizontal)

    print("Limite inferior x: "+str(x1)+"//"+str(tamanio_horizontal)+" = "+str(limite_inf_x))
    print("Limite superior x: "+str(x2)+"//"+str(tamanio_horizontal)+" = "+str(limite_sup_x))
    print("Limite inferior y: "+str(y1)+"//"+str(tamanio_vertical)+" = "+str(limite_inf_y))
    print("Limite superior y: "+str(y2)+"//"+str(tamanio_vertical)+" = "+str(limite_sup_y))

    lista_regiones_importantes = []

    print(range(limite_inf_x, limite_sup_x))
    print(range(limite_inf_y, limite_sup_y))
    for i in range(limite_inf_y, limite_sup_y):
        for j in range(limite_inf_x, limite_sup_x):
            lista_regiones_importantes.append(numero_columnas * i + j)

    return lista_regiones_importantes


def obtener_limite_sobre_eje_verificando_modulo(limite, tamanio_region):
    if limite%tamanio_region == 0:
        return int(limite//tamanio_region)
    else:
        return int(limite//tamanio_region)

"""
def arreglos_a_modificar(m1, m2):
    nuevo_m1 = np.copy(m1)
    nuevo_m2 = np.copy(m2)

    indices_con_valores_0 = np.argwhere(nuevo_m2 == 0)

    for indices in indices_con_valores_0:
        nuevo_m1[indices[0], indices[1]] = 0
        nuevo_m2[indices[0], indices[1]] = 1

    return nuevo_m1, nuevo_m2
"""

def genera_serie_de_datos(datos):
    return pd.Series(datos)


def genera_dataframes_de_datos(datos):
    diccionario_csv = {
        'valores': datos
    }
    tabla_csv = pd.DataFrame(diccionario_csv)
    return tabla_csv


def exporta_archivo(archivo, nombre_a_guardar, tipo):
    if tipo is "csv":
        archivo.to_csv(nombre_a_guardar)
