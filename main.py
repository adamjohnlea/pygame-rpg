import pygame
import sys
import os
from game.game_state import GameState
from game.menu import Menu
from game.player import Player
from game.room import Room
from game.quest import QuestManager
from game.hud import HUD  # Add import for HUD

class Game:
    def __init__(self):
        print("Initializing game...")
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Python JRPG")
        pygame.font.init()  # Initialize font system
        print("Display initialized")

        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.menu = Menu(self.screen)
        self.hud = HUD()  # Initialize HUD
        print("Game components initialized")
        self.reset_game()

    def reset_game(self):
        print("Resetting game state...")
        # Reset game state
        self.game_state = GameState()

        # Create new player
        print("Creating player...")
        self.player = Player(400, 300)
        print(f"Player initialized at position: ({self.player.x}, {self.player.y})")
        print(f"Player rect: {self.player.rect}")

        # Reset quest manager and start tutorial quest
        self.quest_manager = QuestManager()
        self.quest_manager.start_quest("tutorial_quest")

        # Initialize rooms
        print("Initializing rooms...")
        self.rooms = {
            'town': Room('town', (800, 600)),
            'shop': Room('shop', (800, 600)),
            'dungeon': Room('dungeon', (800, 600))
        }
        self.current_room = 'town'
        print("Game reset completed")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state.toggle_menu()
                if event.key == pygame.K_i:
                    self.game_state.toggle_inventory()
                if event.key == pygame.K_q:
                    self.game_state.toggle_quest_log()
                if event.key == pygame.K_r:
                    self.reset_game()
                if event.key == pygame.K_e and self.current_room == 'shop':
                    current_room = self.rooms[self.current_room]
                    if current_room.can_interact_with_shop(self.player):
                        self.game_state.toggle_shop()

            # Handle shop input when shop is active
            if self.game_state.is_shop_active() and self.current_room == 'shop':
                if self.rooms['shop'].shop.handle_input(event, self.player):
                    # If item was bought, check quest objectives
                    self.quest_manager.check_purchase_objectives(None)
                    # Apply quest rewards if completed
                    self.apply_quest_rewards()

            self.player.handle_input(event)

        return True

    def apply_quest_rewards(self):
        for quest in self.quest_manager.get_active_quests():
            if quest.is_completed() and quest.status != 'rewarded':
                # Apply rewards
                if 'gold' in quest.rewards:
                    self.player.stats['gold'] += quest.rewards['gold']
                if 'items' in quest.rewards:
                    for item in quest.rewards['items']:
                        for _ in range(item.get('quantity', 1)):
                            self.player.inventory.add_item({'id': item['id']})
                if 'stats' in quest.rewards:
                    for stat, value in quest.rewards['stats'].items():
                        self.player.stats[stat] += value
                quest.status = 'rewarded'

    def update(self):
        if not self.game_state.is_menu_active() and not self.game_state.is_shop_active():
            self.player.update()
            self.check_room_transition()
            # Update quest objectives based on current room
            self.quest_manager.check_room_objectives(self.current_room)
            # Check and apply any completed quest rewards
            self.apply_quest_rewards()

    def check_room_transition(self):
        current_room = self.rooms[self.current_room]
        new_room = current_room.check_transition(self.player)
        if new_room and new_room in self.rooms:
            # Store the room we're coming from
            previous_room = self.current_room
            # Change to new room
            self.current_room = new_room
            # Get spawn position for the new room based on where we came from
            try:
                spawn_x, spawn_y = self.rooms[new_room].get_spawn_position(previous_room)
                print(f"Room transition: {previous_room} -> {new_room}")
                print(f"Spawn position: ({spawn_x}, {spawn_y})")
            except AttributeError:
                spawn_x, spawn_y = 400, 300 #Default Spawn
                print(f"Warning: Using default spawn position for {new_room}")

            # Reset player position to the appropriate spawn point
            self.player.reset_position(spawn_x, spawn_y)

    def render(self):
        self.screen.fill((0, 0, 0))

        # Render current room
        self.rooms[self.current_room].render(self.screen)

        # Render player
        if not self.game_state.is_shop_active():
            self.player.render(self.screen)

        # Update and render HUD
        self.hud.update(self.player.stats)
        self.hud.render(self.screen, self.player.stats, self.current_room)

        # Render UI elements
        if self.game_state.is_menu_active():
            self.menu.render()
        if self.game_state.is_inventory_active():
            self.player.inventory.render(self.screen)
        if self.game_state.is_shop_active() and self.current_room == 'shop':
            self.rooms['shop'].shop.render(self.screen)
        if self.game_state.is_quest_log_active():
            self.render_quest_log()

        pygame.display.flip()

    def render_quest_log(self):
        quest_surface = pygame.Surface((400, 300))
        quest_surface.fill((40, 40, 60))
        pygame.draw.rect(quest_surface, (80, 80, 100), (0, 0, 400, 300), 2)

        font = pygame.font.Font(None, 28)
        y_offset = 20

        # Render active quests
        active_quests = self.quest_manager.get_active_quests()
        for quest in active_quests:
            # Quest name
            text = font.render(f"{quest.name}", True, (255, 255, 255))
            quest_surface.blit(text, (20, y_offset))
            y_offset += 30

            # Quest description
            font_small = pygame.font.Font(None, 24)
            text = font_small.render(f"{quest.description}", True, (200, 200, 200))
            quest_surface.blit(text, (30, y_offset))
            y_offset += 25

            # Objectives
            for objective in quest.objectives:
                status = "✓" if objective['completed'] else "○"
                text = font_small.render(f"{status} {objective['description']}", True, 
                                       (100, 255, 100) if objective['completed'] else (200, 200, 200))
                quest_surface.blit(text, (40, y_offset))
                y_offset += 20

            y_offset += 10

        self.screen.blit(quest_surface, (200, 150))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()