from config.settings import *
from os.path import join
from .State import *
from utils.Box import *
from utils.Button import *
from utils.Box import *
from utils.TextInput import *

INPUT_POS = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

class Player(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)

        self.box = Box(self.elements)
        box_rect = self.box.get_rect()
        self.display_error = False

        self.setup_text(box_rect)
        self.setup_buttons(event_manager)
        self.setup_inputs(event_manager)

    def setup_text(self, box_rect):
        TITLE_POSITION = (box_rect.centerx, box_rect.top + 50)
        self.title = TITLE.render("Player Name", True, COLORS["AMBER"])
        self.title_rect = self.title.get_rect(center=TITLE_POSITION)

        self.error = TEXT.render("Please enter a name before proceeding", True, COLORS["RED"])
        self.error_rect = self.error.get_rect(center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 125))

    def setup_buttons(self, event_manager):
        self.continue_btn = Button(self.elements, RIGHT_BTN_POSITION, event_manager)
        self.back_btn = Button(self.elements, LEFT_BTN_POSITION, event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.interactive_elements.append(self.continue_btn)
        self.interactive_elements.append(self.back_btn)

    def setup_inputs(self, event_manager):
        self.name_input = TextInput(INPUT_POS, 300,50, event_manager ,'name')
        self.name_input.set_up_input_events()

    def draw(self):
        self.elements.draw(self.screen)
        self.screen.blit(self.title, self.title_rect)
        self.name_input.draw()
        if self.display_error:
            self.screen.blit(self.error, self.error_rect)

    def update(self):
        self.elements.update()
        self.check_click()
        self.update_cursor_state()
        self.name_input.update()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.check_input_click()
                self.back_btn.check_notify_state("menu")
                self.check_continue()
                self.click_handled = True
        else:
            self.click_handled = False

    def check_continue(self):
        if self.continue_btn.rect.collidepoint(pygame.mouse.get_pos()):
            if(self.name_input.get_input_text() == ''):
                self.display_error = True
            else:
                self.clear()
                self.continue_btn.check_notify_state("instructions")
                self.event_manager.notify("display_continue_btn")

    def clear(self, *args):
        self.display_error = False
        self.name_input.set_text('')

    def check_input_click(self):
        if self.name_input.rect.collidepoint(pygame.mouse.get_pos()):
            self.name_input.toggle_active(True)
        else:
            self.name_input.toggle_active(False)

    def set_up_player_events(self):
        self.event_manager.subscribe("clear_player_data", self.clear)