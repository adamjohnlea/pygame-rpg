import pygame

class Inventory:
    def __init__(self):
        self.items = []
        self.max_items = 20
        self.selected_item = None

    def add_item(self, item):
        if len(self.items) < self.max_items:
            self.items.append(item)
            return True
        return False

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def render(self, screen):
        # Draw inventory background
        inventory_surface = pygame.Surface((400, 300))
        inventory_surface.fill((50, 50, 50))
        pygame.draw.rect(inventory_surface, (100, 100, 100), (0, 0, 400, 300), 2)

        # Draw items
        font = pygame.font.Font(None, 24)
        for i, item in enumerate(self.items):
            y_pos = 20 + i * 30
            text = font.render(f"{item['name']} - {item.get('quantity', 1)}", True, (255, 255, 255))
            inventory_surface.blit(text, (20, y_pos))

        # Draw inventory at center of screen
        screen.blit(inventory_surface, (200, 150))
