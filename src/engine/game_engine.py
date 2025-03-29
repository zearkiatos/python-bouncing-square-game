import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.system_movement import systems_movement


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((640, 340), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = 60
        self.delta_time = 0

        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        square_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(square_entity, CSurface(
            size=pygame.Vector2(50, 50), color=pygame.Color(255, 255, 100)))
        self.ecs_world.add_component(
            square_entity, CTransform(position=pygame.Vector2(150, 100)))
        self.ecs_world.add_component(square_entity, CVelocity(velocity=pygame.Vector2(100, 100)))

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        systems_movement()

    def _draw(self):
        self.screen.fill((0, 200, 128))

        pygame.display.flip()

    def _clean(self):
        pygame.quit()
