from config.settings import *
from os.path import join
from utils.Button import *
from utils.PathHandler import *

class SurrenderModal(pygame.sprite.Sprite):
    def __init__(self, event_manager):
        super().__init__()
        self.elements = pygame.sprite.Group()
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        self.interactive_elements = []
        self.event_manager = event_manager
        self.click_handled = True
        self.practice_mode = False

        self.image = pygame.image.load(resource_path(join("assets", "img", "question.png"))).convert_alpha()
        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2 ))

        self.surrender_message = "You will keep your money.\n\nAre you sure you want to surrender?"
        self.text = TEXT.render(self.surrender_message, True, COLORS["WHITE"])
        self.text_rect = self.text.get_rect(center=self.rect.center)

        self.create_overlay()

        self.no_btn = Button(self.elements, (self.rect.left + 125, self.rect.bottom - 55), event_manager, 'negative_btn', 'No', 'WHITE')
        self.yes_btn = Button(self.elements, (self.rect.right - 125, self.rect.bottom - 55), event_manager, 'btn', 'Yes')

        self.interactive_elements.append(self.no_btn)
        self.interactive_elements.append(self.yes_btn)

    def create_overlay(self):
        self.overlay = pygame.Surface(self.screen.get_size())
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(128)

    def draw(self):
        self.screen.blit(self.overlay, (0, 0))
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)
        self.elements.draw(self.screen)

    def update(self):
        self.elements.update()
        self.update_cursor_state()
        self.check_click()
        self.no_btn.update()
        self.yes_btn.update()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                if self.yes_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
                    if self.practice_mode:
                        self.event_manager.notify("display_practice_summary")
                    else:
                        self.event_manager.notify("display_final_screen")
                self.event_manager.notify("display_surrender_modal")
                self.click_handled = True
        else:
            self.click_handled = False

    def set_practice_mode(self, state):
        self.practice_mode = state

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
        self.create_overlay()
        self.no_btn.update_position((self.rect.left + 125, self.rect.bottom - 55))
        self.yes_btn.update_position((self.rect.right - 125, self.rect.bottom - 55))