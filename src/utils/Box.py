from config.settings import *
from os.path import join
from utils.BackBtn import *

class Box(pygame.sprite.Sprite):
  def __init__(self, groups, event_manager):
    super().__init__(groups)
    self.image = pygame.image.load(join("assets", "img" ,"blue_box.png")).convert_alpha()
    self.rect = self.image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    self.back_btn = BackBtn(groups, (self.rect.midleft[0] + 170, self.rect.midleft[1] + 190),event_manager)
    self.event_manager = event_manager

  def update(self):
    self.update_cursor_state()

  def update_cursor_state(self):
    if self.back_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
      self.event_manager.notify("change_cursor", 'hover')
    else:
      self.event_manager.notify("change_cursor", 'default')

  def get_rect(self):
    return self.rect

