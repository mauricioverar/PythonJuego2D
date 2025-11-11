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


def draw_grid():
    cell_size = 100
    font = pygame.font.SysFont(None, 48)
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            rect = pygame.Rect(x * cell_size, y * cell_size,
                               cell_size, cell_size)
            pygame.draw.rect(screen, (60, 60, 60), rect)  # fondo de celda
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)  # borde

            if revealed[y][x]:
                if grid[y][x] == 'x':
                    pygame.draw.rect(screen, (60, 60, 60), rect)  # fondo normal para 'x'
                else:
                    # fondo verde oscuro para celdas reveladas sin 'x'
                    pygame.draw.rect(screen, (20, 60, 20), rect)


            else:
                pygame.draw.rect(screen, (30, 30, 30), rect)  # fondo oculto

            pygame.draw.rect(screen, (100, 100, 100), rect, 2)  # borde


            if revealed[y][x] and grid[y][x] != '':
                text = font.render(str(grid[y][x]), True, (255, 255, 255))
                screen.blit(text, (x * cell_size + 35, y * cell_size + 25))

# Entidad jugador
player_sprite = pygame.Surface((50, 50))
player_sprite.fill((0, 255, 0))
player = world.create_entity()
world.add_component(player, Position(0, 0))
world.add_component(player, Velocity(0, 0))
world.add_component(player, Sprite(player_sprite))

# Bucle principal con salida automática en CI/CD
running = True
start_time = time.time()
ci_mode = os.getenv("CI") == "true"

move_cooldown = 0.2
last_move = 0

while running:
    dt = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and time.time() - last_move > move_cooldown:
            pos = world.component_for_entity(player, Position)
            if event.key in [pygame.K_LEFT, pygame.K_a] and pos.x > 0:
                pos.x -= 1
            if event.key in [pygame.K_RIGHT, pygame.K_d] and pos.x < len(grid[0]) - 1:
                pos.x += 1
            if event.key in [pygame.K_UP, pygame.K_w] and pos.y > 0:
                pos.y -= 1
            if event.key in [pygame.K_DOWN, pygame.K_s] and pos.y < len(grid) - 1:
                pos.y += 1
            if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                if not revealed[pos.y][pos.x] and grid[pos.y][pos.x] != '':
                    revealed[pos.y][pos.x] = True

            last_move = time.time()

    # Salida automática en CI/CD después de 5 segundos
    if ci_mode and time.time() - start_time > 5:
        print("[INFO] Finalizando ejecución automática en entorno CI/CD")
        running = False

    world.process()
    render_system(world, dt)

pygame.quit()
print("[INFO] Juego finalizado correctamente")
