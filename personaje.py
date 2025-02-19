"""
Created by Diego Rubio Canales in nov 2024
Universidad Carlos III de Madrid
"""

from constantes import *

class Personaje:
    def __init__(self, x: int, y: int, sprite: tuple, vel: int, vidas: int,
                 muros: list, tiempo_activacion: int):
        # Atributos cinemáticos
        self.x = x  # Posición x en el tablero
        self.y = y  # Posición y en el tablero
        self.vel = vel  # Velocidad de movimiento
        self.sprite = sprite  # Conjunto de sprites para animación
        self.nueva_x = self.x + self.vel  # Próxima posición x
        self.nueva_y = self.y + self.vel  # Próxima posición y
        self.vidas = vidas  # Número de vidas
        self.direccion_actual = None  # Dirección en la que se mueve
        self.lista_muros = muros  # Lista de muros para colisiones

        # Estado del personaje
        self.cazar = False  # Modo poder activo
        self.last_direction = 0  # 0: derecha, 1: izquierda, 2: arriba, 3: abajo
        self.sprite_actual = 1  # Índice del sprite actual (ciclo de animación)
        self.fuera_caja = False  # Si el fantasma está fuera de su caja inicial
        self.comportamiento = 0  # Para fantasmas: 0 perseguir/emboscar, 1 huir
        
        # Variables temporales
        self.t_activacion = tiempo_activacion  # Tiempo antes de activarse

    # Método auxiliar para validaciones
    @staticmethod
    def _validate_int(value, name):
        """Valida que un valor sea entero"""
        if not isinstance(value, int):
            raise TypeError(str(name) + " debe ser un entero: " + str(type(
                value)))
        return value

    # Properties para validar atributos
    @property
    def nueva_x(self) -> int:
        return self.__nueva_x

    @nueva_x.setter
    def nueva_x(self, value: int):
        self.__nueva_x = self._validate_int(value, "nueva_x")

    @property
    def nueva_y(self) -> int:
        return self.__nueva_y

    @nueva_y.setter
    def nueva_y(self, value: int):
        self.__nueva_y = self._validate_int(value, "nueva_y")

    @property
    def vidas(self) -> int:
        return self.__vidas

    @vidas.setter
    def vidas(self, value: int):
        self.__vidas = self._validate_int(value, "vidas")

    @property
    def direccion_actual(self):
        return self.__direccion_actual

    @direccion_actual.setter
    def direccion_actual(self, value):
        self.__direccion_actual = value

    @property
    def lista_muros(self) -> list:
        return self.__lista_muros

    @lista_muros.setter
    def lista_muros(self, value: list):
        if not isinstance(value, list):
            raise TypeError("lista_muros debe ser una lista")
        self.__lista_muros = value

    @property
    def cazar(self) -> bool:
        return self.__cazar

    @cazar.setter
    def cazar(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("cazar debe ser un booleano")
        self.__cazar = value

    @property
    def last_direction(self) -> int:
        return self.__last_direction

    @last_direction.setter
    def last_direction(self, value: int):
        self.__last_direction = self._validate_int(value, "last_direction")

    @property
    def sprite_actual(self) -> int:
        return self.__sprite_actual

    @sprite_actual.setter
    def sprite_actual(self, value: int):
        self.__sprite_actual = self._validate_int(value, "sprite_actual")

    @property
    def fuera_caja(self) -> bool:
        return self.__fuera_caja

    @fuera_caja.setter
    def fuera_caja(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("fuera_caja debe ser un booleano")
        self.__fuera_caja = value

    @property
    def comportamiento(self) -> int:
        return self.__comportamiento

    @comportamiento.setter
    def comportamiento(self, value: int):
        self.__comportamiento = self._validate_int(value, "comportamiento")

    @property
    def t_activacion(self) -> int:
        return self.__t_activacion

    @t_activacion.setter
    def t_activacion(self, value: int):
        self.__t_activacion = self._validate_int(value, "t_activacion")


    def mov(self, direccion: str, colision: bool):
        """Movimiento de personajes con verificación de colisión."""
        #Aparecer al otro lado de la pantalla si se atraviesa
        if self.x - ANCHO_PACMAN > WIDTH:
            self.x = self.x - WIDTH - ANCHO_PACMAN
        elif self.x < 0:
            self.x = WIDTH + ALTO_PACMAN
        elif self.y > WIDTH + ALTO_PACMAN:
            self.y = 0
        elif self.y < 0:
            self.y = WIDTH + ALTO_PACMAN

        #definir movimiento
        if colision:  # Si se activan las colisiones
            # Solo mueve si no hay colisión en la dirección deseada
            if direccion == "up" and not self.colision("up"):
                self.y -= self.vel
                self.last_direction = 2 #Cambia la ultima dirección hacia arriba
            elif direccion == "down" and not self.colision("down"):
                self.y += self.vel
                self.last_direction = 3 #Cambia la ultima dirección hacia abajo
            elif direccion == "right" and not self.colision("right"):
                self.x += self.vel
                self.last_direction = 0 #Cambia la ultima dirección hacia derecha
            elif direccion == "left" and not self.colision("left"):
                self.x -= self.vel
                self.last_direction = 1 #Cambia la ultima dirección hacia izquierda
        else:  # Si no hay colisiones, mueve libremente
            if direccion == "up":
                self.y -= self.vel
                self.last_direction = 2 #Cambia la ultima dirección hacia arriba
            elif direccion == "down":
                self.y += self.vel
                self.last_direction = 3 #Cambia la ultima dirección hacia abajo
            elif direccion == "right":
                self.x += self.vel
                self.last_direction = 0 #Cambia la ultima dirección hacia derecha
            elif direccion == "left":
                self.x -= self.vel
                self.last_direction = 1 #Cambia la ultima dirección hacia izquierda

    def colision(self, direccion):
        """Detección de colisión en cada posible dirección del personaje."""
        nueva_x, nueva_y = self.x, self.y

        #Calcular las futuras celdas si personaje se moviera en cada dirección
        if direccion == "up":
            nueva_y -= self.vel
        elif direccion == "down":
            nueva_y += self.vel
        elif direccion == "left":
            nueva_x -= self.vel
        elif direccion == "right":
            nueva_x += self.vel

        # Guarda las futuras celdas ocupadas por personaje
        celdas_ocupadas = (
            (nueva_x // 16, nueva_y // 16),  # Esquina superior izquierda
            ((nueva_x + 15) // 16, nueva_y // 16),  # Esquina superior derecha
            (nueva_x // 16, (nueva_y + 15) // 16), # Esquina inferior izquierda
            ((nueva_x + 15) // 16, (nueva_y + 15) // 16)# Esquina inferior derecha
        )

        # Verificar si alguna futura celda que pueda ocupar está en los muros
        for celda in celdas_ocupadas:
            for i in range(len(self.lista_muros)):
                if (self.lista_muros[i][0], self.lista_muros[i][1]) == celda:
                    return True
        return False

    def colision_personaje(self, personaje):
        """Detecta si hay colisión con otro personaje"""
        if abs(self.x - personaje.x) < 8 and abs(self.y - personaje.y) < 8:
            return True
        return False

    def huir(self, personaje):

        nuevas_celdas = []
        celdas_pacman = (personaje.x // 16, personaje.y // 16)
        dist_x = 0
        dist_y = 0
        prox_celda = (0, 0)
        # Guardar celda en posibles futuras celdas si no hay colisión en esa
        # dirección y además se limitan los cambios de dirección a priori.
        if not self.colision("up") and self.last_direction != 3:
            nuevas_celdas.append((self.x // 16, (self.y // 16 - 1)))
        if not self.colision("down") and self.last_direction != 2:
            nuevas_celdas.append((self.x // 16, (self.y // 16 + 1)))
        if not self.colision("right") and self.last_direction != 1:
            nuevas_celdas.append(((self.x // 16) + 1, self.y // 16))
        if not self.colision("left") and self.last_direction != 0:
            nuevas_celdas.append(((self.x // 16) - 1, self.y // 16))
        # Seleccionamos la nueva celda que aumente la distancia al objetivo
        for celda in nuevas_celdas:
            nueva_dist_x = celdas_pacman[0] - celda[0]
            nueva_dist_y = celdas_pacman[1] - celda[1]
            # Cuenta el número total de celdas al objetivo en la posible
            # dirección y si es menor que el anterior, lo cambia
            if abs(nueva_dist_x) + abs(nueva_dist_y) > abs(dist_x) + abs(
                    dist_y):
                dist_x = nueva_dist_x
                dist_y = nueva_dist_y
                prox_celda = celda
        # compara el valor de la celda objetivo para determinar la dirección
        if prox_celda == (self.x // 16, (self.y // 16 - 1)):
            self.mov("up", True)
        elif prox_celda == (self.x // 16, (self.y // 16 + 1)):
            self.mov("down", True)
        elif prox_celda == ((self.x // 16) + 1, self.y // 16):
            self.mov("right", True)
        elif prox_celda == ((self.x // 16) - 1, self.y // 16):
            self.mov("left", True)
        # en el caso en el que no haya celdas en la lista indica que el único
        # movimiento posible es un cambio de dirección, ahora lo permitimos:
        else:
            if self.colision("right"):
                self.mov("left", True)
            elif self.colision("left"):
                self.mov("right", True)
            elif self.colision("up"):
                self.mov("down", True)
            else:
                self.mov("up", True)



    def perseguir(self, x, y):
        """Persecución de personaje sobre unas coordenadas."""
        nuevas_celdas = []
        celdas_pacman = (x // 16, y // 16)
        dist_x = 500
        dist_y = 500
        prox_celda = (0, 0)
        #Guardar celda en posibles futuras celdas si no hay colisión en esa
        #dirección y además se limitan los cambios de dirección a priori.
        if not self.colision("right") and self.last_direction != 1:
            nuevas_celdas.append(((self.x // 16) + 1, self.y // 16))
        if not self.colision("left") and self.last_direction != 0:
            nuevas_celdas.append(((self.x // 16) - 1, self.y // 16))
        if not self.colision("up") and self.last_direction != 3:
            nuevas_celdas.append((self.x // 16, (self.y // 16 - 1)))
        if not self.colision("down") and self.last_direction != 2:
            nuevas_celdas.append((self.x // 16, (self.y // 16 + 1)))

        #Seleccionamos la nueva celda que minimice la distancia al objetivo
        for celda in nuevas_celdas:
            nueva_dist_x = celdas_pacman[0] - celda[0]
            nueva_dist_y = celdas_pacman[1] - celda[1]
            #Cuebta el número total de celdas al objetivo en la posible
            #dirección y si es menor que el anterior, lo cambia
            if abs(nueva_dist_x) + abs(nueva_dist_y) < abs(dist_x) + abs(dist_y):
                dist_x = nueva_dist_x
                dist_y = nueva_dist_y
                prox_celda = celda
        #compara el valor de la celda objetivo para determinar la dirección
        if prox_celda == (self.x // 16, (self.y // 16 - 1)):
            self.mov("up", True)
        elif prox_celda == (self.x // 16, (self.y // 16 + 1)):
            self.mov("down", True)
        elif prox_celda == ((self.x // 16) + 1, self.y // 16):
            self.mov("right", True)
        elif prox_celda == ((self.x // 16) - 1, self.y // 16):
            self.mov("left", True)
            #en el caso en el que no haya celdas en la lista indica que el único
            #movimiento posible es un cambio de dirección, ahora lo permitimos:
        else:
            if self.colision("right"):
                self.mov("left", True)
            elif self.colision("left"):
                self.mov("right", True)
            elif self.colision("up"):
                self.mov("down", True)
            else:
                self.mov("up", True)
    def emboscar(self, personaje):
        #persuigue a una distancia determinada de donde mira personaje
        if personaje.last_direction == 0:
            self.perseguir(personaje.x + DIST_OBJETIVO,personaje.y)
        elif personaje.last_direction == 1:
            self.perseguir(personaje.x - DIST_OBJETIVO, personaje.y)
        elif personaje.last_direction == 2:
            self.perseguir(personaje.x, personaje.y - DIST_OBJETIVO)
        elif personaje.last_direction == 3:
            self.perseguir(personaje.x, personaje.y + DIST_OBJETIVO)
    def salir_caja(self):
        #Movimiento en el eje x:
        self.vel = 1
        if self.x - 9*16> 0:
            self.mov("left", False)
        elif self.x - 9*16 < 0:
            self.mov("right", False)
        elif self.y - 8*16 > 0:
            self.mov("up", False)
        else:
            self.fuera_caja = True
            self.vel = 2


