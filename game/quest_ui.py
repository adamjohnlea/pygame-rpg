import pygame

class QuestUI:
    def __init__(self):
        self.current_notification = None
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)
        self.selected_quest_index = 0  # Track selected quest

    def show_notification(self, message):
        self.current_notification = message

    def handle_input(self, event, quests):
        if not quests:
            return None
            
        if event.type == pygame.KEYDOWN:
            # Handle notification dismissal
            if event.key == pygame.K_SPACE and self.current_notification:
                self.current_notification = None
                return None
                
            # Handle quest selection
            if event.key == pygame.K_UP:
                self.selected_quest_index = (self.selected_quest_index - 1) % len(quests)
            elif event.key == pygame.K_DOWN:
                self.selected_quest_index = (self.selected_quest_index + 1) % len(quests)
            elif event.key == pygame.K_RETURN:
                return quests[self.selected_quest_index]
        return None

    def render_notification(self, screen):
        if self.current_notification:
            # Create notification surface with alpha channel
            lines = self.current_notification.split('\n')
            line_height = 30
            height = (len(lines) + 1) * line_height + 20  # Extra space for dismiss instruction
            notif_surface = pygame.Surface((600, height), pygame.SRCALPHA)
            
            # Fill with semi-transparent background
            pygame.draw.rect(notif_surface, (40, 40, 60, 230), (0, 0, 600, height))
            pygame.draw.rect(notif_surface, (80, 80, 100, 255), (0, 0, 600, height), 2)

            # Render each line
            y_offset = 10
            for line in lines:
                # Create text surface
                text = self.font.render(line.strip(), True, (255, 255, 255))
                # Center text
                text_rect = text.get_rect(centerx=300, y=y_offset)
                notif_surface.blit(text, text_rect)
                y_offset += line_height

            # Add dismiss instruction
            dismiss_text = self.small_font.render("Press SPACE to dismiss", True, (200, 200, 200))
            dismiss_rect = dismiss_text.get_rect(centerx=300, y=y_offset)
            notif_surface.blit(dismiss_text, dismiss_rect)

            # Position at top center of screen
            x = (screen.get_width() - notif_surface.get_width()) // 2
            screen.blit(notif_surface, (x, 20))
            
            # Debug print
            print(f"Rendering notification: {self.current_notification}")

    def render_available_quests(self, screen, quests):
        if not quests:
            return

        # Create quest list surface
        quest_surface = pygame.Surface((400, 300))
        quest_surface.fill((40, 40, 60))
        pygame.draw.rect(quest_surface, (80, 80, 100), (0, 0, 400, 300), 2)

        # Title
        title = self.font.render("Available Quests", True, (255, 255, 255))
        quest_surface.blit(title, (20, 20))

        # Instructions
        instructions = self.small_font.render("Use UP/DOWN to select, ENTER to accept", True, (200, 200, 200))
        quest_surface.blit(instructions, (20, 45))

        # Render each quest
        y_offset = 80
        for i, quest in enumerate(quests):
            # Highlight selected quest
            if i == self.selected_quest_index:
                pygame.draw.rect(quest_surface, (60, 60, 80), (10, y_offset - 5, 380, 65))
                
            # Quest name
            name_text = self.font.render(quest.name, True, (200, 200, 255))
            quest_surface.blit(name_text, (20, y_offset))
            y_offset += 25

            # Quest description
            desc_text = self.small_font.render(quest.description, True, (200, 200, 200))
            quest_surface.blit(desc_text, (30, y_offset))
            y_offset += 20

            # Quest rewards
            rewards_text = self.small_font.render(f"Rewards: {quest.get_reward_description()}", True, (150, 255, 150))
            quest_surface.blit(rewards_text, (30, y_offset))
            y_offset += 35

        # Draw at center of screen
        x = (screen.get_width() - quest_surface.get_width()) // 2
        y = (screen.get_height() - quest_surface.get_height()) // 2
        screen.blit(quest_surface, (x, y)) 