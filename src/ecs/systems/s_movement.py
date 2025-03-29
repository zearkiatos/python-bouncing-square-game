import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_movement(world: esper.World, delta_time:float):
    components = world.get_components(CVelocity, CTransform)

    c_transform:CTransform
    c_velocity:CVelocity
    for entity, (c_velocity, c_transform) in components:
        c_transform.position.x += c_velocity.velocity.x * delta_time
        c_transform.position.y += c_velocity.velocity.y * delta_time
        
