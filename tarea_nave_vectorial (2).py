"""Nave vectorial y proyectiles 2D - Pygame.
Instalacion: pip install pygame
Ejecucion: python tarea_nave_vectorial.py
"""
import math
import pygame

ANCHO, ALTO = 800, 600
FPS = 60
FONDO = (12, 16, 32)
BLANCO = (235, 242, 255)
CIAN = (60, 225, 245)
AMARILLO = (255, 205, 75)
VELOCIDAD_NAVE = 220.0       # pixeles por segundo
VELOCIDAD_GIRO = 190.0       # grados por segundo
VELOCIDAD_DISPARO = 470.0    # pixeles por segundo
VIDA_DISPARO = 1.8           # segundos
COOLDOWN_MS = 250

# Vertices locales con centroide en (0, 0) y proa en (0, -25).
MODELO_NAVE = [(0, -25), (-18, 12.5), (18, 12.5)]


def transformar_punto(local_x, local_y, x, y, angulo):
    """Rotacion alrededor del origen local y posterior traslacion."""
    c, s = math.cos(angulo), math.sin(angulo)
    return (x + local_x * c - local_y * s,
            y + local_x * s + local_y * c)


def ejecutar():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.DOUBLEBUF)
    pygame.display.set_caption('Nave vectorial y proyectiles 2D')
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont('consolas', 18)

    x, y = 400.0, 300.0
    angulo = 0.0
    proyectiles = []
    ultimo_disparo = -COOLDOWN_MS
    activo = True

    while activo:
        dt = min(reloj.tick(FPS) / 1000.0, 0.05)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                activo = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                activo = False

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            angulo -= math.radians(VELOCIDAD_GIRO) * dt
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            angulo += math.radians(VELOCIDAD_GIRO) * dt

        # La proa local apunta hacia arriba: vector (sin(theta), -cos(theta)).
        direccion_x = math.sin(angulo)
        direccion_y = -math.cos(angulo)
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            x += direccion_x * VELOCIDAD_NAVE * dt
            y += direccion_y * VELOCIDAD_NAVE * dt

        # Reto opcional: pantalla envolvente en los cuatro bordes.
        x %= ANCHO
        y %= ALTO

        ahora = pygame.time.get_ticks()
        if teclas[pygame.K_SPACE] and ahora - ultimo_disparo >= COOLDOWN_MS:
            punta_x, punta_y = transformar_punto(0, -25, x, y, angulo)
            proyectiles.append({
                'x': punta_x, 'y': punta_y,
                'vx': direccion_x * VELOCIDAD_DISPARO,
                'vy': direccion_y * VELOCIDAD_DISPARO,
                'vida': VIDA_DISPARO,
            })
            ultimo_disparo = ahora

        # Actualizacion independiente y filtrado de proyectiles expirados.
        for proyectil in proyectiles:
            proyectil['x'] += proyectil['vx'] * dt
            proyectil['y'] += proyectil['vy'] * dt
            proyectil['vida'] -= dt
        proyectiles = [p for p in proyectiles
                       if p['vida'] > 0
                       and 0 <= p['x'] < ANCHO
                       and 0 <= p['y'] < ALTO]

        pantalla.fill(FONDO)
        vertices = [transformar_punto(lx, ly, x, y, angulo)
                    for lx, ly in MODELO_NAVE]
        pygame.draw.polygon(pantalla, CIAN, vertices, width=3)
        pygame.draw.line(pantalla, BLANCO, (x, y), vertices[0], width=2)

        for p in proyectiles:
            pygame.draw.circle(pantalla, AMARILLO,
                               (round(p['x']), round(p['y'])), 4)

        controles = 'W/Arriba: avanzar | A/D: girar | ESPACIO: disparar | ESC: salir'
        pantalla.blit(fuente.render(controles, True, BLANCO), (15, 15))
        estado = f'Posicion: ({x:.0f}, {y:.0f}) | Proyectiles: {len(proyectiles)}'
        pantalla.blit(fuente.render(estado, True, BLANCO), (15, 40))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    ejecutar()
