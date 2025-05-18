from config.settings import *
from os.path import join
from utils.Button import *

class NoData(pygame.sprite.Sprite):
    def __init__(self, event_manager):
        super().__init__()
        self.elements = pygame.sprite.Group()
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()

        self.image = pygame.image.load(join("assets", "img", "question.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(self.width//2, self.height//2))

        self.click_handled = True
        self.event_manager = event_manager
        self.interactive_elements = []

        self.back_btn = Button(self.elements, (self.rect.left + 125, self.rect.bottom - 55), event_manager, 'negative_btn', 'Go Back', 'WHITE')

        self.interactive_elements.append(self.back_btn)

        self.update_text()

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)
        self.elements.draw(self.screen)

    def update(self):
        self.elements.update()
        self.check_click()
        self.update_cursor_state()

    def update_text(self):
        self.message = f"No questions found"
        self.text = TEXT.render(self.message, True, COLORS["WHITE"])
        self.text_rect = self.text.get_rect(center=self.rect.center)


    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.back_btn.check_notify_state("menu")
                self.click_handled = True
        else:
            self.click_handled = False

    def update_cursor_state(self):
        hover_detected = False
        for element in self.interactive_elements:
            if element.rect.collidepoint(pygame.mouse.get_pos()):
                if not hover_detected:
                    element.on_hover()
                    self.event_manager.notify("change_cursor", 'hover')
                    hover_detected = True
            else:
                element.reset_hover()

        if not hover_detected:
            self.event_manager.notify("change_cursor", 'default')

    def update_position(self):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2))
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.back_btn.update_position((self.rect.left + 125, self.rect.bottom - 55))