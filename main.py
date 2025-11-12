import os
import time
import pygame
import esper

from config import CELL_SIZE, PLAYER_SIZE, CI_TIMEOUT, MOVE_COOLDOWN
from components import Position, Velocity, Sprite
from grid import grid, revealed, draw_grid, auto_reveal_non_mines
from input import handle_input

# 🧱 Inicialización segura
os.environ["SDL_AUDIODRIVER"] = "dummy"

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

# 🧩 Revelado automático
auto_reveal_non_mines()

# 🎮 Entidad jugador
player_sprite = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_sprite.fill((0, 255, 0))

player = world.create_entity()
world.add_component(player, Position(1, 1))
world.add_component(player, Velocity(0, 0))
world.add_component(player, Sprite(player_sprite))

# 🌀 Sistemas ECS


def movement_system(world, dt):
    for ent, (pos, vel) in world.get_components(Position, Velocity):
        pos.x += vel.dx * dt
        pos.y += vel.dy * dt


def render_system(world, dt):
    screen.fill((30, 30, 30))
    draw_grid(screen)
    for ent, (pos, sprite) in world.get_components(Position, Sprite):
        screen.blit(sprite.image, (pos.x * CELL_SIZE +
                    25, pos.y * CELL_SIZE + 25))
    pygame.display.flip()


# 🚀 Bucle principal
running = True
start_time = time.time()
ci_mode = os.getenv("CI") == "true"
last_move = 0

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and time.time() - last_move > MOVE_COOLDOWN:
            handle_input(event, player, grid, revealed, world)
            last_move = time.time()

    if ci_mode and time.time() - start_time > CI_TIMEOUT:
        print("[INFO] Finalizando ejecución automática en entorno CI/CD")
        running = False

    world.process()
    render_system(world, dt)

pygame.quit()
print("[INFO] Juego finalizado correctamente")
