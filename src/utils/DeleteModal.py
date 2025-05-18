from config.settings import *
from os.path import join
from utils.Button import *
class DeleteModal(pygame.sprite.Sprite):
    def __init__(self, event_manager):
        super().__init__()
        self.elements = pygame.sprite.Group()
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()

        self.id = ''

        self.image = pygame.image.load(join("assets", "img", "question.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(self.width//2, self.height//2))

        self.message = "Are you sure you want to delete the question?"
        self.text = TEXT.render(self.message, True, COLORS["WHITE"])
        self.text_rect = self.text.get_rect(center=(self.width//2, self.height//2))

        self.event_manager = event_manager
        self.interactive_elements = []
        self.click_handled = True

        self.create_overlay()
        self.display = False

        self.no_btn = Button(self.elements, (self.rect.left + 125, self.rect.bottom - 55), event_manager, 'negative_btn', 'No', 'WHITE')
        self.yes_btn = Button(self.elements, (self.rect.right - 125, self.rect.bottom - 55), event_manager, 'btn', 'Yes')

        self.interactive_elements.append(self.no_btn)
        self.interactive_elements.append(self.yes_btn)

    def create_overlay(self):
        self.overlay = pygame.Surface(self.screen.get_size())
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(128)

    def draw(self):
        if self.display:
            self.screen.blit(self.overlay, (0, 0))
            self.screen.blit(self.image, self.rect)
            self.screen.blit(self.text, self.text_rect)
            self.elements.draw(self.screen)

    def update(self):
        if self.display:
            self.elements.update()
            self.update_cursor_state()
            self.check_click()

    def set_id(self, id):
        self.id = id

    def show_modal(self):
        self.display = True

    def hide_modal(self):
        self.display = False

    def is_open(self):
        return self.display

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                if self.no_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
                    self.hide_modal()
                if self.yes_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
                    self.event_manager.notify("delete", self.id)
                    self.event_manager.notify("load_data")
                    self.event_manager.notify("fetch_questions")
                    self.hide_modal()
                self.click_handled = True
        else:
            self.click_handled = False

    def update_position(self):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        self.rect = self.image.get_rect(center=(self.width // 2, self.height // 2))
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.create_overlay()
        self.no_btn.update_position((self.rect.left + 125, self.rect.bottom - 55))
        self.yes_btn.update_position((self.rect.right - 125, self.rect.bottom - 55))


    def update_cursor_state(self):
        for element in self.interactive_elements:
            if element.rect.collidepoint(pygame.mouse.get_pos()):
                self.event_manager.notify("change_cursor", 'hover')
                break
        else:
            self.event_manager.notify("change_cursor", 'default')