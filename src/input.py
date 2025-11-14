import pygame
from components import Position


def handle_input(event, player, grid, revealed, world):
    pos = world.component_for_entity(player, Position)

    # Convertimos a enteros para evitar errores de índice
    x = int(pos.x)
    y = int(pos.y)

    if event.key in [pygame.K_LEFT, pygame.K_a] and x > 1:
        pos.x -= 1
    elif event.key in [pygame.K_RIGHT, pygame.K_d] and x < len(grid[0]) - 1:
        pos.x += 1
    elif event.key in [pygame.K_UP, pygame.K_w] and y > 1:
        pos.y -= 1
    elif event.key in [pygame.K_DOWN, pygame.K_s] and y < len(grid) - 1:
        pos.y += 1
    elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
        if not revealed[y][x]:
            revealed[y][x] = True
