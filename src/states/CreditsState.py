from config.settings import *
from .State import *
from utils.Box import *
from utils.Button import *

class Credits(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.box = Box(self.elements)
        box_rect = self.box.get_rect()

        self.setup_positions(box_rect)
        self.setup_text_elements()
        self.setup_buttons( box_rect)

    def setup_positions(self, box_rect):
        self.TITLE_POSITION = (box_rect.centerx, box_rect.top + 50)
        self.SUB_TITLE_1_POSITION = (box_rect.centerx, box_rect.top + 125)
        self.SUB_TITLE_2_POSITION = (box_rect.centerx, box_rect.top + 225)
        self.TEXT_1_POSITION = (box_rect.centerx, box_rect.top + 175)
        self.TEXT_2_POSITION = (box_rect.centerx, box_rect.top + 300)

    def setup_text_elements(self):
        self.text_elements = [
            (TITLE.render("Credits", True, COLORS["AMBER"]), self.TITLE_POSITION),
            (SUB_TITLE.render("Developer", True, COLORS["AMBER"]), self.SUB_TITLE_1_POSITION),
            (SUB_TITLE.render("Contributors", True, COLORS["AMBER"]), self.SUB_TITLE_2_POSITION),
            (TEXT.render(DEVELOPER, True, COLORS["WHITE"]), self.TEXT_1_POSITION),
            (TEXT.render(CONTRIBUTORS, True, COLORS["WHITE"]), self.TEXT_2_POSITION)
        ]

    def setup_buttons(self,  box_rect):
        self.back_btn = Button(self.elements, (box_rect.left + 150, box_rect.bottom - 75), self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.interactive_elements.append(self.back_btn)

    def draw(self):
        self.elements.draw(self.screen)
        self.draw_text_elements()

    def draw_text_elements(self):
        for text_surface, position in self.text_elements:
            text_rect = text_surface.get_rect(center=position)
            self.screen.blit(text_surface, text_rect)

    def update(self):
        self.elements.update()
        self.update_cursor_state()
        self.check_click()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.back_btn.check_notify_state("menu")
                self.click_handled = True
        else:
            self.click_handled = False

    def update_size(self, *args):
        self.box.updates_position()
        box_rect = self.box.get_rect()
        self.back_btn.update_position((box_rect.left + 150, box_rect.bottom - 75))
        self.setup_positions(box_rect)
        self.setup_text_elements()

    def set_up_credits_events(self):
        self.event_manager.subscribe("update_size", self.update_size)
        
