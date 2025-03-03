from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *
from utils.PracticeFlag import *

RESTART_POSITION = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 75)
REWARD_POSITION = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 15)
COIN_POSITION = (REWARD_POSITION[0] + 75, REWARD_POSITION[1] - 2)

class Practice(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)

        self.box = Box(self.elements)
        self.reward_message = ""

        self.no_btn = Button(self.elements, LEFT_BTN_POSITION, event_manager, 'negative_btn', 'No', 'WHITE')
        self.yes_btn = Button(self.elements, RIGHT_BTN_POSITION, event_manager, 'btn', 'Yes')

        PracticeFlag(self.elements)

        self.interactive_elements.append(self.no_btn)
        self.interactive_elements.append(self.yes_btn)

        self.update_text_elements()

    def draw(self):
        self.elements.draw(self.screen)
        self.draw_text_elements()
        self.update_cursor_state()
        self.check_click()

    def draw_text_elements(self):
        for text_surface, position in self.text_elements:
            text_rect = text_surface.get_rect(center=position)
            self.screen.blit(text_surface, text_rect)

    def update(self):
        self.elements.update()

    def update_text_elements(self):
        self.text_elements = [
            (TITLE.render("Play again?", True, COLORS["WHITE"]), RESTART_POSITION),
            (TEXT.render(self.reward_message, True, COLORS["WHITE"]), REWARD_POSITION)
        ]

    def set_results(self, *args):
        data = args[0]
        self.reward_message = f"Correct answers: {data[0]}     Wrong answers: {data[1]}"
        self.update_text_elements()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.no_btn.check_notify_state("menu")
                self.yes_btn.check_notify_state("play")
                self.click_handled = True
        else:
            self.click_handled = False

    def set_up_practice_events(self):
        self.event_manager.subscribe("practice_results", self.set_results)