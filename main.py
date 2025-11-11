import esper
import pygame
import os
import time

# Evitar errores de audio en entornos sin salida de sonido
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Inicialización segura
try:
    pygame.init()
    print("[INFO] pygame inicializado correctamente")
except Exception as e:
    print(f"[ERROR] Falló la inicialización de pygame: {e}")
    exit(1)

try:
    world = esper.World()
    print("[INFO] Mundo ECS creado con esper")
except Exception as e:
    print(f"[ERROR] Falló la creación del mundo ECS: {e}")
    exit(1)

try:
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    print("[INFO] Pantalla y reloj inicializados")
except Exception as e:
    print(f"[ERROR] Falló la creación de pantalla o reloj: {e}")
    exit(1)

# Componentes


class Position:
    def __init__(self, x, y): self.x, self.y = x, y


class Velocity:
    def __init__(self, dx, dy): self.dx, self.dy = dx, dy


class Sprite:
    def __init__(self, image): self.image = image

# Sistemas


def movement_system(world, dt):
    for ent, (pos, vel) in world.get_components(Position, Velocity):
        pos.x += vel.dx * dt
        pos.y += vel.dy * dt


def render_system(world, dt):
    screen.fill((30, 30, 30))
    for ent, (pos, sprite) in world.get_components(Position, Sprite):
        screen.blit(sprite.image, (pos.x, pos.y))
    pygame.display.flip()


# Entidad jugador
player_sprite = pygame.Surface((50, 50))
player_sprite.fill((0, 255, 0))
player = world.create_entity()
world.add_component(player, Position(375, 275))
world.add_component(player, Velocity(0, 0))
world.add_component(player, Sprite(player_sprite))

# Bucle principal con salida automática en CI/CD
running = True
start_time = time.time()
ci_mode = os.getenv("CI") == "true"

while running:
    dt = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # controles
    keys = pygame.key.get_pressed()
    speed = 200  # píxeles por segundo

    vel = world.component_for_entity(player, Velocity)
    vel.dx = vel.dy = 0  # Reiniciar velocidad cada frame

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        vel.dx = -speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        vel.dx = speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        vel.dy = -speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        vel.dy = speed

    # Salida automática en CI/CD después de 5 segundos
    if ci_mode and time.time() - start_time > 5:
        print("[INFO] Finalizando ejecución automática en entorno CI/CD")
        running = False

    world.process()
    movement_system(world, dt)
    render_system(world, dt)

pygame.quit()
print("[INFO] Juego finalizado correctamente")
