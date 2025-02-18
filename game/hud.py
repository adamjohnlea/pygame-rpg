import pygame
import math

class HUD:
    def __init__(self):
        self.animated_health = 100
        self.animated_gold = 100
        self.animation_speed = 0.1
        self.header_height = 40
        self.font = pygame.font.Font(None, 28)
        # Gold coin colors
        self.coin_color = (255, 215, 0)  # Golden yellow
        self.coin_border = (218, 165, 32)  # Darker gold
        self.coin_radius = 8

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
            self.animated_health += diff * self.animation_speed

        # Smoothly animate gold changes
        target_gold = player_stats['gold']
        if self.animated_gold != target_gold:
            diff = target_gold - self.animated_gold
            self.animated_gold += diff * self.animation_speed

    def render(self, screen, player_stats, current_room):
        # Create a semi-transparent surface for the header bar
        header_surface = pygame.Surface((800, self.header_height))
        header_surface.fill((20, 22, 24))
        header_surface.set_alpha(230)

        # Draw header bar background
        screen.blit(header_surface, (0, 0))

        # Draw health bar background
        health_bar_width = 150
        pygame.draw.rect(screen, (40, 40, 40), (10, 10, health_bar_width, 20))

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
        pygame.draw.rect(screen, health_color, (10, 10, health_width, 20))
        
        # Draw health text
        health_text = self.font.render(
            f"{int(self.animated_health)}/{player_stats['max_health']} HP", 
            True, (255, 255, 255)
        )
        screen.blit(health_text, (170, 10))

        # Draw custom gold coin and amount
        self.draw_gold_coin(screen, 350, 20)  # Draw coin at y=20 to center it vertically
        gold_text = self.font.render(
            str(int(self.animated_gold)), True, self.coin_color
        )
        screen.blit(gold_text, (365, 10))  # Adjusted x position to account for coin

        # Draw room name with a background highlight
        room_text = self.font.render(current_room.capitalize(), True, (200, 200, 255))
        text_width = room_text.get_width()
        
        # Draw a subtle background for the room name
        pygame.draw.rect(screen, (40, 44, 52), 
                        (600, 5, text_width + 20, 30), 
                        border_radius=5)
        screen.blit(room_text, (610, 10))
