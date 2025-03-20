import pygame
import random
import os

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Destruye los Cuadros")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Reloj para controlar los FPS (fotogramas por segundo)
reloj = pygame.time.Clock()

# Fuente para el texto
fuente = pygame.font.Font(None, 36)

# Ruta del archivo de puntaje máximo
archivo_puntaje_maximo = "puntaje_maximo.txt"

# Cargar imágenes
def cargar_imagen(ruta, ancho, alto):
    imagen = pygame.image.load(ruta)
    return pygame.transform.scale(imagen, (ancho, alto))

# Imágenes, cargamos las imagenes segun nuestra ruta de almacenamiento
imagen_jugador = cargar_imagen("img\jugador.png", 50, 50)  
imagen_bala = cargar_imagen("img\bala.png", 10, 20)       
imagen_enemigo_comun = cargar_imagen("img\enemigo_comun.png", 50, 50)       
imagen_enemigo_poco_comun = cargar_imagen("img\enemigo_poco_comun.png", 50, 50)  
imagen_enemigo_inusual = cargar_imagen("img\enemigo_inusual.png", 50, 50)    

# Función para cargar el puntaje máximo desde un archivo
def cargar_puntaje_maximo():
    if os.path.exists(archivo_puntaje_maximo):
        with open(archivo_puntaje_maximo, "r") as archivo:
            return int(archivo.read())
    return 0

# Función para guardar el puntaje máximo en un archivo
def guardar_puntaje_maximo(puntaje):
    with open(archivo_puntaje_maximo, "w") as archivo:
        archivo.write(str(puntaje))

