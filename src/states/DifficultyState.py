from config.settings import *
from .State import *
from utils.Box import *
from utils.Button import *
from utils.DifficultyOption import *

DIFFICULTIES = [
    ("Practice", "_yellow", (WINDOW_WIDTH // 2 - 225, WINDOW_HEIGHT // 2 - 35)),
    ("Easy", "_green", (WINDOW_WIDTH // 2 - 225, WINDOW_HEIGHT // 2 + 65)),
    ("Normal", "_light_blue", (WINDOW_WIDTH // 2 + 225, WINDOW_HEIGHT // 2 - 35)),
    ("Hard", "_red", (WINDOW_WIDTH // 2 + 225, WINDOW_HEIGHT // 2 + 65))
]

class Difficulty(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.box = Box(self.elements)
        box_rect = self.box.get_rect()
        self.active_difficulty = None
        self.display_warning_message = False

        self.setup_positions(box_rect)
        self.setup_text_elements()
        self.setup_difficulty_options()
        self.setup_buttons(event_manager)

    def setup_positions(self, box_rect):
        self.TITLE_POSITION = (box_rect.centerx, box_rect.top + 50)
        self.WARNING_POSITION = (box_rect.centerx, box_rect.top + 100)

    def setup_text_elements(self):
        self.text_elements = [
            (TITLE.render("Select Difficulty", True, COLORS["AMBER"]), self.TITLE_POSITION),
        ]
        self.warning_message = TEXT.render("Please select a difficulty", True, COLORS["RED"])
        self.warning_rect = self.warning_message.get_rect(center=self.WARNING_POSITION)

    def setup_difficulty_options(self):
        self.difficulties = []
        for difficulty, color, position in DIFFICULTIES:
            option = DifficultyOption(difficulty, position, self.elements, color)
            self.difficulties.append(option)
            self.interactive_elements.append(option)

    def setup_buttons(self, event_manager):
        self.continue_btn = Button(self.elements, RIGHT_BTN_POSITION, event_manager, text="Start")
        self.back_btn = Button(self.elements, LEFT_BTN_POSITION, event_manager, 'negative_btn', 'Go Back', 'WHITE')
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
            if not difficulty.get_active():
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
            self.back_btn.check_notify_state("rewards")
            self.reset_difficulty_selection()
            return True
        return False

    def reset_difficulty_selection(self):
        if self.active_difficulty:
            self.active_difficulty.set_active(False)
        self.display_warning_message = False
        self.active_difficulty = None