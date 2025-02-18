import pygame
import math

class HUD:
    def __init__(self):
        self.animated_health = 100
        self.animated_gold = 100
        self.health_animation_speed = 0.1  # Keep health animation slower
        self.gold_animation_speed = 0.5    # Make gold animation faster
        self.header_height = 50  # Slightly taller header for 1080p
        self.font = pygame.font.Font(None, 32)  # Larger font for 1080p
        # Gold coin colors
        self.coin_color = (255, 215, 0)  # Golden yellow
        self.coin_border = (218, 165, 32)  # Darker gold
        self.coin_radius = 10  # Slightly larger coin for 1080p

    def draw_gold_coin(self, screen, x, y):
        # Draw the main coin circle
        pygame.draw.circle(screen, self.coin_color, (x, y), self.coin_radius)
        # Draw border
        pygame.draw.circle(screen, self.coin_border, (x, y), self.coin_radius, 1)
        # Draw a simple '$' or 'G' in the middle
        mini_font = pygame.font.Font(None, 16)
        symbol = mini_font.render("G", True, self.coin_border)
        symbol_rect = symbol.get_rect(center=(x, y))
        screen.blit(symbol, symbol_rect)

    def update(self, player_stats):
        # Smoothly animate health changes
        target_health = player_stats['health']
        if self.animated_health != target_health:
            diff = target_health - self.animated_health
            self.animated_health += diff * self.health_animation_speed

        # Smoothly animate gold changes
        target_gold = player_stats['gold']
        if self.animated_gold != target_gold:
            diff = target_gold - self.animated_gold
            self.animated_gold += diff * self.gold_animation_speed
            # If we're very close to target, just snap to it
            if abs(self.animated_gold - target_gold) < 1:
                self.animated_gold = target_gold

    def render(self, screen, player_stats, current_room):
        # Create a semi-transparent surface for the header bar
        header_surface = pygame.Surface((1280, self.header_height))
        header_surface.fill((20, 22, 24))
        header_surface.set_alpha(230)

        # Draw header bar background
        screen.blit(header_surface, (0, 0))

        # Draw health bar background
        health_bar_width = 300  # Wider health bar for 1080p
        pygame.draw.rect(screen, (40, 40, 40), (20, 15, health_bar_width, 25))

        # Calculate health percentage and color
        health_percent = self.animated_health / player_stats['max_health']
        health_width = int(health_bar_width * health_percent)
        
        # Interpolate color from red to green based on health
        health_color = (
            int(255 * (1 - health_percent)),  # Red component
            int(255 * health_percent),        # Green component
            0                                 # Blue component
        )

        # Draw animated health bar
        pygame.draw.rect(screen, health_color, (20, 15, health_width, 25))
        
        # Draw health text
        health_text = self.font.render(
            f"{int(self.animated_health)}/{player_stats['max_health']} HP", 
            True, (255, 255, 255)
        )
        screen.blit(health_text, (330, 15))

        # Draw custom gold coin and amount
        self.draw_gold_coin(screen, 650, 25)  # Adjusted position for 1080p
        gold_text = self.font.render(
            str(int(self.animated_gold)), True, self.coin_color
        )
        screen.blit(gold_text, (670, 15))  # Adjusted position for 1080p

        # Draw room name with a background highlight
        room_text = self.font.render(current_room.capitalize(), True, (200, 200, 255))
        text_width = room_text.get_width()
        
        # Draw a subtle background for the room name
        pygame.draw.rect(screen, (40, 44, 52), 
                        (960, 10, text_width + 20, 35),  # Adjusted for 1280x1024
                        border_radius=5)
        screen.blit(room_text, (970, 15))  # Adjusted for 1280x1024
