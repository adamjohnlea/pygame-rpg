import pygame

class Room:
    def __init__(self, room_type, size):
        self.room_type = room_type
        self.width, self.height = size
        self.exits = self.setup_exits()
        self.spawn_points = self.setup_spawn_points()
        self.objects = []
        self.shop = None
        # Center the shop interaction area horizontally (1280/2 - width/2)
        self.interaction_area = pygame.Rect(490, 412, 300, 200)
        
        # Initialize room-specific elements
        if room_type == 'shop':
            from .shop import Shop
            self.shop = Shop()
        elif room_type == 'dungeon':
            self.enemy = {
                'health': 100,
                'max_health': 100,
                'attack': 8,
                'defense': 3,
                'name': 'Dungeon Slime'
            }
            # Create enemy interaction area in center of dungeon
            self.enemy_area = pygame.Rect(540, 412, 200, 200)
            self.enemy_active = True  # Track if enemy is alive

    def setup_exits(self):
        """Setup exit rectangles for each room. Exits are 80 pixels wide and 160 pixels tall."""
        if self.room_type == 'town':
            return {
                'shop': pygame.Rect(self.width - 80, 432, 80, 160),    # Right exit to shop
                'dungeon': pygame.Rect(0, 432, 80, 160)                 # Left exit to dungeon
            }
        elif self.room_type == 'shop':
            return {
                'town': pygame.Rect(0, 432, 80, 160)                    # Left exit to town
            }
        elif self.room_type == 'dungeon':
            return {
                'town': pygame.Rect(self.width - 80, 432, 80, 160)     # Right exit to town
            }
        return {}

    def setup_spawn_points(self):
        """
        Setup spawn points for room transitions.
        Spawn points are positioned just inside the opposite side of where the player entered,
        and at the same height as the exit's center (432 + 160/2 = 512).
        """
        if self.room_type == 'town':
            return {
                'shop': (self.width - 120, 512),    # From shop (left exit), spawn near right
                'dungeon': (120, 512)               # From dungeon (right exit), spawn near left
            }
        elif self.room_type == 'shop':
            return {
                'town': (120, 512)                  # From town (right exit), spawn near left
            }
        elif self.room_type == 'dungeon':
            return {
                'town': (self.width - 120, 512)     # From town (left exit), spawn near right
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
        spawn_pos = self.spawn_points.get(previous_room, (self.width // 2, self.height // 2))
        print(f"Spawning in {self.room_type} from {previous_room} at position: {spawn_pos}")
        return spawn_pos

    def can_interact_with_shop(self, player):
        return self.room_type == 'shop' and player.rect.colliderect(self.interaction_area)

    def can_interact_with_enemy(self, player):
        return (self.room_type == 'dungeon' and 
                self.enemy_active and 
                player.rect.colliderect(self.enemy_area))

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

        # Draw enemy and interaction prompt in dungeon
        if self.room_type == 'dungeon' and self.enemy_active:
            # Draw enemy area
            pygame.draw.rect(screen, (200, 50, 50), self.enemy_area, 2)
            # Draw enemy (simple rectangle for now)
            pygame.draw.rect(screen, (200, 50, 50), 
                           (self.enemy_area.centerx - 20, self.enemy_area.centery - 20, 40, 40))
            
            # Draw interaction prompt when player is near
            font = pygame.font.Font(None, 24)
            text = font.render("Press E to fight", True, (255, 255, 255))
            screen.blit(text, (self.enemy_area.centerx - text.get_width() // 2,
                             self.enemy_area.centery - 50))