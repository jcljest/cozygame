import os
import sys
from pathlib import Path

import pygame

# Screen settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 60

# Movement
PLAYER_SPEED = 250  # pixels per second

# Asset paths (replace with your own)
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
PLAYER_IMAGE_PATH = ASSETS_DIR / "player.png"
BACKGROUND_IMAGE_PATH = ASSETS_DIR / "background.png"


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size=(86, 96)):
        super().__init__()
        self.original_image = load_or_placeholder(
            PLAYER_IMAGE_PATH, size, (240, 200, 60)
        )
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=pos)

        self.velocity = pygame.Vector2(0, 0)
        self.facing_right = True  # or False, depending on your sprite

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        self.velocity.y = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x = -1
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x = 1
            self.facing_right = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity.y = 1
        if self.velocity.length_squared() > 0:
            self.velocity = self.velocity.normalize()

    def move(self, dt, colliders):
        # Move on X axis
        self.rect.x += int(self.velocity.x * PLAYER_SPEED * dt)
        self.resolve_collisions(colliders, axis="x")
        # Move on Y axis
        self.rect.y += int(self.velocity.y * PLAYER_SPEED * dt)
        self.resolve_collisions(colliders, axis="y")

    def resolve_collisions(self, colliders, axis):
        for collider in colliders:
            if self.rect.colliderect(collider):
                if axis == "x":
                    if self.velocity.x > 0:
                        self.rect.right = collider.left
                    elif self.velocity.x < 0:
                        self.rect.left = collider.right
                else:
                    if self.velocity.y > 0:
                        self.rect.bottom = collider.top
                    elif self.velocity.y < 0:
                        self.rect.top = collider.bottom

    def update_image(self):
        self.image = self.original_image
        if self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)


class World:
    def __init__(self):
        self.background = load_or_placeholder(
            BACKGROUND_IMAGE_PATH,
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            (40, 48, 56),
        )
        self.colliders = self._build_colliders()

    def _build_colliders(self):
        # Placeholder walls; replace with your own layout or imported hitboxes
        return [
            pygame.Rect(0, 0, SCREEN_WIDTH, 16),
            pygame.Rect(0, SCREEN_HEIGHT - 16, SCREEN_WIDTH, 16),
            pygame.Rect(0, 0, 16, SCREEN_HEIGHT),
            pygame.Rect(SCREEN_WIDTH - 16, 0, 16, SCREEN_HEIGHT),
        ]

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        # Debug: draw placeholder hitboxes
        for rect in self.colliders:
            pygame.draw.rect(surface, (80, 120, 140), rect)



def load_or_placeholder(path, size, color):
    if path.exists():
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.smoothscale(image, size)
        return image
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(color)
    return surface


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cozy Game Prototype")
    clock = pygame.time.Clock()

    world = World()
    player = Player((120, 120))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.handle_input()
        player.move(dt, world.colliders)
        player.update_image()

        world.draw(screen)
        screen.blit(player.image, player.rect.topleft)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
