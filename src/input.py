import pygame
from components import Position


def move_player(event, pos, grid):
    # Convertimos a enteros para evitar errores de índice
    x, y = int(pos.x), int(pos.y)

    if event.key in [pygame.K_LEFT, pygame.K_a] and x > 1:
        pos.x -= 1
    elif event.key in [pygame.K_RIGHT, pygame.K_d] and x < len(grid[0]) - 1:
        pos.x += 1
    elif event.key in [pygame.K_UP, pygame.K_w] and y > 1:
        pos.y -= 1
    elif event.key in [pygame.K_DOWN, pygame.K_s] and y < len(grid) - 1:
        pos.y += 1


def reveal_cell(event, pos, revealed, grid):
    x, y = int(pos.x), int(pos.y)
    if event.key in [pygame.K_RETURN, pygame.K_SPACE] and not revealed[y][x]:
        revealed[y][x] = True

        # Chequear victoria
        if check_victory(grid, revealed):
            print("[INFO] ¡Has ganado! 🎉")
            # Opcional: mostrar mensaje en pantalla
            font = pygame.font.SysFont(None, 72)
            text = font.render("¡Has ganado!", True, (0, 255, 0))
            screen = pygame.display.get_surface()
            rect = text.get_rect(
                center=(screen.get_width()//2, screen.get_height()//2))
            screen.blit(text, rect)
            pygame.display.flip()
            pygame.time.wait(3000)  # Espera 3 segundos antes de cerrar
            pygame.quit()
            exit(0)


def handle_input(event, player, grid, revealed, world):
    pos = world.component_for_entity(player, Position)
    move_player(event, pos, grid)
    reveal_cell(event, pos, revealed, grid)


def check_victory(grid, revealed):
    """Verifica si todas las minas ('x') han sido reveladas."""
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val == 'x' and not revealed[y][x]:
                return False
    return True
