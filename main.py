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

grid = [
    ['*', 0, 2, 1, 2, 0],
    [0, '', '', '', '', ''],
    [2, '', 'x', '', 'x', ''],
    [1, '', '', 'x', '', ''],
    [2, '', 'x', '', 'x', ''],
    [0, '', '', '', '', ''],
]

CELL_SIZE = 100
PLAYER_SIZE = 50
CI_TIMEOUT = 5
MOVE_COOLDOWN = 0.2

revealed = [[False for _ in row] for row in grid]
# Revelar automáticamente las celdas que no son 'x' ni vacías
for y, row in enumerate(grid):
    for x, val in enumerate(row):
        if val != '' and val != 'x':
            revealed[y][x] = True

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
    draw_grid()
    for ent, (pos, sprite) in world.get_components(Position, Sprite):
        screen.blit(sprite.image, (pos.x * 100 + 25, pos.y * 100 + 25))
    pygame.display.flip()


def draw_cell_background(x, y, val):
    rect = pygame.Rect(x * 100, y * 100, 100, 100)
    if val == 'x':
        pygame.draw.rect(screen, (0, 0, 200), rect)
        inner_rect = pygame.Rect(x * 100 + 20, y * 100 + 20, 60, 60)
        pygame.draw.rect(screen, (255, 0, 0), inner_rect)
    elif val == '':
        pygame.draw.rect(screen, (200, 200, 0), rect)
    elif isinstance(val, int):
        pygame.draw.rect(screen, (20, 60, 20), rect)
    else:
        pygame.draw.rect(screen, (60, 60, 60), rect)
    return rect

def draw_grid():
    font = pygame.font.SysFont(None, 48)
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE,
                               CELL_SIZE, CELL_SIZE)

            # Fondo según estado revelado y tipo de celda
            if revealed[y][x]:
                rect = draw_cell_background(x, y, val)
            else:
                pygame.draw.rect(screen, (30, 30, 30), rect)  # fondo oculto

            # Borde gris
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)

            # Borde rojo si está en fila 0 o columna 0
            if x == 0 or y == 0:
                pygame.draw.rect(screen, (150, 0, 0), rect, 3)

            # Texto si revelado y no vacío
            if revealed[y][x]:
                val = grid[y][x]

                if val == 'x':
                    # Fondo azul
                    pygame.draw.rect(screen, (0, 0, 200), rect)

                    # Cuadro rojo centrado
                    inner_rect = pygame.Rect(
                        x * CELL_SIZE + 20,  # desplazamiento horizontal
                        y * CELL_SIZE + 20,  # desplazamiento vertical
                        CELL_SIZE - 40,      # ancho
                        CELL_SIZE - 40       # alto
                    )
                    pygame.draw.rect(screen, (255, 0, 0), inner_rect)


                elif isinstance(val, int):
                    pygame.draw.rect(screen, (20, 60, 20), rect)
                    text = font.render(str(val), True, (255, 255, 255))
                    screen.blit(text, (x * CELL_SIZE + 35, y * CELL_SIZE + 25))

                elif val == '':
                    pygame.draw.rect(screen, (200, 200, 0), rect)
                    text = font.render(' ', True, (255, 255, 0))
                    screen.blit(text, (x * CELL_SIZE + 35, y * CELL_SIZE + 25))


def handle_input(event, player, grid, revealed):
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

# Entidad jugador
player_sprite = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_sprite.fill((0, 255, 0))
player = world.create_entity()
world.add_component(player, Position(1, 1))
world.add_component(player, Velocity(0, 0))
world.add_component(player, Sprite(player_sprite))

# Bucle principal con salida automática en CI/CD
running = True
start_time = time.time()
ci_mode = os.getenv("CI") == "true"

last_move = 0

while running:
    dt = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and time.time() - last_move > MOVE_COOLDOWN:
            handle_input(event, player, grid, revealed)
            last_move = time.time()

    # Salida automática en CI/CD después de 5 segundos
    if ci_mode and time.time() - start_time > CI_TIMEOUT:
        print("[INFO] Finalizando ejecución automática en entorno CI/CD")
        running = False

    world.process()
    render_system(world, dt)

pygame.quit()
print("[INFO] Juego finalizado correctamente")
