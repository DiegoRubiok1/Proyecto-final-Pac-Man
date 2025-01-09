"""
Created by Diego Rubio Canales in nov 2024
Universidad Carlos III de Madrid
"""
import muro
from constantes import *
import pyxel

class Personaje:
    def __init__(self, x: int, y: int, sprite: tuple, vel: int):
        # Atributos cinemáticos
        self.x = x
        self.y = y
        self.vel = vel
        self.sprite = sprite
        self.nueva_x = self.x + self.vel
        self.nueva_y = self.y + self.vel

        # Estado del personaje
        self.last_direction = 0  # 0: derecha, 1: izquierda, 2: arriba, 3: abajo
        self.sprite_actual = 1  # Boca abierta o cerrada


    # Metodo auxiliar para validaciones
    def _validate_int(self, value, name, min_value=0):
        if not isinstance(value, int):
            raise TypeError(str(name) + " debe ser un entero: " + str(type(
                value)))
        if value <= min_value:
            raise ValueError(str(name) + " debe ser mayor o igual a " + str(
                min_value))
        return value

    # Propiedades
    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, value: int):
        if value - ANCHO_PACMAN > WIDTH:
            self.__x = value - WIDTH - ANCHO_PACMAN
        elif value < 0:
            self.__x = WIDTH + ANCHO_PACMAN
        else:
            self.__x = value
    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, value: int):
        self.__y = self._validate_int(value, "y")

    @property
    def vel(self) -> int:
        return self.__vel

    @vel.setter
    def vel(self, value: int):
        self.__vel = self._validate_int(value, "vel", min_value=-1)


    def mov(self, direccion: str):
        """Movimiento de Pacman con verificación de colisión."""
        if direccion == "up" and not self.colision("up"):
            self.y -= self.vel
            return True
        elif direccion == "down" and not self.colision("down"):
            self.y += self.vel
            return True
        elif direccion == "right" and not self.colision("right"):
            self.x += self.vel
            return True
        elif direccion == "left" and not self.colision("left"):
            self.x -= self.vel
            return True
        return False

    def colision(self, direccion):
        nueva_x, nueva_y = self.x, self.y
        if direccion == "up":
            nueva_y -= self.vel
        elif direccion == "down":
            nueva_y += self.vel
        elif direccion == "left":
            nueva_x -= self.vel
        elif direccion == "right":
            nueva_x += self.vel

        # Calcular celdas ocupadas
        celdas_ocupadas = (
            (nueva_x // 16, nueva_y // 16),  # Esquina superior izquierda
            ((nueva_x + 15) // 16, nueva_y // 16),  # Esquina superior derecha
            (nueva_x // 16, (nueva_y + 15) // 16),
            # Esquina inferior izquierda
            ((nueva_x + 15) // 16, (nueva_y + 15) // 16)
            # Esquina inferior derecha
        )

        print(f"Dirección: {direccion}, Celdas ocupadas: {celdas_ocupadas}")

        # Verificar si alguna celda está en los muros
        for celda in celdas_ocupadas:
            if celda in MUROS:
                return True
        return False

    def perseguir(self, otro_personaje):
        dist_x = otro_personaje.x - self.x
        dist_y = otro_personaje.y - self.y

        moved = False
        if abs(dist_x) >= abs(dist_y):  # Priorizar eje X
            if dist_x > 0 and not self.colision("right"):
                moved = self.mov("right")
            elif dist_x < 0 and not self.colision("left"):
                moved = self.mov("left")
            elif dist_y > 0 and not self.colision("down"):
                moved = self.mov("down")
            elif dist_y < 0 and not self.colision("up"):
                moved = self.mov("up")
        else:  # Priorizar eje Y
            if dist_y > 0 and not self.colision("down"):
                moved = self.mov("down")
            elif dist_y < 0 and not self.colision("up"):
                moved = self.mov("up")
            elif dist_x > 0 and not self.colision("right"):
                moved = self.mov("right")
            elif dist_x < 0 and not self.colision("left"):
                moved = self.mov("left")
        return moved