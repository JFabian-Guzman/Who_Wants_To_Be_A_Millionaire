from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *
from utils.GameOverFlag import *

RESTART_POSITION = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 75)
ANSWER_POSITION = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20)
REWARD_POSITION = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 15)
class GameOver(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.elements = pygame.sprite.Group()
        self.screen = pygame.display.get_surface()

        self.box = Box(self.elements, self.event_manager)
        box_rect = self.box.get_rect()

        self.font_title = pygame.font.Font(PRESS_START_2P, 20)
        self.font_text = pygame.font.Font(PRESS_START_2P, 14)

        self.answer = ''
        self.reward = ''

        self.no_btn = Button((WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 + 175), event_manager, 'negative_btn', 'No', 'WHITE')
        self.yes_btn = Button((WINDOW_WIDTH // 2 + 200, WINDOW_HEIGHT // 2 + 175), event_manager, 'btn', 'Yes')
        self.win_flag = GameOverFlag((WINDOW_WIDTH // 2, box_rect.top + 50), self.elements)

        self.coin = pygame.image.load(join("assets", "img", "coin.png")).convert_alpha()
        self.coin_rect = self.coin.get_rect(midleft=(REWARD_POSITION[0] + 75, REWARD_POSITION[1] - 2))

        self.interactive_elements.append(self.no_btn)
        self.interactive_elements.append(self.yes_btn)

        self.update_text_elements()

    def update_text_elements(self):
        self.text_elements = [
            (self.font_title.render("Play again?", True, COLORS["WHITE"]), RESTART_POSITION),
            (self.font_text.render("Unfortunately, the correct answer was " + self.answer, True, COLORS["WHITE"]), ANSWER_POSITION),
            (self.font_text.render("You win " + self.reward, True, COLORS["WHITE"]), REWARD_POSITION)
        ]

    def draw(self):
        self.elements.draw(self.screen)
        for text_surface, position in self.text_elements:
            text_rect = text_surface.get_rect(center=position)
            self.screen.blit(text_surface, text_rect)
        self.screen.blit(self.coin, self.coin_rect)
        self.no_btn.draw()
        self.yes_btn.draw()
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
