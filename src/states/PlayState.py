from config.settings import *
from os.path import join
from utils.Cursor import *
from .State import *

class Play(State):
  def __init__(self, event_manager, cursor):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.cursor = cursor
    self.current_level = 1
    self.current_lives = 3
    self.click_handled = False
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 20)
    self.text = self.font.render("Game Screen", True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect()

  def draw(self):
    self.screen.blit(self.text, self.text_rect)
    
  def update(self):
    pass

  def verify_click(self):
    if pygame.mouse.get_pressed()[0]: 
        if not self.click_handled:
            for option in self.options:
                if option.get_rect().collidepoint(pygame.mouse.get_pos()):
                    print(f"OPTION CLICKED: {option.get_title()}")
                    self.event_manager.notify("update_state", option.get_title)
                    self.click_handled = True
                    return
    else:
        self.click_handled = False


  # def set_up_menu_events(self):
  #   self.event_manager.subscribe('click', self.verify_click)

