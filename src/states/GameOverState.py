from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *
from utils.GameOverFlag import *
from utils.Coin import *

class GameOver(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        
        self.box = Box(self.elements)
        box_rect = self.box.get_rect()

        self.answer = ''
        self.reward = ''
        self.set_up_positions(box_rect)
        self.set_up_elements()
        self.update_text_elements()

    def update_text_elements(self):
        self.text_elements = [
            (TITLE.render("Play again?", True, COLORS["WHITE"]), (self.width // 2, self.height // 2 + 75)),
            (TEXT.render("Unfortunately, the correct answer was ", True, COLORS["WHITE"]), (self.width // 2, self.height // 2 - 30)),
            (TEXT.render(self.answer, True, COLORS["WHITE"]), (self.width // 2, self.height // 2 )),
            (TEXT.render("You win " + self.reward, True, COLORS["WHITE"]), (self.width // 2, self.height // 2 + 30))
        ]

    def set_up_positions(self, box_rect):
        self.left_btn_pos = (box_rect.left + 150, box_rect.bottom - 75)
        self.right_btn_pos = (box_rect.right - 150, box_rect.bottom - 75)
        self.flag_pos = (box_rect.centerx, box_rect.top + 60)
        self.coin_pos = (self.width // 2 + 100, self.height // 2 + 28)

    def set_up_elements(self):
        self.no_btn = Button(self.elements, self.left_btn_pos, self.event_manager, 'negative_btn', 'No', 'WHITE')
        self.yes_btn = Button(self.elements, self.right_btn_pos, self.event_manager, 'btn', 'Yes')

        self.flag = GameOverFlag(self.flag_pos, self.elements)
        self.coin = Coin(self.coin_pos, self.elements)

        self.sound = pygame.mixer.Sound(join("assets", "sounds" ,"game_over.mp3"))
        self.sound.set_volume(.5)

        self.interactive_elements.append(self.no_btn)
        self.interactive_elements.append(self.yes_btn)

    def draw(self):
        self.elements.draw(self.screen)
        self.draw_text_elements()
        self.check_click()

    def draw_text_elements(self):
        for text_surface, position in self.text_elements:
            text_rect = text_surface.get_rect(center=position)
            self.screen.blit(text_surface, text_rect)

    def update(self):
        self.elements.update()
        self.update_cursor_state()

    

    def set_reward(self, *args):
        data = args[0]
        self.answer = data[0]
        self.reward = str(data[1])
        self.update_text_elements()

    def play_sound(self, *args):
        self.sound.play()

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
        self.set_up_positions(box_rect)
        self.no_btn.update_position(self.left_btn_pos)
        self.yes_btn.update_position(self.right_btn_pos)
        self.coin.update_position(self.coin_pos)
        self.flag.update_position(self.flag_pos)

    def set_up_game_over_events(self):
        self.event_manager.subscribe("update_size", self.update_size)
        self.event_manager.subscribe("game_over_message", self.set_reward)
        self.event_manager.subscribe("play_game_over_sound", self.play_sound)