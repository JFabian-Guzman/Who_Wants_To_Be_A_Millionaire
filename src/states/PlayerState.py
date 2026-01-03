from config.settings import *
from os.path import join
from .State import *
from utils.Box import *
from utils.Button import *
from utils.Box import *
from utils.TextInput import *

class Player(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)

        self.box = Box(self.elements)
        box_rect = self.box.get_rect()
        self.display_error = False

        self.set_up_position(box_rect)
        self.set_up_text()
        self.set_up_buttons()
        self.set_up_inputs()

    def set_up_text(self):
        self.title = TITLE.render("Player's Name", True, COLORS["AMBER"])
        self.title_rect = self.title.get_rect(center=self.title_position)

        self.error = TEXT.render("Please enter a name before proceeding", True, COLORS["AMBER"])
        self.error_rect = self.error.get_rect(center = self.error_pos)

    def set_up_position(self, box_rect):
        self.title_position = (box_rect.centerx, box_rect.top + 50)
        self.left_btn_pos = (box_rect.left + 150, box_rect.bottom - 75)
        self.right_btn_pos = (box_rect.right - 150, box_rect.bottom - 75)
        self.error_pos = (box_rect.centerx, box_rect.top + 100)
        
    def set_up_buttons(self):
        self.continue_btn = Button(self.elements, self.right_btn_pos, self.event_manager)
        self.back_btn = Button(self.elements, self.left_btn_pos, self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.interactive_elements.append(self.continue_btn)
        self.interactive_elements.append(self.back_btn)

    def set_up_inputs(self):
        self.name_input = TextInput((self.width//2, self.height//2), 300,50, self.event_manager ,'name')
        self.name_input.set_up_input_events()
        self.interactive_elements.append(self.name_input)

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
                self.back_btn.check_notify_state("play")
                self.check_continue()
                self.click_handled = True
        else:
            self.click_handled = False

    def check_continue(self):
        if self.continue_btn.rect.collidepoint(pygame.mouse.get_pos()):
            if(self.name_input.get_input_text() == ''):
                self.display_error = True
            else:
                self.event_manager.notify("set_player_name", self.name_input.get_input_text())
                self.clear()
                self.continue_btn.check_notify_state("difficulty")
                

    def clear(self, *args):
        self.display_error = False
        self.name_input.set_text('')

    def check_input_click(self):
        if self.name_input.rect.collidepoint(pygame.mouse.get_pos()):
            self.name_input.toggle_active(True)
        else:
            self.name_input.toggle_active(False)

    def update_size(self, *args):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        self.box.updates_position()
        box_rect = self.box.get_rect()
        self.set_up_position(box_rect)
        self.set_up_text()
        self.name_input.update_position(box_rect.center)
        self.back_btn.update_position(self.left_btn_pos)
        self.continue_btn.update_position(self.right_btn_pos)

    def set_up_player_events(self):
        self.event_manager.subscribe("clear_player_data", self.clear)
        self.event_manager.subscribe("update_size", self.update_size)