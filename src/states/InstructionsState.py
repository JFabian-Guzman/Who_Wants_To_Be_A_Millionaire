from config.settings import *
from os.path import join
from .State import *
from utils.Box import *
from utils.Button import *

class Instructions(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.box = Box(self.elements)
        box_rect = self.box.get_rect()

        self.setup_positions(box_rect)
        self.setup_text_elements()
        self.setup_buttons(event_manager)

        self.display_continue = True
        self.click_handled = False

    def setup_positions(self, box_rect):
        self.INSTRUCTIONS_TITLE_POSITION = (box_rect.centerx, box_rect.top + 50)
        self.INSTRUCTIONS_POSITION = (box_rect.centerx, box_rect.centery - 20)

    def setup_text_elements(self):
        self.title = TITLE.render("Instructions", True, COLORS["AMBER"])
        self.title_rect = self.title.get_rect(center=self.INSTRUCTIONS_TITLE_POSITION)

        self.instructions = TEXT.render(INSTRUCTIONS, True, COLORS["WHITE"])
        self.instructions_rect = self.instructions.get_rect(center=self.INSTRUCTIONS_POSITION)

    def setup_buttons(self, event_manager):
        self.continue_btn = Button(None, RIGHT_BTN_POSITION, event_manager)
        self.back_btn = Button(self.elements, LEFT_BTN_POSITION, event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.interactive_elements.append(self.continue_btn)
        self.interactive_elements.append(self.back_btn)

    def draw(self):
        self.elements.draw(self.screen)
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.instructions, self.instructions_rect)
        if self.display_continue:
            self.continue_btn.draw()
            self.continue_btn.update()

    def update(self):
        self.elements.update()
        self.check_click()
        self.update_cursor_state()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.continue_btn.check_notify_state("rewards")
                self.back_btn.check_notify_state("player")
                self.click_handled = True
        else:
            self.click_handled = False

    def display_continue_btn(self, *args):
        self.display_continue = True

    def erase_continue_btn(self, *args):
        self.display_continue = False

    def set_up_instruction_events(self):
        self.event_manager.subscribe("display_continue_btn", self.display_continue_btn)
        self.event_manager.subscribe("erase_continue_btn", self.erase_continue_btn)