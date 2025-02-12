from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *
from utils.GameOverFlag import *
from utils.Coin import *

RESTART_POSITION = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 75)
ANSWER_TEXT_POSITION = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
ANSWER_POSITION = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
REWARD_POSITION = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30)
COIN_POSITION = (REWARD_POSITION[0] + 75, REWARD_POSITION[1] - 2)

class GameOver(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        
        self.box = Box(self.elements)

        self.answer = ''
        self.reward = ''

        self.no_btn = Button(self.elements, LEFT_BTN_POSITION, event_manager, 'negative_btn', 'No', 'WHITE')
        self.yes_btn = Button(self.elements,RIGHT_BTN_POSITION, event_manager, 'btn', 'Yes')

        GameOverFlag(self.elements)
        
        Coin(COIN_POSITION, self.elements)

        self.interactive_elements.append(self.no_btn)
        self.interactive_elements.append(self.yes_btn)

        self.update_text_elements()

    def update_text_elements(self):
        self.text_elements = [
            (TITLE.render("Play again?", True, COLORS["WHITE"]), RESTART_POSITION),
            (TEXT.render("Unfortunately, the correct answer was ", True, COLORS["WHITE"]), ANSWER_TEXT_POSITION),
            (TEXT.render(self.answer, True, COLORS["WHITE"]), ANSWER_POSITION),
            (TEXT.render("You win " + self.reward, True, COLORS["WHITE"]), REWARD_POSITION)
        ]

    def draw(self):
        self.elements.draw(self.screen)
        for text_surface, position in self.text_elements:
            text_rect = text_surface.get_rect(center=position)
            self.screen.blit(text_surface, text_rect)
        self.check_click()

    def update(self):
        self.elements.update()
        self.update_cursor_state()

    # args = [[Correct_answer, Level]]
    def set_reward(self, *args):
        data = args[0]
        self.answer = data[0]
        self.reward = REWARDS[data[1]]
        self.update_text_elements()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.no_btn.check_notify_state("menu")
                self.yes_btn.check_notify_state("play")
                self.click_handled = True
        else:
            self.click_handled = False

    def set_up_game_over_events(self):
        self.event_manager.subscribe("game_over_message", self.set_reward)
