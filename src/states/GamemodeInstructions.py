from config.settings import *
from os.path import join
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

class GamemodeInstrucitions(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.box = Box(self.elements)
        box_rect = self.box.get_rect()

        self.setup_positions(box_rect)
        self.setup_text_elements()
        self.setup_buttons(box_rect)
        self.set_up_difficulty_options()

        self.display_continue = True
        self.click_handled = False
        self.display_lifeline = False

    def setup_positions(self, box_rect):
        self.title_position = (box_rect.centerx, box_rect.top + 50)
        self.positions = [
            (box_rect.left + 200, box_rect.top + 125), # Practice
            (box_rect.left + 200, box_rect.top + 200), # Easy
            (box_rect.left + 200, box_rect.top + 275), # Normal
            (box_rect.left + 200, box_rect.top + 350)  # Hard
        ]
        self.practice_text_position = (box_rect.left + 375, box_rect.top + 125)
        self.easy_text_position = (box_rect.left + 375, box_rect.top + 200)
        self.normal_text_position = (box_rect.left + 375, box_rect.top + 275)
        self.hard_text_position = (box_rect.left + 375, box_rect.top + 350)
        self.right_btn_pos = (box_rect.right - 150, box_rect.bottom - 75)
        self.left_btn_pos = (box_rect.left + 150, box_rect.bottom - 75)

    def setup_text_elements(self):
        self.title = TITLE.render("Gamemode", True, COLORS["AMBER"])
        self.title_rect = self.title.get_rect(center=self.title_position)

        # Handle multiline texts
        self.text_lines = {}
        gamemode_texts = {
            "practice": (GAMEMODES_INSTRUCTIONS["PRACTICE"], self.practice_text_position),
            "easy": (GAMEMODES_INSTRUCTIONS["EASY"], self.easy_text_position),
            "normal": (GAMEMODES_INSTRUCTIONS["NORMAL"], self.normal_text_position),
            "hard": (GAMEMODES_INSTRUCTIONS["HARD"], self.hard_text_position)
        }
        line_height = TEXT.get_height()
        for key, (text, position) in gamemode_texts.items():
            lines = text.strip().split('\n')
            self.text_lines[key] = []
            for i, line in enumerate(lines):
                if line.strip():
                    rendered_line = TEXT.render(line.strip(), True, COLORS["WHITE"])
                    rect = rendered_line.get_rect(midleft=(position[0], position[1] + i * (line_height + 2)))
                    self.text_lines[key].append((rendered_line, rect))


    def set_up_difficulty_options(self):
        self.difficulties = []
        for i, (difficulty, color) in enumerate(DIFFICULTIES):
            self.difficulties.append(DifficultyOption(difficulty, self.positions[i], self.elements, color))


    def setup_buttons(self, box_rect):
        self.back_btn = Button(self.elements, self.left_btn_pos, self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.interactive_elements.append(self.back_btn)

    def draw(self):
        self.elements.draw(self.screen)
        self.screen.blit(self.title, self.title_rect)
        for key in self.text_lines:
            for line_surface, line_rect in self.text_lines[key]:
                self.screen.blit(line_surface, line_rect)

    def update(self):
        self.elements.update()
        self.check_click()
        self.update_cursor_state()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.back_btn.check_notify_state("instructions")
                self.click_handled = True
        else:
            self.click_handled = False


    def update_size(self, *args):
        self.box.updates_position()
        box_rect = self.box.get_rect()
        self.setup_positions(box_rect)
        self.setup_text_elements()
        self.back_btn.update_position(self.left_btn_pos)
        for i, difficulty in enumerate(self.difficulties):
            difficulty.update_position(self.positions[i])
        

    def set_up_gamemode_instructins_events(self):
        self.event_manager.subscribe("update_size", self.update_size)