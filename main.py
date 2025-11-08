import esper
import pygame
import os
os.environ["SDL_AUDIODRIVER"] = "dummy"


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

# Componentos
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
    screen.fill((30,30,30))
    for ent, (pos, sprite) in world.get_components(Position, Sprite):
        screen.blit(sprite.image, (pos.x, pos.y))
    pygame.display.flip()

world = esper.World()
player_sprite = pygame.Surface((50, 50))
player_sprite.fill((0, 255, 0))
player = world.create_entity()
world.add_component(player, Position(375, 275))
world.add_component(player, Velocity(0, 0))
world.add_component(player, Sprite(player_sprite))

running = True
while running:
    dt = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        # ... controles
    world.process()
    movement_system(world, dt)
    render_system(world, dt)
