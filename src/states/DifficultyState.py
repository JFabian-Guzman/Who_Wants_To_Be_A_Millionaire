from config.settings import *
from .State import *
from utils.Box import *
from utils.Button import *
from utils.DifficultyOption import *

DIFFICULTIES = [
    ("Practice", "_yellow"),
    ("Easy", "_green"),
    ("Normal", "_light_blue"),
    ("Hard", "_red")
]

class Difficulty(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.box = Box(self.elements)
        box_rect = self.box.get_rect()
        self.active_difficulty = None
        self.display_warning_message = False

        self.set_up_positions(box_rect)
        self.set_up_text_elements()
        self.set_up_difficulty_options()
        self.set_up_buttons(box_rect)


    def set_up_positions(self, box_rect):
        self.positions = [
            (self.width // 2 - 225, self.height // 2 - 35), # Practice
            (self.width // 2 - 225, self.height // 2 + 65), # Easy
            (self.width // 2 + 225, self.height // 2 - 35), # Normal
            (self.width // 2 + 225, self.height // 2 + 65)  # Hard
        ]
        self.TITLE_POSITION = (box_rect.centerx, box_rect.top + 50)
        self.WARNING_POSITION = (box_rect.centerx, box_rect.top + 100)
        self.right_btn_pos = (box_rect.right - 150, box_rect.bottom - 75)
        self.left_btn_pos = (box_rect.left + 150, box_rect.bottom - 75)

    def set_up_text_elements(self):
        self.text_elements = [
            (TITLE.render("Select Difficulty", True, COLORS["AMBER"]), self.TITLE_POSITION),
        ]
        self.warning_message = TEXT.render("Please select a difficulty", True, COLORS["RED"])
        self.warning_rect = self.warning_message.get_rect(center=self.WARNING_POSITION)

    def set_up_difficulty_options(self):
        self.difficulties = []
        for i, (difficulty, color) in enumerate(DIFFICULTIES):
            option = DifficultyOption(difficulty, self.positions[i], self.elements, color)
            self.difficulties.append(option)
            self.interactive_elements.append(option)

    def set_up_buttons(self, box_rect):
        self.continue_btn = Button(self.elements, self.right_btn_pos, self.event_manager, text="Start")
        self.back_btn = Button(self.elements, self.left_btn_pos, self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.interactive_elements.append(self.continue_btn)
        self.interactive_elements.append(self.back_btn)

    def draw(self):
        self.elements.draw(self.screen)
        self.draw_text_elements()
        self.draw_difficulty_overlays()
        if self.display_warning_message:
            self.screen.blit(self.warning_message, self.warning_rect)

    def draw_text_elements(self):
        for text_surface, position in self.text_elements:
            text_rect = text_surface.get_rect(center=position)
            self.screen.blit(text_surface, text_rect)

    def draw_difficulty_overlays(self):
        for difficulty in self.difficulties:
            if not difficulty.get_active() and not difficulty.get_hover():
                difficulty.draw_overlay()

    def update(self):
        self.elements.update()
        self.update_cursor_state()
        self.check_click()

    def is_difficulty_selected(self):
        if self.active_difficulty is None:
            self.display_warning_message = True
            return False
        return True

    def check_click(self):
        if not pygame.mouse.get_pressed()[0]:
            self.click_handled = False
            return

        if self.click_handled:
            return

        if self.check_difficulty_click() or self.check_continue_click() or self.check_back_click():
            self.click_handled = True

    def check_difficulty_click(self):
        for difficulty in self.difficulties:
            if difficulty.get_rect().collidepoint(pygame.mouse.get_pos()):
                if self.active_difficulty:
                    self.active_difficulty.set_active(False)
                difficulty.set_active(True)
                self.active_difficulty = difficulty
                return True
        return False

    def check_continue_click(self):
        if self.continue_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
            if self.is_difficulty_selected():
                self.event_manager.notify("set_difficulty", self.active_difficulty.get_title())
                self.continue_btn.check_notify_state("game")
                self.reset_difficulty_selection()
            else:
                self.display_warning_message = True
            return True
        return False

    def check_back_click(self):
        if self.back_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
            self.back_btn.check_notify_state("player")
            self.event_manager.notify("clear_player_data")
            self.reset_difficulty_selection()
            return True
        return False

    def update_size(self, *args):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        self.box.updates_position()
        box_rect = self.box.get_rect()
        self.set_up_positions(box_rect)
        self.back_btn.update_position(self.left_btn_pos)
        self.continue_btn.update_position(self.right_btn_pos)
        self.set_up_text_elements()
        for i, difficulty in enumerate(self.difficulties):
            difficulty.update_position(self.positions[i])


    def reset_difficulty_selection(self):
        if self.active_difficulty:
            self.active_difficulty.set_active(False)
        self.display_warning_message = False
        self.active_difficulty = None

    def set_up_difficulty_events(self):
        self.event_manager.subscribe("update_size", self.update_size)