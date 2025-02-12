from config.settings import *
from os.path import join
from .State import *
from utils.Button import *

class Glossary(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.current_level = 1
    self.current_lives = 3
    self.click_handled = False
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 30)
    message = """
  Glossary Screen

(Under Construction)
    """

    self.text = self.font.render(message, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center=(WINDOW_WIDTH/2  ,WINDOW_HEIGHT/2))
    self.back_btn = Button(self.elements,( WINDOW_WIDTH//2, WINDOW_HEIGHT //2 + 100), event_manager, 'negative_btn', 'Go Back', 'WHITE')

    self.interactive_elements.append(self.back_btn)

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.text, self.text_rect)
    self.update_cursor_state()
    self.check_click()
    
  def update(self):
    self.elements.update()

  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        self.back_btn.check_notify_state("menu")
        self.click_handled = True
    else:
        self.click_handled = False


