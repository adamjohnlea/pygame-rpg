import pygame

class Shop:
    def __init__(self):
        self.items = [
            {"id": "health_potion", "name": "Health Potion", "price": 50, "effect": {"health": 50}},
            {"id": "iron_sword", "name": "Iron Sword", "price": 100, "effect": {"attack": 5}},
            {"id": "leather_armor", "name": "Leather Armor", "price": 80, "effect": {"defense": 3}}
        ]
        self.selected_item = 0
        self.item_height = 30

    def handle_input(self, event, player):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                return self.buy_item(player, self.selected_item)
        return False

    def buy_item(self, player, item_index):
        if item_index < 0 or item_index >= len(self.items):
            return False

        item = self.items[item_index]
        if player.stats['gold'] >= item['price']:
            player.stats['gold'] -= item['price']
            player.inventory.add_item(item.copy())
            return True
        return False

    def render(self, screen):
        # Draw shop background
        shop_surface = pygame.Surface((400, 300))
        shop_surface.fill((80, 50, 20))
        pygame.draw.rect(shop_surface, (120, 80, 40), (0, 0, 400, 300), 2)

        # Draw items for sale
        font = pygame.font.Font(None, 24)
        for i, item in enumerate(self.items):
            y_pos = 20 + i * self.item_height
            # Highlight selected item
            if i == self.selected_item:
                pygame.draw.rect(shop_surface, (100, 80, 40), (10, y_pos - 2, 380, self.item_height))
            text = font.render(f"{item['name']} - {item['price']} gold", True, (255, 255, 255))
            shop_surface.blit(text, (20, y_pos))

        # Draw instructions
        instructions = font.render("↑↓: Select item, Enter: Buy", True, (200, 200, 200))
        shop_surface.blit(instructions, (20, 250))

        # Draw shop at center of screen
        screen.blit(shop_surface, (200, 150))