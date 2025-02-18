import pygame
import random

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 'player'
        self.combat_log = []
        # Store max number of log entries to prevent unlimited growth
        self.max_log_entries = 8

    def player_attack(self):
        damage = max(1, self.player.stats['attack'] - self.enemy['defense'])
        self.enemy['health'] -= damage
        self.combat_log.append(f"Player deals {damage} damage!")
        if len(self.combat_log) > self.max_log_entries:
            self.combat_log.pop(0)
        self.turn = 'enemy'

    def enemy_attack(self):
        damage = max(1, self.enemy['attack'] - self.player.stats['defense'])
        self.player.stats['health'] -= damage
        self.combat_log.append(f"Enemy deals {damage} damage!")
        if len(self.combat_log) > self.max_log_entries:
            self.combat_log.pop(0)
        self.turn = 'player'

    def is_combat_over(self):
        if self.player.stats['health'] <= 0:
            return 'enemy'
        elif self.enemy['health'] <= 0:
            return 'player'
        return None

    def render(self, screen):
        # Calculate dimensions for 1280x1024
        surface_width = 800  # Reduced from 1200 to fit 1280x1024
        surface_height = 600  # Reduced from 800 to fit 1280x1024
        
        # Draw combat interface
        combat_surface = pygame.Surface((surface_width, surface_height))
        combat_surface.fill((40, 40, 40))
        
        # Draw health bars - adjusted for new dimensions
        bar_width = 250  # Reduced from 400 to fit new surface
        bar_height = 25
        
        # Player health bar
        pygame.draw.rect(combat_surface, (60, 60, 60), (50, 50, bar_width, bar_height))  # Background
        if self.player.stats['health'] > 0:  # Only draw if health > 0
            health_width = int(bar_width * (self.player.stats['health'] / self.player.stats['max_health']))
            pygame.draw.rect(combat_surface, (255, 0, 0), (50, 50, health_width, bar_height))
            
        # Enemy health bar
        pygame.draw.rect(combat_surface, (60, 60, 60), (surface_width - bar_width - 50, 50, bar_width, bar_height))  # Background
        if self.enemy['health'] > 0:  # Only draw if health > 0
            enemy_health_width = int(bar_width * (self.enemy['health'] / self.enemy['max_health']))
            pygame.draw.rect(combat_surface, (255, 0, 0), 
                           (surface_width - bar_width - 50, 50, enemy_health_width, bar_height))

        # Draw combat log with larger font
        font = pygame.font.Font(None, 32)
        for i, log in enumerate(self.combat_log):
            text = font.render(log, True, (255, 255, 255))
            combat_surface.blit(text, (50, 400 + i * 25))

        # Center the combat surface on screen (1280x1024)
        combat_x = (1280 - surface_width) // 2
        combat_y = (1024 - surface_height) // 2
        screen.blit(combat_surface, (combat_x, combat_y))

        # Draw labels
        player_label = font.render("Player", True, (255, 255, 255))
        enemy_label = font.render("Enemy", True, (255, 255, 255))
        combat_surface.blit(player_label, (50, 20))
        combat_surface.blit(enemy_label, (surface_width - enemy_label.get_width() - 50, 20))
