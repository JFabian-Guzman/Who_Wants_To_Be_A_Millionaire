from config.settings import *
from os.path import join
from utils.Option import *
from utils.Logo import *
from .State import *

class Menu(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.options = []
        self.click_handled = True
        self.is_option_animating = False
        self.setup_options()
        self.setup_logo()

    def setup_options(self):
        cols = 2
        for i in range(len(MENU)):
            row = i // cols # calculates the row number for the current option
            col = i % cols # even -> left - odd -> righ
            x_position = ((self.width // 2) // 2) + (self.width // 2 * col)
            y_position = self.height // 2 + (self.height // 8 * row)
            option_instance = Option(MENU[i]["TITLE"], (x_position, y_position), self.elements)
            self.options.append(option_instance)
            self.interactive_elements.append(option_instance)


    def setup_logo(self):
        self.logo = Logo(self.elements)

    def draw(self):
        self.elements.draw(self.screen)

    def update(self):
        self.elements.update()
        self.update_cursor_state()
        self.update_user_click()

    def update_user_click(self):
        if pygame.mouse.get_pressed()[0] :
            if (not self.click_handled and not self.is_option_animating):
                self.handle_option_click()
        else:
            self.click_handled = False

    def handle_option_click(self):
        mouse_pos = pygame.mouse.get_pos()
        for option in self.options:
            if option.get_rect().collidepoint(mouse_pos):
                if option.get_title().lower() == 'exit':
                    self.event_manager.notify("stop_game")
                else:
                    self.is_option_animating = True
                    option.start_animation(callback=lambda: self.change_state(option))
                self.click_handled = True    
                return

    def change_state(self, option):
        self.event_manager.notify("set_state", option.get_title().lower())
        self.is_option_animating = False

    def update_size(self, *args):
        self.width, self.height  = self.screen.get_size()
        self.logo.draw_logo()
        cols = 2
        for i, option in enumerate(self.options):
            row = i // cols # calculates the row number for the current option
            col = i % cols # even -> left - odd -> righ
            x_position = ((self.width // 2) // 2) + (self.width // 2 * col)
            y_position = self.height // 2 + (self.height // 8 * row)
            option.update_position((x_position, y_position))


    def set_up_menu_events(self):
        self.event_manager.subscribe("update_size", self.update_size)