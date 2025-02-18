import pygame
import random

class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 'player'
        self.combat_log = []

    def player_attack(self):
        damage = max(1, self.player.stats['attack'] - self.enemy['defense'])
        self.enemy['health'] -= damage
        self.combat_log.append(f"Player deals {damage} damage!")
        self.turn = 'enemy'

    def enemy_attack(self):
        damage = max(1, self.enemy['attack'] - self.player.stats['defense'])
        self.player.stats['health'] -= damage
        self.combat_log.append(f"Enemy deals {damage} damage!")
        self.turn = 'player'

    def is_combat_over(self):
        if self.player.stats['health'] <= 0:
            return 'enemy'
        elif self.enemy['health'] <= 0:
            return 'player'
        return None

    def render(self, screen):
        # Draw combat interface
        combat_surface = pygame.Surface((600, 400))
        combat_surface.fill((40, 40, 40))
        
        # Draw health bars
        pygame.draw.rect(combat_surface, (255, 0, 0), (50, 50, 200 * (self.player.stats['health'] / self.player.stats['max_health']), 20))
        pygame.draw.rect(combat_surface, (255, 0, 0), (350, 50, 200 * (self.enemy['health'] / self.enemy['max_health']), 20))

        # Draw combat log
        font = pygame.font.Font(None, 24)
        for i, log in enumerate(self.combat_log[-5:]):
            text = font.render(log, True, (255, 255, 255))
            combat_surface.blit(text, (50, 300 + i * 20))

        screen.blit(combat_surface, (100, 100))
