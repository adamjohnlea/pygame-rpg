import pygame
import math

class HUD:
    def __init__(self):
        self.animated_health = 100
        self.animated_gold = 100
        self.animation_speed = 0.1
        self.header_height = 40
        self.font = pygame.font.Font(None, 28)

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

        # Draw gold with animation
        gold_icon = "⚜"  # Unicode symbol for gold
        gold_text = self.font.render(
            f"{gold_icon} {int(self.animated_gold)}", True, (255, 215, 0)
        )
        screen.blit(gold_text, (350, 10))

        # Draw room name with a background highlight
        room_text = self.font.render(current_room.capitalize(), True, (200, 200, 255))
        text_width = room_text.get_width()
        
        # Draw a subtle background for the room name
        pygame.draw.rect(screen, (40, 44, 52), 
                        (600, 5, text_width + 20, 30), 
                        border_radius=5)
        screen.blit(room_text, (610, 10))
