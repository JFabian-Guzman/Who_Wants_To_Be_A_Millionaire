from config.settings import *
from os.path import join
from utils.Button import *

class ConfirmModal(pygame.sprite.Sprite):
  def __init__(self , position, event_manager):
    super().__init__()
    self.elements = pygame.sprite.Group()
    pygame.font.init()  
    self.image = pygame.image.load(join("assets", "img" ,"question.png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 14)
    self.set_option(0)
    self.event_manager = event_manager
    self.interactive_elements = []
    self.click_handled = True
    self.overlay = pygame.Surface(self.screen.get_size())
    self.overlay.fill((0, 0, 0))
    self.overlay.set_alpha(128)
    self.option_index = ''
    self.no_btn = Button(self.elements ,( self.rect.centerx - 200, self.rect.centery + 75 ), event_manager, 'negative_btn', 'No', 'WHITE')
    self.yes_btn = Button(self.elements ,( self.rect.centerx + 200, self.rect.centery + 75), event_manager, 'btn', 'Yes')

    self.interactive_elements.append(self.no_btn)
    self.interactive_elements.append(self.yes_btn)

  def draw(self):
    self.screen.blit(self.overlay, (0, 0))
    self.screen.blit(self.image, self.rect)
    self.screen.blit(self.text, self.text_rect)
    self.elements.draw(self.screen)


  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.check_click()


  def set_option(self, *args):
    self.option_index = args[0]
    self.message = "Is option "+ OPTIONS[self.option_index] +" your final answer?"
    self.text = self.font.render(self.message, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center=(WINDOW_WIDTH//2  ,WINDOW_HEIGHT//2))

  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        if self.no_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
          self.event_manager.notify("switch_modal")
        if self.yes_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
          self.event_manager.notify("validate_answer", self.option_index)
          self.event_manager.notify("switch_modal")
        self.click_handled = True
    else:
        self.click_handled = False

  def update_cursor_state(self):
    for element in self.interactive_elements:
      if element.rect.collidepoint(pygame.mouse.get_pos()):
        self.event_manager.notify("change_cursor", 'hover')
        break
      else:
        self.event_manager.notify("change_cursor", 'default')