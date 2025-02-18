import pygame
from .inventory import Inventory

class Player:
    def __init__(self, x, y):
        print(f"Initializing Player at position ({x}, {y})")
        # Initialize basic attributes
        self.width = 32
        self.height = 48
        self.speed = 5
        self.x = x
        self.y = y

        # Create rect for collision detection
        self.rect = pygame.Rect(x, y, self.width, self.height)
        print(f"Created player rect at ({self.rect.x}, {self.rect.y})")

        # Initialize inventory and stats
        self.inventory = Inventory()
        self.stats = {
            "health": 100,
            "max_health": 100,
            "stamina": 100,
            "max_stamina": 100,
            "attack": 10,
            "defense": 5,
            "gold": 100
        }
        print("Player initialization completed")

    def reset_position(self, x=400, y=300):
        """Reset player position to specified coordinates"""
        print(f"Resetting player position to ({x}, {y})")
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        print(f"New player position: ({self.x}, {self.y}), rect: ({self.rect.x}, {self.rect.y})")

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.move(0, -self.speed)
            elif event.key == pygame.K_s:
                self.move(0, self.speed)
            elif event.key == pygame.K_a:
                self.move(-self.speed, 0)
            elif event.key == pygame.K_d:
                self.move(self.speed, 0)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.x = self.x
        self.rect.y = self.y

        # Keep player in bounds for 1280x1024 resolution
        self.x = max(0, min(self.x, 1280 - self.width))
        self.y = max(0, min(self.y, 1024 - self.height))
        
        # Update rectangle position to match actual position
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.move(0, -self.speed)
        if keys[pygame.K_s]:
            self.move(0, self.speed)
        if keys[pygame.K_a]:
            self.move(-self.speed, 0)
        if keys[pygame.K_d]:
            self.move(self.speed, 0)

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)