import pygame
class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((640, 340), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = 60
        self.delta_time = 0

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
        self.square_velocity = pygame.Vector2(100, 100)
        self.square_position = pygame.Vector2(-25, 100)
        square_size = pygame.Vector2(50,50)
        square_color = pygame.Color(0, 0, 0)

        self.square_superface = pygame.Surface(square_size)
        self.square_superface.fill(square_color)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        # We advance in X to 100 pixeles per seconds (delta_time)
        self.square_position.x += self.square_velocity.x * self.delta_time
        self.square_position.y += self.square_velocity.y * self.delta_time

        screen_rectangule = self.screen.get_rect()
        square_rectangule = self.square_superface.get_rect(topleft = self.square_position)

        if square_rectangule.left <= 0 or square_rectangule.right >= screen_rectangule.width:
            self.square_velocity.x *= -1
            square_rectangule.clamp_ip(screen_rectangule)
            self.square_position.x = square_rectangule.left

        if square_rectangule.top <= 0 or square_rectangule.bottom >= screen_rectangule.height:
            self.square_velocity.y *= -1
            square_rectangule.clamp_ip(screen_rectangule)
            self.square_position.y = square_rectangule.y

        # if my_rectangle.left <= 0 or my_rectangle.right

    def _draw(self):
        self.screen.fill((0, 200, 128))
        self.screen.blit(self.square_superface, self.square_position)
        pygame.display.flip()

    def _clean(self):
        pygame.quit()
