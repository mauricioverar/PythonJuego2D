import pygame

from components import Position


def handle_input(event, player, grid, revealed, world):
    pos = world.component_for_entity(player, Position)

    if event.key in [pygame.K_LEFT, pygame.K_a] and pos.x > 1:
        pos.x -= 1
    elif event.key in [pygame.K_RIGHT, pygame.K_d] and pos.x < len(grid[0]) - 1:
        pos.x += 1
    elif event.key in [pygame.K_UP, pygame.K_w] and pos.y > 1:
        pos.y -= 1
    elif event.key in [pygame.K_DOWN, pygame.K_s] and pos.y < len(grid) - 1:
        pos.y += 1
    elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
        if not revealed[pos.y][pos.x]:
            revealed[pos.y][pos.x] = True
