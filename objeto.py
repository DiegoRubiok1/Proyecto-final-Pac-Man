"""
Created by Diego Rubio Canales in dic 2024
Universidad Carlos III de Madrid
"""
import random
from constantes import *
class Objeto:
    def __init__(self, lista_muros:list, pastillas):
        self.pastillas = pastillas
        self.lista_monedas = self.cargar_monedas(lista_muros)
        self.numero_inicial = len(self.lista_monedas)
        self.contacto_moneda = False
        self.monedas_eliminadas = 0

    # Properties para "pastillas"
    @property
    def pastillas(self):
        return self.__pastillas

    @pastillas.setter
    def pastillas(self, value):
        # Verifica que el número de pastillas sea un entero
        if not isinstance(value, int):
            raise ValueError("El atributo 'pastillas' debe ser un entero.")
        self.__pastillas = value

    # Properties para "lista_monedas"
    @property
    def lista_monedas(self):
        return self.__lista_monedas

    @lista_monedas.setter
    def lista_monedas(self, value):
        # Verifica que la lista de monedas sea una lista
        if not isinstance(value, list):
            raise ValueError("El atributo 'lista_monedas' debe ser una lista.")
        self.__lista_monedas = value

    # Properties para "numero_inicial"
    @property
    def numero_inicial(self):
        return self.__numero_inicial

    @numero_inicial.setter
    def numero_inicial(self, value):
        # Verifica que el número inicial sea un entero no negativo
        if not isinstance(value, int) or value < 0:
            raise ValueError("El atributo 'numero_inicial' debe ser un entero no negativo.")
        self.__numero_inicial = value

    # Properties para "contacto_moneda"
    @property
    def contacto_moneda(self):
        return self.__contacto_moneda

    @contacto_moneda.setter
    def contacto_moneda(self, value):
        # Verifica que el contacto_moneda sea un booleano
        if not isinstance(value, bool):
            raise ValueError("El atributo 'contacto_moneda' debe ser un valor booleano.")
        self.__contacto_moneda = value

    # Properties para "monedas_eliminadas"
    @property
    def monedas_eliminadas(self):
        return self.__monedas_eliminadas

    @monedas_eliminadas.setter
    def monedas_eliminadas(self, value):
        # Verifica que monedas_eliminadas sea un entero
        if not isinstance(value, int):
            raise ValueError("El atributo 'monedas_eliminadas' debe ser un entero.")
        self.__monedas_eliminadas = value

    def cargar_monedas(self, lista_muros: list):
        """Crea y distribuye las monedas en el tablero."""
        monedas = []
        # Extraer solo las coordenadas (x, y) de los muros
        coordenadas_muros = {(muro[0], muro[1]) for muro in lista_muros}

        # Recorre todo el tablero buscando espacios libres para monedas
        for y in range(1, 17):
            for x in range(1, WIDTH // 16 + 1):
                # Verifica si (x, y) está en las coordenadas de los muros
                if (x, y) not in coordenadas_muros and (x, y) not in (
                (8, 10), (9, 10), (10, 10)):  # Evita poner monedas en la jaula
                    # Todas las monedas inicializan como tipo 0 (monedas normales)
                    monedas.append((x, y, 0))

        # Seleccionar cuatro monedas aleatorias para ser tipo 1 (pastillas de poder)
        monedas_tipo_0 = [moneda for moneda in monedas]  # Lista de monedas disponibles
        monedas_tipo_1 = random.sample(monedas_tipo_0, self.pastillas)  # Selecciona aleatoriamente

        # Actualiza el tipo de las monedas seleccionadas a tipo 1
        for i in range(len(monedas)):
            if monedas[i] in monedas_tipo_1:
                monedas[i] = (monedas[i][0], monedas[i][1], 1)

        return monedas

    def colision_moneda(self, personaje):
        """Detecta colisión entre un personaje y una moneda."""
        # Calcula la posición del personaje en coordenadas de celda
        pos_pacman = ((personaje.x + 8)//16, (personaje.y + 8)//16)
        
        # Verifica cada moneda en la lista
        for moneda in self.lista_monedas[:]:  # Usa una copia para evitar problemas al modificar
            x, y, tipo = moneda
            if pos_pacman == (x, y):  # Si hay colisión
                self.lista_monedas.remove(moneda)  # Elimina la moneda
                self.monedas_eliminadas += 1  # Incrementa contador
                return tipo  # Devuelve el tipo de moneda (0: normal, 1: poder, 2: fruta)
        return -1  # No hay colisión