# Clase para el jugador
class Jugador:
    def __init__(self):
        self.rectangulo = pygame.Rect(ANCHO // 2 - 25, ALTO - 50, 50, 50)
        self.velocidad = 5
        self.vida = 50
        self.vida_maxima = 50
        self.ultimo_disparo = 0

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rectangulo.x > 0:
            self.rectangulo.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rectangulo.x < ANCHO - self.rectangulo.width:
            self.rectangulo.x += self.velocidad

    def disparar(self, balas):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_disparo > 100:
            balas.append(Bala(self.rectangulo.centerx, self.rectangulo.top))
            self.ultimo_disparo = tiempo_actual

    def dibujar(self, pantalla):
        pantalla.blit(imagen_jugador, self.rectangulo.topleft)
        self.dibujar_barra_vida(pantalla)

    def dibujar_barra_vida(self, pantalla):
        barra_ancho = 200
        barra_alto = 20
        barra_x = 10
        barra_y = 40
        vida_ancho = (self.vida / self.vida_maxima) * barra_ancho
        pygame.draw.rect(pantalla, (255, 0, 0), (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(pantalla, (0, 255, 0), (barra_x, barra_y, vida_ancho, barra_alto))

class Bala:
    def __init__(self, x, y):
        self.rectangulo = pygame.Rect(x - 5, y, 10, 20)
        self.velocidad = 7

    def mover(self):
        self.rectangulo.y -= self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(imagen_bala, self.rectangulo.topleft)

class Enemigo:
    def __init__(self, dificultad):
        tipo = random.choices(["comun", "poco_comun", "inusual"], [70, 20, 10])[0]
        self.tipo = tipo
        self.rectangulo = pygame.Rect(random.randint(0, ANCHO - 50), 0, 50, 50)

        # Aumentar la velocidad del enemigo según la dificultad
        self.velocidad = random.randint(2, 4) + dificultad // 10  # Incrementa la velocidad según el puntaje

        # Aumentar la vida del enemigo según la dificultad
        self.vida = 50 if tipo == "comun" else 80 if tipo == "poco_comun" else 100
        if dificultad > 50:
            self.vida += 30  # Aumenta la vida si la dificultad es alta

        self.puntaje = 10 if tipo == "comun" else 20 if tipo == "poco_comun" else 30

    def mover(self):
        self.rectangulo.y += self.velocidad

    def dibujar(self, pantalla):
        if self.tipo == "comun":
            pantalla.blit(imagen_enemigo_comun, self.rectangulo.topleft)
        elif self.tipo == "poco_comun":
            pantalla.blit(imagen_enemigo_poco_comun, self.rectangulo.topleft)
        elif self.tipo == "inusual":
            pantalla.blit(imagen_enemigo_inusual, self.rectangulo.topleft)

# Función para mostrar el menú de inicio
def mostrar_menu_inicio():
    pantalla.fill(NEGRO)
    texto_inicio = fuente.render("Presiona ENTER para Jugar o ESC para Salir", True, BLANCO)
    pantalla.blit(texto_inicio, (ANCHO // 2 - 200, ALTO // 2))
    pygame.display.flip()

# Función para mostrar el puntaje final
def mostrar_puntaje_final(puntaje, puntaje_maximo):
    pantalla.fill(NEGRO)
    texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
    texto_maximo = fuente.render(f"Puntaje Maximo: {puntaje_maximo}", True, BLANCO)
    pantalla.blit(texto_puntaje, (ANCHO // 2 - 100, ALTO // 2 - 50))
    pantalla.blit(texto_maximo, (ANCHO // 2 - 100, ALTO // 2))
    pygame.display.flip()

# Variables del juego
jugador = Jugador()
balas = []
enemigos = []
puntaje = 0
puntaje_maximo = cargar_puntaje_maximo()
jugar = False
dificultad = 0  # Inicialmente la dificultad es 0

# Bucle principal
while True:
    if not jugar:
        mostrar_menu_inicio()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:  # Empezar el juego
                    jugar = True
                    puntaje = 0
                    jugador = Jugador()
                    balas = []
                    enemigos = []
                    dificultad = 0  # Reiniciar la dificultad
                elif evento.key == pygame.K_ESCAPE:  # Salir del juego
                    pygame.quit()
                    exit()

    # Si el juego está en progreso
    if jugar:
        pantalla.fill(NEGRO)
        teclas = pygame.key.get_pressed()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jugador.disparar(balas)

        # Aumentar la frecuencia de aparición de los enemigos según el puntaje
        if random.randint(1, 100) <= max(2 - (dificultad // 10), 1):
            enemigos.append(Enemigo(dificultad))

        # Mover y dibujar las balas
        for bala in balas[:]:
            bala.mover()
            if bala.rectangulo.bottom < 0:
                balas.remove(bala)
            bala.dibujar(pantalla)

        # Mover y dibujar los enemigos
        for enemigo in enemigos[:]:
            enemigo.mover()
            if enemigo.rectangulo.top > ALTO:
                jugador.vida -= 5
                enemigos.remove(enemigo)
            enemigo.dibujar(pantalla)

        # Verificar colisiones entre balas y enemigos
        for bala in balas[:]:
            for enemigo in enemigos[:]:
                if bala.rectangulo.colliderect(enemigo.rectangulo):
                    enemigo.vida -= 20
                    balas.remove(bala)
                    if enemigo.vida <= 0:
                        puntaje += enemigo.puntaje
                        enemigos.remove(enemigo)
                    break

        jugador.mover(teclas)
        jugador.dibujar(pantalla)

        texto_puntaje = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        pantalla.blit(texto_puntaje, (10, 10))

        # Incrementar la dificultad basada en el puntaje
        dificultad = puntaje // 50  # Por cada 50 puntos, aumenta la dificultad

        if jugador.vida <= 0:
            if puntaje > puntaje_maximo:
                puntaje_maximo = puntaje
                guardar_puntaje_maximo(puntaje_maximo)
            mostrar_puntaje_final(puntaje, puntaje_maximo)
            pygame.time.delay(3000)
            jugar = False

        pygame.display.flip()
        reloj.tick(60)
