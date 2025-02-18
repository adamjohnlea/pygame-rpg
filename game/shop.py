import pygame

class Shop:
    def __init__(self):
        self.items = [
            {"id": "health_potion", "name": "Health Potion", "price": 50, "effect": {"health": 20}},
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
                success, message = self.buy_item(player, self.selected_item)
                return success, message
        return False, None

    def buy_item(self, player, item_index):
        if item_index < 0 or item_index >= len(self.items):
            return False, None

        item = self.items[item_index]
        print(f"Attempting to buy {item['name']} for {item['price']} gold. Current gold: {player.stats['gold']}")
        
        if player.stats['gold'] >= item['price']:
            # Deduct gold first
            old_gold = player.stats['gold']
            player.stats['gold'] -= item['price']
            print(f"Gold deducted: {item['price']}. Old gold: {old_gold}, New gold: {player.stats['gold']}")
            
            # Create a clean copy with only necessary data
            inventory_item = {
                "id": item['id'],
                "name": item['name'],
                "effect": item['effect'].copy() if 'effect' in item else {}
            }
            print(f"Adding item to inventory: {inventory_item}")
            player.inventory.add_item(inventory_item)
            return True, None
        else:
            return False, f"Not enough gold!\nRequired: {item['price']}\nYou have: {player.stats['gold']}"

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

        # Center the shop menu on screen
        shop_x = (1280 - shop_surface.get_width()) // 2
        shop_y = (1024 - shop_surface.get_height()) // 2
        screen.blit(shop_surface, (shop_x, shop_y))