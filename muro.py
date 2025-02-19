"""
Created by Diego Rubio Canales in dic 2024
Universidad Carlos III de Madrid
"""
from constantes import *

class Muro:
    def __init__(self, nivel: int):
        # Inicializa los muros con el nivel 1 por defecto
        self.lista_muros = MUROS_1  # Lista de coordenadas y tipos de muros
        self.nivel = nivel  # Nivel actual del juego

    # Property para lista_muros
    @property
    def lista_muros(self):
        return self.__lista_muros

    @lista_muros.setter
    def lista_muros(self, value):
        # Verifica que el valor sea una lista
        if type(value) != list: 
            raise TypeError("la lista de muros debe ser una lista")
        self.__lista_muros = value

    # Property para nivel
    @property
    def nivel(self):
        return self.__nivel

    @nivel.setter
    def nivel(self, value):
        # Verifica que el nivel sea un entero
        if type(value) != int:
            raise TypeError("El nivel debe ser un entero")
        self.__nivel = value
