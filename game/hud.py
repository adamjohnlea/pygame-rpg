import pygame
import math

class HUD:
    def __init__(self):
        # Animation values
        self.animated_health = 100
        self.animated_stamina = 100  # New stat
        self.animated_gold = 100
        
        # Animation speeds
        self.health_animation_speed = 0.1
        self.stamina_animation_speed = 0.15
        self.gold_animation_speed = 0.5
        
        # Layout
        self.header_height = 80  # Increased height to fit all elements
        self.padding = 8  # Slightly reduced padding
        self.bar_height = 20  # Slightly smaller bars
        self.bar_spacing = 24  # Reduced spacing between bars
        
        # Fonts
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        # Colors
        self.colors = {
            'bar_bg': (40, 40, 40, 180),  # Added alpha for transparency
            'health_full': (220, 50, 50),    # Red for health
            'stamina_full': (50, 150, 220),  # Blue for stamina
            'gold': (255, 215, 0),
            'gold_border': (218, 165, 32),
            'text': (255, 255, 255),
            'text_shadow': (0, 0, 0),
            'location_bg': (40, 44, 52, 180),  # Added alpha for transparency
            'location_text': (200, 200, 255)
        }

    def draw_stat_bar(self, surface, x, y, width, current, maximum, color, label):
        # Draw background with rounded corners
        pygame.draw.rect(surface, self.colors['bar_bg'], 
                        (x, y, width, self.bar_height), 
                        border_radius=3)
        
        # Draw the filled portion with rounded corners
        fill_width = int(width * (current / maximum))
        if fill_width > 0:  # Only draw if there's something to fill
            pygame.draw.rect(surface, color, 
                           (x, y, fill_width, self.bar_height),
                           border_radius=3)
        
        # Draw text with shadow effect
        text = self.font.render(f"{label}: {int(current)}/{maximum}", True, self.colors['text_shadow'])
        surface.blit(text, (x + 2, y + 2))  # Shadow
        text = self.font.render(f"{label}: {int(current)}/{maximum}", True, self.colors['text'])
        surface.blit(text, (x, y))

    def draw_gold_display(self, surface, x, y):
        # Draw coin icon
        pygame.draw.circle(surface, self.colors['gold'], (x, y + self.bar_height//2), 10)
        pygame.draw.circle(surface, self.colors['gold_border'], (x, y + self.bar_height//2), 10, 1)
        
        # Draw 'G' symbol
        symbol = self.small_font.render("G", True, self.colors['gold_border'])
        symbol_rect = symbol.get_rect(center=(x, y + self.bar_height//2))
        surface.blit(symbol, symbol_rect)
        
        # Draw amount
        gold_text = self.font.render(str(int(self.animated_gold)), True, self.colors['gold'])
        surface.blit(gold_text, (x + 20, y))

    def draw_location_display(self, surface, room_name, width):
        room_text = self.font.render(room_name.capitalize(), True, self.colors['location_text'])
        text_width = room_text.get_width()
        text_height = room_text.get_height()
        
        # Position the location display on the right
        x = width - text_width - self.padding * 4
        
        # Calculate background rectangle with more padding in both directions
        bg_rect = pygame.Rect(x - self.padding * 2, self.padding,
                            text_width + self.padding * 4, 
                            text_height + self.padding * 3)  # Increased vertical padding
        
        # Draw simple background
        pygame.draw.rect(surface, (30, 33, 40, 160), bg_rect, border_radius=5)
        
        # Draw text centered in the background
        text_y = bg_rect.y + (bg_rect.height - text_height) // 2
        surface.blit(room_text, (x, text_y))

    def update(self, player_stats):
        # Update health animation
        if self.animated_health != player_stats['health']:
            diff = player_stats['health'] - self.animated_health
            self.animated_health += diff * self.health_animation_speed

        # Update stamina animation
        if self.animated_stamina != player_stats['stamina']:
            diff = player_stats['stamina'] - self.animated_stamina
            self.animated_stamina += diff * self.stamina_animation_speed

        # Update gold animation
        if self.animated_gold != player_stats['gold']:
            diff = player_stats['gold'] - self.animated_gold
            self.animated_gold += diff * self.gold_animation_speed
            if abs(self.animated_gold - player_stats['gold']) < 1:
                self.animated_gold = player_stats['gold']

    def render(self, screen, player_stats, current_room):
        # Create UI elements surface with alpha channel
        ui_surface = pygame.Surface((1280, self.header_height), pygame.SRCALPHA)
        
        # Draw stat bars
        self.draw_stat_bar(ui_surface, self.padding, self.padding, 
                          300, self.animated_health, player_stats['max_health'],
                          self.colors['health_full'], "Health")
        
        self.draw_stat_bar(ui_surface, self.padding, self.padding + self.bar_spacing,
                          300, self.animated_stamina, player_stats['max_stamina'],
                          self.colors['stamina_full'], "Stamina")
        
        # Draw gold display
        self.draw_gold_display(ui_surface, 350, self.padding)
        
        # Draw location display
        self.draw_location_display(ui_surface, current_room, 1280)
        
        # Render to screen
        screen.blit(ui_surface, (0, 0))
