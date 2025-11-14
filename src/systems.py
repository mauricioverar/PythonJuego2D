# systems.py

import pygame
import esper
from components import Position, Velocity, Sprite
from config import CELL_SIZE
from grid import draw_grid


class MovementSystem(esper.Processor):
    def process(self, dt: float):
        for ent, (pos, vel) in self.world.get_components(Position, Velocity):
            pos.x += vel.dx * dt
            pos.y += vel.dy * dt


class RenderSystem(esper.Processor):
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def process(self, dt: float):
        self.screen.fill((30, 30, 30))
        draw_grid(self.screen)
        for ent, (pos, sprite) in self.world.get_components(Position, Sprite):
            self.screen.blit(
                sprite.image, (pos.x * CELL_SIZE + 25, pos.y * CELL_SIZE + 25))
        pygame.display.flip()
