"""
Created by Diego Rubio Canales in dic 2024
Universidad Carlos III de Madrid
"""
import random
from time import time
import pyxel
from pyxel.pyxel_wrapper import *
from personaje import Personaje
from constantes import *
from muro import Muro
from objeto import Objeto

class Tablero:
    """
    Clase que gestiona el tablero del juego, incluyendo personajes,
    __muros, __monedas y la lógica principal de actualización y dibujo.
    """

    def __init__(self, width: int, height: int):
        # Dimensiones del tablero
        self.width = width
        self.height = height

        # Inicialización de elementos del juego
        self.__muros = Muro(1)  # Crea los muros del nivel 1

        # Creación de personajes principales con sus posiciones iniciales y características
        self.__pacman = Personaje(PACMAN_INICIAL_X, PACMAN_INICIAL_Y,
                                  PACMAN_ANIMATION, 2, 4,
                                  self.__muros.lista_muros, 0)
        self.__blinky = Personaje(BLINKY_INICIAL_X, BLINKY_INICIAL_Y,
                                  BLINKY_ANIMATION, 2, 1,
                                  self.__muros.lista_muros, 0)
        self.__pinky = Personaje(PINKY_INICIAL_X, PINKY_INICIAL_Y,
                                 PINKY_ANIMATION, 2, 1,
                                 self.__muros.lista_muros, 3)
        self.__clyde = Personaje(CLYDE_INICIAL_X, CLYDE_INICIAL_Y,
                                 CLYDE_ANIMATION, 2, 1,
                                 self.__muros.lista_muros, 6)
        self.__inky = Personaje(INKY_INICIAL_X, INKY_INICIAL_Y,
                                INKY_ANIMATION, 2, 1,
                                self.__muros.lista_muros, 9)

        # Variables de control del juego
        self.__tiempo_inicio = time()  # Tiempo de inicio del juego
        self.__fantasmas_liberados = False  # Control de liberación de fantasmas
        self.__tiempo_espera = 5  # Tiempo antes de liberar fantasmas
        self.__t_pastilla_comida = 0  # Tiempo desde última pastilla comida
        self.__t_caza = 10  # Duración del modo "cazar"
        self.__puntos = 0  # Puntuación del jugador

        # Inicialización de monedas en el tablero
        self.__monedas = Objeto(self.__muros.lista_muros, pastillas= 6)

        # Configuración inicial de Pyxel
        pyxel.init(self.width, self.height, title="Pacman movimiento")
        pyxel.load("assets/tileset.pyxres")  # Carga recursos gráficos
        pyxel.images[1].load(0, 0, "assets/pantalla_start.png")
        pyxel.images[2].load(0, 0, "assets/caracteres.png")
        pyxel.run(self.update, self.draw)  # Inicia el bucle del juego

    # Propiedades para validar dimensiones del tablero
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

    @height.setter
    def height(self, value):
        # Valida que la altura sea un entero positivo
        if value < 0 or not isinstance(value, int):
            raise ValueError("La altura debe ser un entero positivo.")
        self.__height = value

    # --------------------------------- Lógica del juego ---------------------------------
    def update(self):
        """Actualiza el estado del juego en cada frame."""
        # Si pacman tiene 4 vidas, estamos en la pantalla inicial
        if self.__pacman.vidas == 4:
            self._gestionar_inicio()
        # Si tiene entre 1-3 vidas, el juego está activo
        elif self.__pacman.vidas > 0:
            self._gestionar_juego_activo()
        # Si no tiene vidas, reinicia el juego
        else:
            self._reiniciar_juego()

    def _gestionar_inicio(self):
        """Gestión del estado inicial del juego."""
        # Al presionar espacio, inicia el juego
        if pyxel.btn(KEY_SPACE):
            # Configura el primer nivel
            self.__muros.nivel = 1
            self.__muros.lista_muros = MUROS_1.copy()
            self.__tiempo_inicio = time()
            self.__pacman.vidas = 3
            # Inicializa las monedas del nivel
            self.__monedas.lista_monedas = self.__monedas.cargar_monedas(self.__muros.lista_muros)
            self.__monedas.numero_inicial = len(self.__monedas.lista_monedas)
            self.__monedas.monedas_eliminadas = 0

    def _gestionar_juego_activo(self):
        """Lógica principal del juego cuando está activo."""
        # Verifica si los fantasmas están aún en la jaula
        if not self.__fantasmas_liberados:
            self._liberacion_fantasmas()
        else:
            self._actualizar_elementos_juego()

    def _liberacion_fantasmas(self):
        """Libera los fantasmas tras un tiempo de espera."""
        # Comprueba si ha pasado el tiempo de espera
        if time() - self.__tiempo_inicio >= self.__tiempo_espera:
            self.__fantasmas_liberados = True
            # Reposiciona todos los personajes a sus posiciones iniciales
            self.__blinky.x, self.__blinky.y = BLINKY_INICIAL_X, BLINKY_INICIAL_Y
            self.__pinky.x, self.__pinky.y = PINKY_INICIAL_X, PINKY_INICIAL_Y
            self.__inky.x, self.__inky.y = INKY_INICIAL_X, INKY_INICIAL_Y
            self.__clyde.x, self.__clyde.y = CLYDE_INICIAL_X, CLYDE_INICIAL_Y
            self.__pacman.x, self.__pacman.y = PACMAN_INICIAL_X, PACMAN_INICIAL_Y
            self.__tiempo_inicio = time()
        else:
            # Mantiene a los fantasmas en posiciones fijas dentro de la jaula
            self.__blinky.x, self.__blinky.y = 144, 160
            self.__pinky.x, self.__pinky.y = 128, 160
            self.__clyde.x, self.__clyde.y = 160, 160
            self.__inky.x, self.__inky.y = 144, 160

    def _actualizar_elementos_juego(self):
        """Actualiza el estado de los personajes y objetos en el juego."""
        # Verifica si se han recogido todas las monedas para cambiar de nivel
        if self.__monedas.monedas_eliminadas == self.__monedas.numero_inicial:
            self._cambiar_nivel()

        # Gestiona el estado de poder de Pac-man (modo cazar)
        if time() >= self.__t_pastilla_comida + T_CAZA:
            self.__pacman.cazar = False
            
        # Gestiona la aparición de frutas y movimiento de personajes
        self._aparicion_fruta()
        self._mover_pacman()
        
        # Determina el comportamiento de los fantasmas según el estado de Pac-man
        if self.__pacman.cazar:
            self._fantasmas_huir()
        else:
            self._perseguir_pacman()

        # Gestiona colisiones y actualiza animaciones
        self._gestionar_colisiones()
        self._actualizar_animaciones()

    def _aparicion_fruta(self):
        # Cada 1000 frames, convierte una moneda normal en una fruta con un
        # 50%  de probabilidad  (tipo 2)
        if pyxel.frame_count % 1000 == 0:
            if random.randint(0,2) == 0 or 1:
                (x, y, tipo) = random.choice(self.__monedas.lista_monedas)
                self.__monedas.lista_monedas.remove((x, y, tipo))
                self.__monedas.lista_monedas.append((x, y, 2))

    def _mover_pacman(self):
        # Verifica las teclas presionadas y actualiza la dirección si no hay
        # colisión
        if pyxel.btn(KEY_W) and not self.__pacman.colision("up"):
            self.__pacman.direccion_actual = "up"
        if pyxel.btn(KEY_S) and not self.__pacman.colision("down"):
            self.__pacman.direccion_actual = "down"
        if pyxel.btn(KEY_D) and not self.__pacman.colision("right"):
            self.__pacman.direccion_actual = "right"
        if pyxel.btn(KEY_A) and not self.__pacman.colision("left"):
            self.__pacman.direccion_actual = "left"
        # Mueve a Pacman en la dirección actual con colisiones activadas
        self.__pacman.mov(self.__pacman.direccion_actual, True)

    def _perseguir_pacman(self):
        """Lógica de persecución de Pacman por los fantasmas."""
        # Blinky siempre persigue directamente
        self.__blinky.perseguir(self.__pacman.x, self.__pacman.y)

        # Cada fantasma tiene su comportamiento específico
        self._pinky_comportamiento()
        self._clyde_comportamiento()
        self._inky_comportamiento()

    def _pinky_comportamiento(self):
        # Si Pinky está dentro de la caja, verifica si debe salir
        if not self.__pinky.fuera_caja:
            if time() >= self.__tiempo_inicio + self.__pinky.t_activacion:
                self.__pinky.salir_caja()
        # Si está cerca de Pacman, lo persigue directamente
        elif (abs(self.__pinky.x - self.__pacman.x) < DIST_OBJETIVO and 
              abs(self.__pinky.y - self.__pacman.y) < DIST_OBJETIVO):
            self.__pinky.perseguir(self.__pacman.x, self.__pacman.y)
        else:  # Si no está cerca, intenta emboscarlo
            self.__pinky.emboscar(self.__pacman)

    def _clyde_comportamiento(self):
        # Si Clyde está en la caja, verifica si debe salir
        if not self.__clyde.fuera_caja:
            if time() >= self.__tiempo_inicio + self.__clyde.t_activacion:
                self.__clyde.salir_caja()
        else:
            # Cambia aleatoriamente su comportamiento
            cambio_actitud = random.randint(100, 500)
            if pyxel.frame_count % cambio_actitud == 0:
                self.__clyde.comportamiento = (self.__clyde.comportamiento + 1) % 2
            # perseguir directamente a una distancia, si no emboscar
            if self.__clyde.comportamiento == 1:
                if (abs(self.__clyde.x - self.__pacman.x) < DIST_OBJETIVO and abs(
                        self.__clyde.y - self.__pacman.y) < DIST_OBJETIVO):
                    self.__clyde.perseguir(self.__pacman.x, self.__pacman.y)
                else:  # Si no embosca
                    self.__clyde.emboscar(self.__pacman)
            #si comportamiento es 0, huye
            else:
                self.__clyde.huir(self.__pacman)

    def _inky_comportamiento(self):
        # Si Inky está en la caja, verifica si debe salir
        if not self.__inky.fuera_caja:
            if time() >= self.__tiempo_inicio + self.__inky.t_activacion:
                self.__inky.salir_caja()
        else:
            # Cambia aleatoriamente su comportamiento
            cambio_actitud = random.randint(100, 500)
            if pyxel.frame_count % cambio_actitud == 0:
                self.__inky.comportamiento = (self.__inky.comportamiento + 1) % 2
            # Si comportamiento es 1 persigue, si es 0 huye
            if self.__inky.comportamiento == 1:
                self.__inky.perseguir(self.__pacman.x, self.__pacman.y)
            else:
                self.__inky.huir(self.__pacman)

    def _fantasmas_huir(self):
        """Fantasmas huyen de Pacman."""
        self.__blinky.huir(self.__pacman)
        self.__pinky.huir(self.__pacman)
        self.__clyde.huir(self.__pacman)
        self.__inky.huir(self.__pacman)

    def _gestionar_colisiones(self):
        """Detecta colisiones entre Pacman, fantasmas y __monedas."""
        self._colision_moneda()
        if self.__pacman.cazar:
            self._colision_fantasma()
        else:
            if (self.__blinky.colision_personaje(self.__pacman) or
                    self.__pinky.colision_personaje(self.__pacman) or
                    self.__clyde.colision_personaje(self.__pacman) or
                    self.__inky.colision_personaje(self.__pacman)):
                self.__pacman.vidas -= 1
                if self.__puntos > 10: self.__puntos -= 10
                else: self.__puntos = 0
                self._reiniciar_personajes()

    def _colision_moneda(self):
        # Verifica si Pacman colisiona con alguna moneda y devuelve el tipo
        tipo_colision = self.__monedas.colision_moneda(self.__pacman)
        if tipo_colision != -1:
            self.__puntos += 1  # Punto base por cualquier moneda
            if tipo_colision == 1:  # Si es una pastilla de poder
                self.__pacman.cazar = True
                self.__t_pastilla_comida = time()
            elif tipo_colision == 2:  # Si es una fruta
                self.__puntos += 19  # Puntos extra por fruta

    def _colision_fantasma(self):
         if self.__pacman.cazar:
             # Si colisiona con Blinky
             if self.__blinky.colision_personaje(self.__pacman):
                 self.__blinky.x, self.__blinky.y = (BLINKY_INICIAL_X,
                                                     BLINKY_INICIAL_Y)
                 self.__puntos += 10
             # Si colisiona con Pinky
             if self.__pinky.colision_personaje(self.__pacman):
                 self.__pinky.x, self.__pinky.y = PINKY_INICIAL_X, PINKY_INICIAL_Y
                 self.__puntos += 10
                 self.__pinky.fuera_caja = False
             # Si colisiona con Clyde
             if self.__clyde.colision_personaje(self.__pacman):
                self.__clyde.x, self.__clyde.y = CLYDE_INICIAL_X, CLYDE_INICIAL_Y
                self.__puntos += 10
                self.__clyde.fuera_caja = False
             # Si colisiona con Inky
             if self.__inky.colision_personaje(self.__pacman):
                self.__inky.x, self.__inky.y = INKY_INICIAL_X, INKY_INICIAL_Y
                self.__puntos += 10
                self.__inky.fuera_caja = False

    def _reiniciar_personajes(self):
        """Restablece posiciones de los personajes y reduce una vida de Pacman,
        también devuelve el estado de los fantasmas a dentro de la caja y
        reinicia el tiempo"""
        # Reposiciona a Pacman y los fantasmas
        self.__pacman.x = self.__blinky.x = self.__pinky.x = PACMAN_INICIAL_X
        self.__pacman.y = PACMAN_INICIAL_Y
        self.__blinky.y = BLINKY_INICIAL_Y
        self.__pinky.y = PINKY_INICIAL_Y
        self.__clyde.x, self.__clyde.y = CLYDE_INICIAL_X, CLYDE_INICIAL_Y
        self.__inky.x, self.__inky.y = INKY_INICIAL_X, INKY_INICIAL_Y
        
        # Reinicia estados del juego
        self.__pacman.cazar = False
        self.__pinky.fuera_caja = False
        self.__inky.fuera_caja = False
        self.__clyde.fuera_caja = False
        self.__fantasmas_liberados = False
        self.__tiempo_inicio = time()

    def _actualizar_animaciones(self):
        """Actualiza los sprites de animación en cada frame."""
        if pyxel.frame_count % FREC_ANIMACION == 0:
            # Actualiza el sprite actual de cada personaje
            self.__pacman.sprite_actual = (self.__pacman.sprite_actual + 1) % 4
            self.__blinky.sprite_actual = (self.__blinky.sprite_actual + 1) % 2
            self.__pinky.sprite_actual = (self.__blinky.sprite_actual + 1) % 2
            self.__clyde.sprite_actual = (self.__clyde.sprite_actual + 1) % 2
            self.__inky.sprite_actual = (self.__inky.sprite_actual + 1) % 2

    def _cambiar_nivel(self):
        """Cambia al siguiente nivel del juego."""
        # Incrementa el nivel y reinicia posiciones
        self.__muros.nivel = self.__muros.nivel + 1
        self._reiniciar_personajes()
        
        # Configura el nivel 1
        if self.__muros.nivel == 1:
            self.__monedas.pastillas = 6
            # Carga los muros en todos los objetos del juego
            self.__muros.lista_muros = self.__pacman.lista_muros = (
                self.__blinky).lista_muros = self.__pinky.lista_muros = (
                self.__clyde).lista_muros = self.__inky.lista_muros = MUROS_1
            self.__monedas.lista_monedas = self.__monedas.cargar_monedas(MUROS_1)
            
        # Configura el nivel 2
        elif self.__muros.nivel == 2:
            self.__monedas.pastillas = 3
            self.__muros.lista_muros = self.__pacman.lista_muros = (
                self.__blinky).lista_muros = self.__pinky.lista_muros = (
                self.__clyde).lista_muros = self.__inky.lista_muros = MUROS_2
            self.__monedas.lista_monedas = self.__monedas.cargar_monedas(MUROS_2)
            
        # Configura el nivel 3
        elif self.__muros.nivel == 3:
            self.__monedas.pastillas = 2
            self.__muros.lista_muros = self.__pacman.lista_muros = (
                self.__blinky).lista_muros = self.__pinky.lista_muros = (
                self.__clyde).lista_muros = self.__inky.lista_muros = MUROS_3
            self.__monedas.lista_monedas = self.__monedas.cargar_monedas(MUROS_3)
        else:
            self._reiniciar_juego()
            
        # Reinicia contadores de monedas
        self.__monedas.numero_inicial = len(self.__monedas.lista_monedas)
        self.__monedas.monedas_eliminadas = 0

    def _reiniciar_juego(self):
        """Reinicia el estado del juego al nivel inicial."""
        self.__pacman.vidas = 4  # Vuelve a la pantalla de inicio
        self.__puntos = 0  # Reinicia puntuación
        self.__muros.nivel = 0  # Reinicia nivel
        self._cambiar_nivel()  # Configura el primer nivel
        # Reinicia las monedas
        self.__monedas.lista_monedas = self.__monedas.cargar_monedas(
            self.__muros.lista_muros)
        self.__monedas.numero_inicial = len(self.__monedas.lista_monedas)
        self.__monedas.numero_inicial = 0

    # --------------------------------- Dibujo del juego ---------------------------------
    def draw(self):
        """Dibuja el estado actual del juego en pantalla."""
        pyxel.cls(0)  # Limpia la pantalla
        if self.__pacman.vidas == 4:
            self._dibujar_pantalla_inicio()
        elif self.__pacman.vidas > 0:
            self._dibujar_elementos_juego()

    def _dibujar_pantalla_inicio(self):
        """Dibuja la pantalla de inicio del juego."""
        pyxel.blt(8, 8, 1, 0, 0, 256, 256, 0)  # Dibuja la imagen de inicio

    def _dibujar_elementos_juego(self):
        """Dibuja los elementos del juego como personajes y objetos."""
        self._draw_monedas()  # Dibuja todas las monedas
        self._draw_muros()    # Dibuja los muros del nivel
        self._dibujar_personajes()  # Dibuja pacman y fantasmas
        self._draw_vidas()    # Dibuja el contador de vidas
        self._dibujar_numero(self.__puntos)  # Dibuja la puntuación

    def _draw_vidas(self):
        # Dibuja las vidas restantes de Pacman como íconos
        for i in range(self.__pacman.vidas):
            pyxel.blt((i+1)*18, 17*16, 0, 16, 0, 16, 16)

    def _dibujar_numero(self, numero: int):
        # Dibuja la puntuación dígito por dígito
        str_numero = str(numero)
        i = 0
        for caracter in str_numero:
                pyxel.blt(13*16 + i*16, 17*16, 2, int(caracter) * 16, 0, 8, 16)
                i +=1

    def _dibujar_personajes(self):
        """Dibuja a Pacman y los fantasmas."""
        self._dibujar_pacman()
        self._draw_pinky()
        self._draw_clyde()
        self._draw_blinky()
        self._draw_inky()

    def _dibujar_pacman(self):
        # Dibuja a Pacman según su dirección actual y frame de animación
        pyxel.blt(self.__pacman.x - ANCHO_PACMAN, self.__pacman.y - ALTO_PACMAN,
                  *self.__pacman.sprite[self.__pacman.last_direction][
                      self.__pacman.sprite_actual])

    def _draw_blinky(self):
        # Dibuja a Blinky en modo normal o de huida
        if not self.__pacman.cazar:
            pyxel.blt(self.__blinky.x - ANCHO_BLINKY, self.__blinky.y -
                      ALTO_BLINKY,
                      *self.__blinky.sprite[self.__blinky.last_direction])
        else:
            pyxel.blt(self.__blinky.x - ANCHO_BLINKY, self.__blinky.y -
                      ALTO_BLINKY, *FANTASMAS_HUIR[self.__blinky.sprite_actual])

    def _draw_pinky(self):
        # Dibuja a Pinky en modo normal o de huida
        if not self.__pacman.cazar:
            pyxel.blt(self.__pinky.x - ANCHO_PINKY, self.__pinky.y - ALTO_PINKY,
                      *self.__pinky.sprite[self.__pinky.last_direction])
        else:
            pyxel.blt(self.__pinky.x - ANCHO_PINKY, self.__pinky.y - ALTO_PINKY,
                      *FANTASMAS_HUIR[self.__blinky.sprite_actual])

    def _draw_clyde(self):
        # Dibuja a Clyde en modo normal o de huida
        if not self.__pacman.cazar:
            pyxel.blt(self.__clyde.x - ANCHO_CLYDE, self.__clyde.y - ALTO_CLYDE,
                      *self.__clyde.sprite[self.__clyde.last_direction])
        else:
            pyxel.blt(self.__clyde.x - ANCHO_CLYDE, self.__clyde.y - ALTO_CLYDE,
                      *FANTASMAS_HUIR[self.__clyde.sprite_actual])

    def _draw_inky(self):
        # Dibuja a Inky en modo normal o de huida
        if not self.__pacman.cazar:
            pyxel.blt(self.__inky.x - ANCHO_INKY, self.__inky.y - ALTO_INKY,
                      *self.__inky.sprite[self.__inky.last_direction])
        else:
            pyxel.blt(self.__inky.x - ANCHO_INKY, self.__inky.y - ALTO_INKY,
                      *FANTASMAS_HUIR[self.__inky.sprite_actual])

    def _draw_monedas(self):
        # Dibuja cada moneda según su tipo (normal, pastilla o fruta)
        for (x, y, tipo) in self.__monedas.lista_monedas:
            if tipo == 0:  # Moneda normal
                pyxel.blt((x - 1) * 16, (y - 1) * 16, 0, 32, 32, 16, 16)
            elif tipo == 1:  # Pastilla de poder
                pyxel.blt((x - 1) * 16, (y - 1) * 16, 0, 48, 32, 16, 16)
            else:  # Fruta
                pyxel.blt((x - 1) * 16, (y - 1) * 16, 0, 32, 216, 16, 16)

    def _draw_muros(self):
        # Dibuja cada muro según su tipo (diferentes sprites para esquinas y bordes)
        for (x, y, tipo) in self.__muros.lista_muros:
            if tipo == 0:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 0, 112, 16, 16)
            if tipo == 1:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 16, 112, 16, 16)
            if tipo == 2:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 32, 112, 16, 16)
            if tipo == 3:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 48, 112, 16, 16)
            if tipo == 4:
                pyxel.blt((x-1) * 16, (y-1) * 16, 0, 48, 128, 16, 16)
            if tipo == 5:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 48, 144, 16, 16)
            if tipo == 6:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 0, 128, 16, 16)
            if tipo == 7:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 16, 128, 16, 16)
            if tipo == 8:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 32, 128, 16, 16)
            if tipo == 9:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 32, 144, 16, 16)
            if tipo == 10:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 32, 160, 16, 16)
            if tipo == 11:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 0, 144, 16, 16)
            if tipo == 12:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 16, 144, 16, 16)
            if tipo == 13:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 0, 160, 16, 16)
            if tipo == 14:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 16, 160, 16, 16)
            if tipo == 15:
                pyxel.blt((x-1) * 16 , (y-1) * 16, 0, 8, 152, 16, 16)
            if tipo == 16:
                pyxel.blt((x - 1) * 16, (y - 1) * 16, 0, 32, 176, 16, 16)