from config.settings import *
from os.path import join

class Box(pygame.sprite.Sprite):
  def __init__(self, groups, event_manager):
    super().__init__(groups)
    self.image = pygame.image.load(join("assets", "img" ,"blue_box.png")).convert_alpha()
    self.rect = self.image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    # self.back_btn = BackBtn(groups, (self.rect.midleft[0] + 170, self.rect.midleft[1] + 190),event_manager)
    self.event_manager = event_manager
    self.display_contiue = True
    

  def erase_continue_btn(self, *args):
    self.display_contiue = False

  def get_rect(self):
    return self.rect