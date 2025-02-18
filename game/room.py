import pygame

class Room:
    def __init__(self, room_type, size):
        self.room_type = room_type
        self.width, self.height = size
        self.exits = self.setup_exits()
        self.spawn_points = self.setup_spawn_points()
        self.objects = []
        self.shop = None
        self.interaction_area = pygame.Rect(300, 200, 200, 100)
        if room_type == 'shop':
            from .shop import Shop
            self.shop = Shop()

    def setup_exits(self):
        if self.room_type == 'town':
            return {
                'shop': pygame.Rect(750, 250, 50, 100),    # Right exit to shop
                'dungeon': pygame.Rect(0, 250, 50, 100)    # Left exit to dungeon
            }
        elif self.room_type == 'shop':
            return {
                'town': pygame.Rect(0, 250, 50, 100)      # Left exit to town
            }
        elif self.room_type == 'dungeon':
            return {
                'town': pygame.Rect(750, 250, 50, 100)    # Right exit to town
            }
        return {}

    def setup_spawn_points(self):
        """
        Setup spawn points for room transitions.
        When player exits through right side (x=750), they should spawn on left side (x=100) of new room
        When player exits through left side (x=0), they should spawn on right side (x=700) of new room
        """
        if self.room_type == 'town':
            return {
                'shop': (700, 300),    # From shop's left exit, spawn on right
                'dungeon': (100, 300)  # From dungeon's right exit, spawn on left
            }
        elif self.room_type == 'shop':
            return {
                'town': (100, 300)     # From town's right exit, spawn on left
            }
        elif self.room_type == 'dungeon':
            return {
                'town': (700, 300)     # From town's left exit, spawn on right
            }
        return {}

    def check_transition(self, player):
        for exit_room, exit_rect in self.exits.items():
            if player.rect.colliderect(exit_rect):
                print(f"\nRoom transition detected:")
                print(f"Current room: {self.room_type}")
                print(f"Exit to: {exit_room}")
                print(f"Exit rectangle: {exit_rect}")
                print(f"Player position: ({player.x}, {player.y})")
                return exit_room
        return None

    def get_spawn_position(self, previous_room):
        """Get the spawn position when entering from a specific room"""
        spawn_pos = self.spawn_points.get(previous_room, (400, 300))
        print(f"Spawning in {self.room_type} from {previous_room} at position: {spawn_pos}")
        return spawn_pos

    def can_interact_with_shop(self, player):
        return self.room_type == 'shop' and player.rect.colliderect(self.interaction_area)

    def render(self, screen):
        # Draw background
        if self.room_type == 'town':
            bg_color = (0, 100, 0)
        elif self.room_type == 'shop':
            bg_color = (100, 50, 0)
        else:
            bg_color = (50, 50, 50)

        screen.fill(bg_color)

        # Draw exits
        for exit_rect in self.exits.values():
            pygame.draw.rect(screen, (150, 150, 150), exit_rect)

        # Draw shop interaction area and prompt if in shop room
        if self.room_type == 'shop':
            pygame.draw.rect(screen, (120, 80, 40), self.interaction_area, 2)
            if self.shop:
                font = pygame.font.Font(None, 24)
                text = font.render("Press E to interact", True, (255, 255, 255))
                screen.blit(text, (self.interaction_area.centerx - text.get_width() // 2, 
                                self.interaction_area.centery))