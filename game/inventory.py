import pygame

class Inventory:
    def __init__(self):
        self.items = []
        self.max_items = 20
        self.selected_item = 0  # Track selected item index
        self.font = pygame.font.Font(None, 24)

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

    def use_item(self, player):
        """Use the currently selected item."""
        if not self.items or self.selected_item >= len(self.items):
            return False, "No item selected!"

        item = self.items[self.selected_item]
        if 'effect' in item:
            for stat, value in item['effect'].items():
                if stat == 'health':
                    # Don't exceed max health
                    player.stats['health'] = min(
                        player.stats['health'] + value,
                        player.stats['max_health']
                    )
                    message = f"Used {item['name']}! Restored {value} health."
                else:
                    # Handle other stat effects
                    if stat in player.stats:
                        player.stats[stat] += value
                        message = f"Used {item['name']}! {stat.capitalize()} increased by {value}."

            # Remove the used item
            self.items.pop(self.selected_item)
            # Adjust selected item if we removed the last item
            if self.selected_item >= len(self.items):
                self.selected_item = max(0, len(self.items) - 1)
            return True, message

        return False, "This item has no effect!"

    def handle_input(self, event, player):
        """Handle inventory input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % max(1, len(self.items))
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % max(1, len(self.items))
            elif event.key == pygame.K_RETURN:
                return self.use_item(player)
        return False, None

    def render(self, screen):
        # Draw inventory background
        inventory_surface = pygame.Surface((400, 300))
        inventory_surface.fill((50, 50, 50))
        pygame.draw.rect(inventory_surface, (100, 100, 100), (0, 0, 400, 300), 2)

        # Draw title
        title = self.font.render("Inventory (↑↓ to select, Enter to use)", True, (255, 255, 255))
        inventory_surface.blit(title, (20, 20))
        y_offset = 50

        # Draw items
        for i, item in enumerate(self.items):
            # Highlight selected item
            if i == self.selected_item:
                pygame.draw.rect(inventory_surface, (80, 80, 80), 
                               (15, y_offset - 2, 370, 25))

            # Get item name or fallback to item ID if name is missing
            item_name = item.get('name', item.get('id', 'Unknown Item'))
            quantity = item.get('quantity', 1)
            
            # Item name and quantity
            text = self.font.render(f"{item_name} x{quantity}", True, 
                                  (255, 255, 0) if i == self.selected_item else (255, 255, 255))
            inventory_surface.blit(text, (20, y_offset))
            
            # If item has effects, display them on the next line
            if 'effect' in item and item['effect']:
                effect_text = []
                for stat, value in item['effect'].items():
                    effect_text.append(f"{stat}: +{value}")
                if effect_text:
                    effects = self.font.render("  " + ", ".join(effect_text), True, 
                                             (150, 255, 150) if i == self.selected_item else (100, 255, 100))
                    y_offset += 20
                    inventory_surface.blit(effects, (30, y_offset))
            
            y_offset += 30

        # Center the inventory on screen (1280x1024)
        inventory_x = (1280 - inventory_surface.get_width()) // 2
        inventory_y = (1024 - inventory_surface.get_height()) // 2
        screen.blit(inventory_surface, (inventory_x, inventory_y))
