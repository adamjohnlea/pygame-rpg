import pygame

class QuestUI:
    def __init__(self):
        self.notification_time = 0
        self.notification_duration = 3000  # 3 seconds
        self.current_notification = None
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 24)

    def show_notification(self, message):
        self.current_notification = message
        self.notification_time = pygame.time.get_ticks()

    def update(self):
        if self.current_notification:
            if pygame.time.get_ticks() - self.notification_time > self.notification_duration:
                self.current_notification = None

    def render_notification(self, screen):
        if self.current_notification:
            # Create notification surface
            lines = self.current_notification.split('\n')
            line_height = 30
            height = (len(lines) + 1) * line_height
            notif_surface = pygame.Surface((600, height))
            notif_surface.fill((40, 40, 60))
            pygame.draw.rect(notif_surface, (80, 80, 100), (0, 0, 600, height), 2)

            # Render each line
            for i, line in enumerate(lines):
                text = self.font.render(line, True, (255, 255, 255))
                notif_surface.blit(text, (20, i * line_height + 10))

            # Add fade effect based on time
            alpha = 255
            time_shown = pygame.time.get_ticks() - self.notification_time
            if time_shown > self.notification_duration - 500:  # Start fading 0.5s before end
                alpha = max(0, 255 * (self.notification_duration - time_shown) / 500)
            notif_surface.set_alpha(alpha)

            # Position at top center of screen
            x = (screen.get_width() - notif_surface.get_width()) // 2
            screen.blit(notif_surface, (x, 20))

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

        # Render each quest
        y_offset = 60
        for quest in quests:
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