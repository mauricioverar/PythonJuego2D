import pygame
from config import CELL_SIZE

# Grid base
grid = [
    ['*', 0, 2, 1, 2, 0],
    [0, '', '', '', '', ''],
    [2, '', 'x', '', 'x', ''],
    [1, '', '', 'x', '', ''],
    [2, '', 'x', '', 'x', ''],
    [0, '', '', '', '', ''],
]

# Estado de revelado
revealed = [[False for _ in row] for row in grid]


def auto_reveal_non_mines():
    """Revela automáticamente celdas que no son minas ni vacías."""
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val != '' and val != 'x':
                revealed[y][x] = True


def draw_cell_background(x, y, val, screen):
    """Dibuja el fondo de una celda según su tipo."""
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    if val == 'x':
        pygame.draw.rect(screen, (0, 0, 200), rect)
        inner_rect = pygame.Rect(
            x * CELL_SIZE + 20, y * CELL_SIZE + 20, CELL_SIZE - 40, CELL_SIZE - 40)
        pygame.draw.rect(screen, (255, 0, 0), inner_rect)
    elif val == '':
        pygame.draw.rect(screen, (200, 200, 0), rect)
    elif isinstance(val, int):
        pygame.draw.rect(screen, (20, 60, 20), rect)
    else:
        pygame.draw.rect(screen, (60, 60, 60), rect)
    return rect


def draw_cell_text(x, y, val, screen, font):
    """Dibuja el texto dentro de una celda revelada."""
    if val == 'x':
        return  # No mostrar texto para minas
    elif isinstance(val, int):
        text = font.render(str(val), True, (255, 255, 255))
    elif val == '':
        text = font.render(' ', True, (255, 255, 0))
    else:
        text = font.render(str(val), True, (255, 255, 255))
    screen.blit(text, (x * CELL_SIZE + 35, y * CELL_SIZE + 25))


def draw_grid(screen):
    """Dibuja el grid completo en pantalla."""
    font = pygame.font.SysFont(None, 48)
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE,
                               CELL_SIZE, CELL_SIZE)

            if revealed[y][x]:
                rect = draw_cell_background(x, y, val, screen)
            else:
                pygame.draw.rect(screen, (30, 30, 30), rect)

            pygame.draw.rect(screen, (100, 100, 100), rect, 2)

            if x == 0 or y == 0:
                pygame.draw.rect(screen, (150, 0, 0), rect, 3)

            if revealed[y][x]:
                draw_cell_text(x, y, val, screen, font)
