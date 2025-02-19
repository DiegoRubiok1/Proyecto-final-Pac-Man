"""
Created by Diego Rubio Canales in nov 2024
Universidad Carlos III de Madrid
"""
import pyxel
from personaje import Personaje
from constantes import *



class Tablero:

    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height

        #Personajes:
        self.pacman = Personaje(32, 32,
                                PACMAN_ANIMATION, 2)
        self.blinky = Personaje(BLINKY_INICIALX, BLINKY_INICIALY,
                                BLINKY_ANIMATION, 1 )

        #inicializo pyxel
        pyxel.init(self.width, self.height, title="Pacman movimiento")
        #cargar imagenes
        pyxel.load("assets/tileset.pyxres")
        #pyxel.image(1).load(0, 0, "assets/map_pacman.png")
        #empezar el juego
        pyxel.run(self.update, self.draw)

#-----------------------------------getters------------------------------------

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, value):
        # Valida que el ancho sea un entero positivo
        if value < 0 or not isinstance(value, int):
            raise ValueError("El ancho debe ser un entero positivo.")
        self.__width = value

    @property
    def height(self) -> int:
        return self.__height

#----------------------------------setters-------------------------------------

    @width.setter
    def width(self, width):
        if width < 0:
            raise ValueError("El width debe sel mayor que 0")
        elif type(width) != int:
            raise TypeError("El valor de width debe ser entero:" + str(type(
                width)))
        else:
            self.__width = width

    @height.setter
    def height(self, height):
        if height < 0:
            raise ValueError("El width debe sel mayor que 0")
        elif type(height) != int:
            raise TypeError("El valor de height debe ser entero:" + str(type(
                height)))
        else:
            self.__height = height

#-----------------------------------update-------------------------------------

    def update(self):
        # Calcular si la boca está cerrada (0) o abierta (1)
        if pyxel.frame_count % FREC_ANIMACION == 0:
            self.pacman.sprite_actual = (self.pacman.sprite_actual + 1) % 4
        #Control del objeto pacman:
        if pyxel.btnp(pyxel.KEY_P):
            quit
        elif pyxel.btn(pyxel.KEY_D):
            self.pacman.mov("right")
        elif pyxel.btn(pyxel.KEY_W):
            self.pacman.mov("up")
        elif pyxel.btn(pyxel.KEY_A):
            self.pacman.mov("left")
        elif pyxel.btn(pyxel.KEY_S):
            self.pacman.mov("down")

        if self.pacman.x // 16 == self.blinky.x // 16 and (
                self.blinky.colision("up") or self.blinky.colision("down")):
            if self.blinky.last_direction == 1:
                self.blinky.mov("left")
            else:
                self.blinky.mov("right")
        else:
            self.blinky.perseguir(self.pacman)

#-----------------------------------draw---------------------------------------

    def draw(self):
        pyxel.cls(0)
        for (x,y) in MUROS:
            pyxel.rect((x - 1) * 16, (y - 1) * 16, 16, 16, 50)
        self.draw_pacman()
        self.draw_blinky()


    def draw_pacman(self):
        if pyxel.btn(pyxel.KEY_D):
            pyxel.blt(self.pacman.x - ANCHO_PACMAN, self.pacman.y - ANCHO_PACMAN,
                      *self.pacman.sprite[0][self.pacman.sprite_actual])
            self.pacman.last_direction = 0
        elif pyxel.btn(pyxel.KEY_A):
            pyxel.blt(self.pacman.x - ANCHO_PACMAN, self.pacman.y - ALTO_PACMAN,
                      *self.pacman.sprite[1][self.pacman.sprite_actual])
            self.pacman.last_direction = 1
        elif pyxel.btn(pyxel.KEY_W):
            pyxel.blt(self.pacman.x - ANCHO_PACMAN, self.pacman.y - ALTO_PACMAN,
                      *self.pacman.sprite[2][self.pacman.sprite_actual])
            self.pacman.last_direction = 2
        elif pyxel.btn(pyxel.KEY_S):
            pyxel.blt(self.pacman.x - ANCHO_PACMAN, self.pacman.y - ALTO_PACMAN,
                      *self.pacman.sprite[3][self.pacman.sprite_actual])
            self.pacman.last_direction = 3
        else:
            pyxel.blt(self.pacman.x - ANCHO_PACMAN, self.pacman.y - ALTO_PACMAN,
                  *self.pacman.sprite[self.pacman.last_direction][0])
    def draw_blinky(self):
        pyxel.blt(self.blinky.x - ANCHO_BLINKY, self.blinky.y - ALTO_BLINKY,
                      *self.blinky.sprite[self.blinky.last_direction])