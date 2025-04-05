from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *
from utils.WinFlag import *
from utils.Coin import *

class Win(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)

        self.box = Box(self.elements)
        box_rect = self.box.get_rect()
        self.reward_message = ""

        self.no_btn = Button(self.elements, (box_rect.left + 150, box_rect.bottom - 75), event_manager, 'negative_btn', 'No', 'WHITE')
        self.yes_btn = Button(self.elements, (box_rect.right - 150, box_rect.bottom - 75), event_manager, 'btn', 'Yes')

        self.flag = WinFlag( (box_rect.centerx, box_rect.top + 60) , self.elements)
        self.coin = Coin((self.width // 2 + 100, self.height // 2 + 13), self.elements)

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
            (TITLE.render("Play again?", True, COLORS["WHITE"]), (self.width / 2, self.height / 2 + 75)),
            (TEXT.render(self.reward_message, True, COLORS["WHITE"]), (self.width // 2, self.height // 2 + 15))
        ]

    def set_reward(self, *args):
        self.reward_message = "You win " + str(args[0])
        self.update_text_elements()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.no_btn.check_notify_state("menu")
                self.yes_btn.check_notify_state("play")
                self.click_handled = True
        else:
            self.click_handled = False

    def update_size(self, *args):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        self.box.updates_position()
        box_rect = self.box.get_rect()
        self.update_text_elements()
        self.no_btn.update_position((box_rect.left + 150, box_rect.bottom - 75))
        self.yes_btn.update_position((box_rect.right - 150, box_rect.bottom - 75))
        self.coin.update_position((self.width // 2 + 100, self.height // 2 + 13))
        self.flag.update_position((box_rect.centerx, box_rect.top + 60))

    def set_up_win_events(self):
        self.event_manager.subscribe("update_size", self.update_size)
        self.event_manager.subscribe("final_reward", self.set_reward)