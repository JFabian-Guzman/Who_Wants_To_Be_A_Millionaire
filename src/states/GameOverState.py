from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *
from utils.GameOverFlag import *

class GameOver(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.title_font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 34)
    self.body_font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 14)
    self.box = Box(self.elements, self.event_manager)
    restart_message = "Play again?"
    box_rect = self.box.get_rect()
    self.text = self.title_font.render(restart_message, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center=(WINDOW_WIDTH/2  ,WINDOW_HEIGHT/2 + 75))
    self.no_btn = Button(( WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT //2 + 175), event_manager, 'negative_btn', 'No', 'WHITE')
    self.yes_btn = Button(( WINDOW_WIDTH//2 + 200, WINDOW_HEIGHT //2 + 175), event_manager, 'btn', 'Yes')
    self.win_flag = GameOverFlag(( WINDOW_WIDTH//2, box_rect.top + 50 ), self.elements)
    self.set_reward(("N",0))
    self.coin = pygame.image.load(join("assets", "img" ,"coin.png")).convert_alpha()
    self.coin_rect = self.coin.get_rect(midleft = (self.reward_text_rect.right + 20, self.reward_text_rect.centery - 2))

    self.interactive_elements.append(self.no_btn)
    self.interactive_elements.append(self.yes_btn)

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.text, self.text_rect)
    self.screen.blit(self.reward_text, self.reward_text_rect)
    self.screen.blit(self.answer_text, self.answer_text_rect)
    self.screen.blit(self.coin, self.coin_rect)

    
    self.no_btn.draw()
    self.yes_btn.draw()
    self.update_cursor_state()
    self.check_click()
    
    
  def update(self):
    self.elements.update()

  def set_reward(self, *args):
    print("ARGS ", args)
    data = args[0]

    self.answer_message = "Unfortunately, the correct answer was " + data[0]
    self.answer_text = self.body_font.render(self.answer_message, True, COLORS["WHITE"])
    self.answer_text_rect = self.answer_text.get_rect(center=(WINDOW_WIDTH//2  ,WINDOW_HEIGHT//2 - 20))

    self.reward_message = "You win " + REWARDS[data[1]]
    self.reward_text = self.body_font.render(self.reward_message, True, COLORS["WHITE"])
    self.reward_text_rect = self.reward_text.get_rect(center=(WINDOW_WIDTH//2  ,WINDOW_HEIGHT//2 + 15))

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
