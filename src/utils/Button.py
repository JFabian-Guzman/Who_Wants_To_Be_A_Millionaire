from config.settings import *
from os.path import join

class Button(pygame.sprite.Sprite):
  def __init__(self, position, event_manager, type = 'btn', text = 'Continue', color = 'BLACK'):
    super().__init__()
    
    self.image = pygame.image.load(join("assets", "img" ,type + '.png')).convert_alpha()
    self.rect = self.image.get_rect(center = position)
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 14)
    self.text = self.font.render(text, True, COLORS[color])
    self.text_rect = self.text.get_rect(center = self.rect.center)
    self.event_manager = event_manager

  def draw(self):
    self.screen.blit(self.image, self.rect)
    self.screen.blit(self.text, self.text_rect)

  def get_rect(self):
    return self.rect

  def check_notify_state(self, state: str):
    state_change = False
    if self.rect.collidepoint(pygame.mouse.get_pos()):
      self.event_manager.notify("set_state", state)
      state_change = True
    return state_change

