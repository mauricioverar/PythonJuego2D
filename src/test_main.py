from input import play_reveal_sound
import esper
import pygame
import os

os.environ["SDL_AUDIODRIVER"] = "dummy"


def test_pygame_init():
    pygame.init()
    assert pygame.get_init()


def test_surface_creation():
    surface = pygame.Surface((100, 100))
    surface.fill((0, 255, 0))
    assert surface.get_at((0, 0)) == (0, 255, 0, 255)


def test_ecs_world():
    world = esper.World()
    assert isinstance(world, esper.World)


def test_empty_reveal_sound_creates_sound():
    pygame.mixer.init()
    sound = play_reveal_sound()
    assert sound is not None
    assert hasattr(sound, "play")
