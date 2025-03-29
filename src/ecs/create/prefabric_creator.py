import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def create_square(world: esper.World, size: pygame.Vector2, position: pygame.Vector2, velocity: pygame.Vector2, color: pygame.Color):
    square_entity = world.create_entity()
    world.add_component(square_entity, CSurface(
        size, color))
    world.add_component(
        square_entity, CTransform(position))
    world.add_component(
        square_entity, CVelocity(velocity))
