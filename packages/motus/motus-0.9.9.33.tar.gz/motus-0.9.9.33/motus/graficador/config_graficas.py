class ConfigGrafica:
    def __init__(self):
        self.limite_eje_x_min = None
        self.limite_eje_x_max = None
        self.limite_eje_y_min = None
        self.limite_eje_y_max = None
        self.tomar_objeto_1 = True
        self.tomar_objeto_2 = True
        self.tomar_objeto_3 = True
        self.tomar_objeto_4 = True
        self.angulo = 220
        self.dist_max_figuras = 24
        self.total_figuras = 2
        self.tipo_figura = "Cilindros"
        self.tipo_arreglo_regresion_lineal = "Velocidad"
        self.lista_consecuencias = None
        self.consecuencia_elegida = None
        self.brinco_temporal_consecuencias = 1
        self.tamanio_vectores_consecuencias = 1
        self.brinco_temporal_regresion_lineal = 2
        self.longitud_serie_tiempo = 2
        self.regiones_preferidas_3d = None

    def regresa_config_grafica_general(self):
        limites_eje_x = [self.limite_eje_x_min, self.limite_eje_x_max]
        limites_eje_y = [self.limite_eje_y_min, self.limite_eje_y_max]
        return limites_eje_x, limites_eje_y

    def regresa_config_grafica_distancias(self):
        objetos_a_utilizar = [self.objeto_1,
                              self.objeto_2,
                              self.objeto_3,
                              self.objeto_4]
        return objetos_a_utilizar

    def regresa_config_grafica_figuras(self):
        return self.dist_max_figuras, self.total_figuras, self.tipo_figura, self.angulo

    def regresa_config_grafica_regresion_lineal(self):
        return self.tipo_arreglo_regresion_lineal, self.brinco_temporal_regresion_lineal, self.longitud_serie_tiempo

    def regresa_config_grafica_consecuencias(self):
        return self.brinco_temporal_consecuencias, self.tamanio_vectores_consecuencias, self.consecuencia_elegida