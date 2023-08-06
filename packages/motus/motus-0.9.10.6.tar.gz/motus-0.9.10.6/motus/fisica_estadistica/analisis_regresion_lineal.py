from sklearn.linear_model import LinearRegression
import numpy as np


def generar_series_tiempo(lista_a_procesar, brinco_temporal, longitud_ventana_tiempo):
    series_tiempo_resultantes = []
    indices_tiempo_resultantes = []
    for brinco in range(0, len(lista_a_procesar), brinco_temporal):
        nueva_serie = []
        nueva_lista_indices = []
        if (brinco+longitud_ventana_tiempo < len(lista_a_procesar)):
            for indice_lista in range(brinco, brinco+longitud_ventana_tiempo, +1):
                nueva_serie.append(lista_a_procesar[indice_lista])
                nueva_lista_indices.append(indice_lista)
            series_tiempo_resultantes.append(nueva_serie)
            indices_tiempo_resultantes.append(nueva_lista_indices)
    return np.array(indices_tiempo_resultantes), np.array(series_tiempo_resultantes)


def generar_regresion_lineal_para_series_tiempo(indices_tiempo, series_tiempo):
    lista_predicciones = []
    regresor_lineal = LinearRegression()
    for indice in range(0, len(indices_tiempo)):
        X = indices_tiempo[indice].reshape(-1, 1)
        Y = series_tiempo[indice].reshape(-1,1)
        regresor_lineal.fit(X, Y)
        prediccion = regresor_lineal.predict(X)
        lista_predicciones.append(prediccion)
    return(lista_predicciones)