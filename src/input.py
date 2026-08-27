import pygame
from components import Position

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
        # Mostrar mensaje en pantalla
        screen = pygame.display.get_surface()
        font = pygame.font.SysFont(None, 72)
        text = font.render("¡Has ganado!", True, (0, 255, 0))
        rect = text.get_rect(
            center=(screen.get_width()//2, screen.get_height()//2))
        screen.blit(text, rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # espera 3 segundos
        pygame.quit()
        exit(0)


def check_victory(grid, revealed):
    """Verifica si todas las minas ('x') han sido reveladas."""
    return all(
        not (val == 'x' and not revealed[y][x])
        for y, row in enumerate(grid)
        for x, val in enumerate(row)
    )
