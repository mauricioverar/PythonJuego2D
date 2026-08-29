import os
import time
import pygame
import esper

from config import CELL_SIZE, PLAYER_SIZE, CI_TIMEOUT, MOVE_COOLDOWN, SCREEN_WIDTH, SCREEN_HEIGHT, GREEN
from components import Position, Velocity, Sprite
from grid import grid, revealed, draw_grid, auto_reveal_non_mines
from input import handle_input

from systems import MovementSystem, RenderSystem

# 🧱 Inicialización segura
os.environ["SDL_AUDIODRIVER"] = "dummy"


def init_game(screen):
    auto_reveal_non_mines()

    player_sprite = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
    player_sprite.fill(GREEN)

    world = esper.World()
    player = world.create_entity()
    world.add_component(player, Position(1, 1))
    world.add_component(player, Velocity(0, 0))
    world.add_component(player, Sprite(player_sprite))

    world.add_processor(MovementSystem())
    world.add_processor(RenderSystem(screen))

    return world, player, grid, revealed


def fatal_error(msg):
    print(f"[ERROR] {msg}")
    exit(1)


def init_pygame():
    try:
        pygame.init()
        print("[INFO] pygame inicializado correctamente")
    except Exception as e:
        fatal_error(f"Falló la inicialización de pygame: {e}")


def init_world():
    try:
        world = esper.World()
        print("[INFO] Mundo ECS creado con esper")
        return world
    except Exception as e:
        fatal_error(f"Falló la creación del mundo ECS: {e}")


def init_display():
    try:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()
        print("[INFO] Pantalla y reloj inicializados")
        return screen, clock
    except Exception as e:
        fatal_error(f"Falló la creación de pantalla o reloj: {e}")


def restart_game():
    """Reinicializa el juego limpiando el estado."""
    # Limpiar estado del grid
    for y in range(len(revealed)):
        for x in range(len(revealed[0])):
            revealed[y][x] = False

    auto_reveal_non_mines()
    print("[INFO] Juego reiniciado")


def main():
    init_pygame()
    world = init_world()
    screen, clock = init_display()

    auto_reveal_non_mines()

    player_sprite = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
    player_sprite.fill(GREEN)

    player = world.create_entity()
    world.add_component(player, Position(1, 1))
    world.add_component(player, Velocity(0, 0))
    world.add_component(player, Sprite(player_sprite))

    world.add_processor(MovementSystem())
    world.add_processor(RenderSystem(screen))

    running = True
    start_time = time.time()
    ci_mode = os.getenv("CI") == "true"
    last_move = 0

    if ci_mode:
        print("[INFO] Modo CI/CD activado")

    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and time.time() - last_move > MOVE_COOLDOWN:
                result = handle_input(event, player, grid, revealed, world)
                if result == "restart":
                    print("[DEBUG] Reiniciando juego...")
                    # Limpiar todas las entidades del mundo
                    for ent in list(world._entities.keys()):
                        world.delete_entity(ent)

                    # Reinicializar juego
                    restart_game()

                    # Recrear jugador
                    player = world.create_entity()
                    world.add_component(player, Position(1, 1))
                    world.add_component(player, Velocity(0, 0))
                    world.add_component(player, Sprite(player_sprite))

                    start_time = time.time()

                    # Forzar redibujado completo
                    world.process(0)  # Procesar sin delta time

                last_move = time.time()

        if ci_mode and time.time() - start_time > CI_TIMEOUT:
            print("[INFO] Finalizando ejecución automática en entorno CI/CD")
            running = False

        world.process(dt)

    pygame.quit()
    print("[INFO] Juego finalizado correctamente")


if __name__ == "__main__":
    main()
