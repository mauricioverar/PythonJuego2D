import math
import pygame
import os
import sys
from array import array
from components import Position

if os.getenv("CI") == "true":
    os.environ["SDL_AUDIODRIVER"] = "dummy"

pygame.mixer.init()
victory_sound = pygame.mixer.Sound("src/assets/victory.wav")


def play_reveal_sound():
    """Genera un pequeño beep para celdas vacías reveladas."""
    sample_rate = 22050
    duration = 0.08
    frequency = 680
    volume = 0.2
    total_samples = int(sample_rate * duration)
    samples = array('h')

    for i in range(total_samples):
        t = i / sample_rate
        envelope = max(0.0, 1.0 - (t / duration) * 1.4)
        wave = math.sin(2 * math.pi * frequency * t)
        value = int(32767 * wave * envelope * volume)
        samples.append(value)

    sound = pygame.mixer.Sound(buffer=samples.tobytes())
    sound.set_volume(0.7)
    sound.play()
    return sound


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
    x = int(pos.x)
    y = int(pos.y)

    if event.key in ACTION_KEYS and not revealed[y][x]:
        revealed[y][x] = True

        if grid[y][x] == '':
            play_reveal_sound()

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
