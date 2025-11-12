import pygame

from components import Position, Velocity, Sprite

def movement_system(world, dt):
    for ent, (pos, vel) in world.get_components(Position, Velocity):
        pos.x += vel.dx * dt
        pos.y += vel.dy * dt


def render_system(world, dt, screen, draw_grid):
    screen.fill((30, 30, 30))
    draw_grid()
    for ent, (pos, sprite) in world.get_components(Position, Sprite):
        screen.blit(sprite.image, (pos.x * 100 + 25, pos.y * 100 + 25))
    pygame.display.flip()
