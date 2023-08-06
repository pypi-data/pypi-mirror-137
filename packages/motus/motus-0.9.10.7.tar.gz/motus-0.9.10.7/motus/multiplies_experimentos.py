from motus.experimento import Experimento
import motus.fisica_estadistica.entropia_divergencia as ed
import numpy as np
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class MultiplesExperimentos:

    def __init__(self,
                 lista_archivos,
                 dimension_caja=None,
                 cantidad_filas=10,
                 cantidad_columnas=10,
                 procesar_tiempo_archivo_irregular=False,
                 puntos_importantes=None,
                 objeto_a_promediar=1,
                 tamanio_intervalo_para_promedio=100,
                 arreglo_regiones_preferidas="",
                 genera_matriz_recurrencia=False):
        self.lista_archivos = lista_archivos
        self.lista_experimentos = []
        self.resultados_entropia = {}
        self.resultados_divergencia = {}
        self.genera_matriz_recurrencia = genera_matriz_recurrencia
        self.arreglo_regiones_preferidas = arreglo_regiones_preferidas

        if dimension_caja is None:
            self.dimension_caja = [100, 100]

        self.dimension_caja = dimension_caja
        self.cantidad_filas = cantidad_filas
        self.cantidad_columnas = cantidad_columnas
        self.procesar_tiempo_archivo_irregular = procesar_tiempo_archivo_irregular
        self.puntos_importantes = puntos_importantes
        self.objeto_a_promediar = objeto_a_promediar
        self.tamanio_intervalo_para_promedio = tamanio_intervalo_para_promedio

    def inicializa_experimentos(self):

        print("Procesar tiempo irregular: ", self.procesar_tiempo_archivo_irregular)
        if isinstance(self.lista_archivos, dict):

            count = 0

            print("Diccionario de archivos: ", self.lista_archivos)

            for (nombre, valor) in self.lista_archivos.items():
                if valor.get() is True:
                    count =+ 1
                    print("conteo de experimentos: ", count)
                    self.lista_experimentos.append(Experimento(str(nombre),
                                                   dimension_caja=self.dimension_caja,
                                                   cantidad_filas=self.cantidad_filas,
                                                   cantidad_columnas=self.cantidad_columnas,
                                                   procesar_tiempo_archivo_irregular=
                                                               self.procesar_tiempo_archivo_irregular,
                                                   puntos_importantes=self.puntos_importantes,
                                                   objeto_a_promediar=self.objeto_a_promediar,
                                                   tamanio_intervalo_para_promedio=self.tamanio_intervalo_para_promedio,
                                                   genera_matriz_recurrencia=self.genera_matriz_recurrencia,
                                                   genera_regiones_preferidas=True,
                                                   arreglo_regiones_preferidas=self.arreglo_regiones_preferidas))

        else:
            for archivo in self.lista_archivos:
                self.lista_experimentos.append(Experimento(archivo,
                                                           dimension_caja=self.dimension_caja,
                                                           cantidad_filas=self.cantidad_filas,
                                                           cantidad_columnas=self.cantidad_columnas,
                                                           procesar_tiempo_archivo_irregular=
                                                           self.procesar_tiempo_archivo_irregular,
                                                           puntos_importantes=self.puntos_importantes,
                                                           objeto_a_promediar=self.objeto_a_promediar,
                                                           tamanio_intervalo_para_promedio=self.tamanio_intervalo_para_promedio,
                                                           genera_matriz_recurrencia=self.genera_matriz_recurrencia))
        self.procesa_diccionario_entropias()
        self.procesa_diccionario_divergencias()

    def procesa_diccionario_entropias(self):
        """
        Se lee uno de los diccionarios de entropía para conocer sus llaves. Por cada llave, se obtienen todos
        los datos correspondientes a esa entropía para cada experimento. La lista resultante se guarda en un
        diccionario, donde la llave es el tipo de entropía y el registro es la lista con los valores encontrados.

        El resultado es un diccionario con todas las entropías registradas, y listas con los valores de
        cada experimento
        """

        experimento_inicial = self.lista_experimentos[0]

        for tipo_entropia in sorted(experimento_inicial.entropias):
            valores_entropia = []
            for experimento in self.lista_experimentos:
                valor_entropia_experimento = experimento.entropias[tipo_entropia]
                valores_entropia.append(valor_entropia_experimento)
            self.resultados_entropia[tipo_entropia] = valores_entropia

    def procesa_diccionario_divergencias(self):
        lista_arreglos_regiones = list()
        lista_arreglos_solo_regiones_preferidas = list()
        lista_arreglos_solo_regiones_no_preferidas = list()
        for experimento in self.lista_experimentos:
            lista_arreglos_regiones.append(
                experimento.matriz_cuadriculada.flatten())
            lista_arreglos_solo_regiones_preferidas.append(
                experimento.matriz_cuadriculada_solo_regiones_preferidas.flatten())
            lista_arreglos_solo_regiones_no_preferidas.append(
                experimento.matriz_cuadriculada_solo_regiones_no_preferidas.flatten())
        self.calcula_divergencia("visitas_regiones", lista_arreglos_regiones)
        self.calcula_divergencia("visitas_regiones_preferidas", lista_arreglos_solo_regiones_preferidas)
        self.calcula_divergencia("visitas_regiones_no_preferidas", lista_arreglos_solo_regiones_no_preferidas)

    def calcula_divergencia(self, tipo_divergencia, lista_datos):
        lista_divergencia = ed.calcula_divergencias_de_lista_arreglos(lista_datos)
        self.resultados_divergencia[tipo_divergencia] = lista_divergencia

    def regresa_imagen_grafica(self, grafica):
        print("-----------------------------------------------")
        print("Gráfica deseada:", grafica)

        fig = Figure(figsize=(6, 6))
        fig_plot = fig.add_subplot(111)
        fig_plot.grid(True)

        cantidad_experimentos = len(self.lista_experimentos)

        if grafica is 'entropia_visitas_regiones':
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones"])

        elif grafica is 'entropia_visitas_regiones_preferidas':
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones_preferidas"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones_preferidas"])

        elif grafica is 'entropia_visitas_regiones_no_preferidas':
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones_no_preferidas"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["visitas_regiones_no_preferidas"])

        elif grafica is 'entropia_hist_velocidad':
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["histograma_velocidad"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos+1),
                          self.resultados_entropia["histograma_velocidad"])

        elif grafica is 'divergencia_regiones':
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones"])

        elif grafica is 'divergencia_regiones_preferidas':
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones_preferidas"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones_preferidas"])

        elif grafica is 'divergencia_regiones_no_preferidas':
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones_no_preferidas"], 'o')
            fig_plot.plot(range(1, cantidad_experimentos),
                          self.resultados_divergencia["visitas_regiones_no_preferidas"])

        return fig
