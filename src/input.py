import pygame
import os
import sys
from components import Position

if os.getenv("CI") == "true":
    os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.mixer.init()
victory_sound = pygame.mixer.Sound("src/assets/victory.wav")

MOVE_MAP = {
    pygame.K_LEFT: (-1, 0),
    pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0),
    pygame.K_d: (1, 0),
    pygame.K_UP: (0, -1),
    pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_s: (0, 1),
}

ACTION_KEYS = {pygame.K_RETURN, pygame.K_SPACE}


def move_player(event, pos, grid):
    if event.key in MOVE_MAP:
        dx, dy = MOVE_MAP[event.key]
        new_x, new_y = int(pos.x) + dx, int(pos.y) + dy
        if 0 <= new_x < len(grid[0]) and 0 <= new_y < len(grid):
            pos.x, pos.y = new_x, new_y


def reveal_cell(event, pos, revealed, grid):
    if event.key in ACTION_KEYS and not revealed[int(pos.y)][int(pos.x)]:
        revealed[int(pos.y)][int(pos.x)] = True
        if check_victory(grid, revealed):
            return True  # devuelve estado de victoria
    return False


def handle_input(event, player, grid, revealed, world):
    pos = world.component_for_entity(player, Position)
    move_player(event, pos, grid)
    if reveal_cell(event, pos, revealed, grid):
        print("[INFO] ¡Has ganado!!!! 🎉")

        # Reproducir sonido de victoria
        victory_sound.set_volume(0.7)
        victory_sound.play()

        # Mostrar mensaje en pantalla
        screen = pygame.display.get_surface()
        result = show_victory_screen(screen)
        return result

    elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        return "restart"
    return None


def show_victory_screen(screen):
    font = pygame.font.SysFont(None, 72)
    text = font.render(
        "¡Has ganado! (R=Reiniciar, Q=Salir)", True, (0, 255, 0))
    rect = text.get_rect(
        center=(screen.get_width()//2, screen.get_height()//2))
    screen.blit(text, rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)
                elif e.key == pygame.K_r:
                    return "restart"  # Retornar restart en lugar de solo salir del bucle

    return None


def check_victory(grid, revealed):
    """Verifica si todas las minas ('x') han sido reveladas."""
    return all(
        not (val == 'x' and not revealed[y][x])
        for y, row in enumerate(grid)
        for x, val in enumerate(row)
    )
