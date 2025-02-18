import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.options = ['Continue', 'Save Game', 'Load Game', 'Quit']
        self.selected_option = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option].lower()
        return None

    def render(self):
        menu_surface = pygame.Surface((300, 400))
        menu_surface.fill((40, 40, 40))
        pygame.draw.rect(menu_surface, (100, 100, 100), (0, 0, 300, 400), 2)

        font = pygame.font.Font(None, 36)
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = font.render(option, True, color)
            menu_surface.blit(text, (20, 50 + i * 50))

        self.screen.blit(menu_surface, (250, 100))
