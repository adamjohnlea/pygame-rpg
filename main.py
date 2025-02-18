import pygame
import sys
import os
from game.game_state import GameState
from game.menu import Menu
from game.player import Player
from game.room import Room
from game.quest import QuestManager
from game.quest_ui import QuestUI
from game.hud import HUD
from game.combat import Combat

class Game:
    def __init__(self):
        print("Initializing game...")
        self.screen = pygame.display.set_mode((1280, 1024))
        pygame.display.set_caption("Python JRPG")
        pygame.font.init()
        print("Display initialized")

        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.menu = Menu(self.screen)
        self.hud = HUD()
        self.quest_ui = QuestUI()
        self.combat = None
        print("Game components initialized")
        self.reset_game()

    def reset_game(self):
        print("Resetting game state...")
        self.game_state = GameState()
        self.player = Player(640, 512)  # Center of 1280x1024
        self.quest_manager = QuestManager()
        self.rooms = {
            'town': Room('town', (1280, 1024)),
            'shop': Room('shop', (1280, 1024)),
            'dungeon': Room('dungeon', (1280, 1024))
        }
        self.current_room = 'town'
        print("Game reset completed")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Handle notification dismissal first
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.quest_ui.current_notification:
                    self.quest_ui.current_notification = None
                    continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state.is_combat_active():
                        self.game_state.toggle_combat()
                        self.combat = None
                    else:
                        self.game_state.toggle_menu()
                if event.key == pygame.K_i and not self.game_state.is_combat_active():
                    self.game_state.toggle_inventory()
                if event.key == pygame.K_q and not self.game_state.is_combat_active():
                    self.game_state.toggle_quest_log()
                if event.key == pygame.K_j and not self.game_state.is_combat_active():
                    available_quests = self.quest_manager.get_available_quests()
                    if available_quests:
                        self.game_state.toggle_available_quests()
                    else:
                        self.quest_ui.show_notification("No quests available!\nComplete current quests to unlock more.")
                if event.key == pygame.K_r:
                    self.reset_game()
                if event.key == pygame.K_e:
                    if self.current_room == 'shop':
                        current_room = self.rooms[self.current_room]
                        if current_room.can_interact_with_shop(self.player):
                            self.game_state.toggle_shop()
                    elif self.current_room == 'dungeon':
                        current_room = self.rooms[self.current_room]
                        if current_room.can_interact_with_enemy(self.player):
                            self.start_combat(current_room.enemy)

            # Handle inventory input when inventory is active
            if self.game_state.is_inventory_active():
                success, message = self.player.inventory.handle_input(event, self.player)
                if message:  # Show message if item was used or there was an error
                    self.quest_ui.show_notification(message)
                if success:  # Close inventory if item was used successfully
                    self.game_state.toggle_inventory()

            # Handle combat input
            if self.game_state.is_combat_active() and self.combat:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.combat.turn == 'player':
                        self.combat.player_attack()
                        # Check if combat is over after player attacks
                        result = self.combat.is_combat_over()
                        if result:
                            if result == 'player':
                                self.quest_ui.show_notification("Victory!")
                                self.rooms[self.current_room].enemy_active = False
                            else:
                                self.quest_ui.show_notification("Defeat!")
                            self.game_state.toggle_combat()
                            self.combat = None
                        else:
                            # Enemy attacks after a brief delay
                            self.combat.enemy_attack()
                            # Check if combat is over after enemy attacks
                            result = self.combat.is_combat_over()
                            if result:
                                if result == 'player':
                                    self.quest_ui.show_notification("Victory!")
                                    self.rooms[self.current_room].enemy_active = False
                                else:
                                    self.quest_ui.show_notification("Defeat!")
                                self.game_state.toggle_combat()
                                self.combat = None

            # Handle other inputs...
            if self.game_state.is_available_quests_active():
                selected_quest = self.quest_ui.handle_input(event, self.quest_manager.get_available_quests())
                if selected_quest:
                    if self.quest_manager.accept_quest(selected_quest.id):
                        self.quest_ui.show_notification(f"Accepted Quest: {selected_quest.name}")
                        self.game_state.toggle_available_quests()

            if self.game_state.is_shop_active() and self.current_room == 'shop':
                success, message = self.rooms['shop'].shop.handle_input(event, self.player)
                if success:
                    self.quest_manager.check_purchase_objectives(None)
                elif message:
                    self.quest_ui.show_notification(message)

            if not self.game_state.is_combat_active():
                self.player.handle_input(event)

        return True

    def start_combat(self, enemy):
        """Initialize combat with an enemy."""
        self.combat = Combat(self.player, enemy)
        self.game_state.toggle_combat()
        self.quest_ui.show_notification("Combat started! Press SPACE to attack.")

    def update(self):
        if not self.game_state.is_menu_active() and not self.game_state.is_shop_active():
            self.player.update()
            self.check_room_transition()
            self.quest_manager.check_room_objectives(self.current_room)
            
            # Apply quest rewards and show notifications
            self.quest_manager.apply_rewards(self.player)
            if self.quest_manager.has_pending_rewards():
                reward_message = self.quest_manager.get_next_reward_message()
                if reward_message:
                    self.quest_ui.show_notification(reward_message)

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
                spawn_x, spawn_y = 640, 512  # Default spawn at center of 1280x1024
                print(f"Warning: Using default spawn position for {new_room}")

            # Reset player position to the appropriate spawn point
            self.player.reset_position(spawn_x, spawn_y)

    def render(self):
        self.screen.fill((0, 0, 0))
        
        # Only render room and player if not in combat
        if not self.game_state.is_combat_active():
            self.rooms[self.current_room].render(self.screen)
            if not self.game_state.is_shop_active():
                self.player.render(self.screen)

        self.hud.update(self.player.stats)
        self.hud.render(self.screen, self.player.stats, self.current_room)

        # Render combat if active
        if self.game_state.is_combat_active() and self.combat:
            self.combat.render(self.screen)

        if self.game_state.is_menu_active():
            self.menu.render()
        if self.game_state.is_inventory_active():
            self.player.inventory.render(self.screen)
        if self.game_state.is_shop_active() and self.current_room == 'shop':
            self.rooms['shop'].shop.render(self.screen)
        if self.game_state.is_quest_log_active():
            self.render_quest_log()
        if self.game_state.is_available_quests_active():
            self.quest_ui.render_available_quests(self.screen, self.quest_manager.get_available_quests())

        # Render any active notifications
        self.quest_ui.render_notification(self.screen)

        pygame.display.flip()

    def render_quest_log(self):
        quest_surface = pygame.Surface((600, 500))  # Larger quest log
        quest_surface.fill((40, 40, 60))
        pygame.draw.rect(quest_surface, (80, 80, 100), (0, 0, 600, 500), 2)

        font = pygame.font.Font(None, 32)  # Slightly larger font
        y_offset = 20

        # Render active quests
        active_quests = self.quest_manager.get_active_quests()
        for quest in active_quests:
            # Quest name
            text = font.render(f"{quest.name}", True, (255, 255, 255))
            quest_surface.blit(text, (20, y_offset))
            y_offset += 35

            # Quest description
            font_small = pygame.font.Font(None, 28)
            text = font_small.render(f"{quest.description}", True, (200, 200, 200))
            quest_surface.blit(text, (30, y_offset))
            y_offset += 30

            # Objectives
            for objective in quest.objectives:
                status = "✓" if objective['completed'] else "○"
                text = font_small.render(f"{status} {objective['description']}", True, 
                                       (100, 255, 100) if objective['completed'] else (200, 200, 200))
                quest_surface.blit(text, (40, y_offset))
                y_offset += 25

            y_offset += 15

        # Center the quest log on screen
        self.screen.blit(quest_surface, (340, 262))  # Centered position for 1280x1024

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