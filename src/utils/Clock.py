from config.settings import *
from os.path import join
from utils.PathHandler import *

class Clock(pygame.sprite.Sprite):
  def __init__(self, group):
    super().__init__(group)
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.image = pygame.image.load(resource_path(join("assets", "img", "clock_circle.png"))).convert_alpha()
    self.rect = self.image.get_rect( center = (self.width//2 ,self.height//2 + 150) )
    self.start_time = pygame.time.get_ticks()
    
  def update_time(self):
    elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000

    text = TEXT.render(str(elapsed_time), True, COLORS["BLACK"])
    text_rect = text.get_rect(center = self.rect.center)
    self.screen.blit(text, text_rect)
  
  def restart_time(self):
    self.start_time = pygame.time.get_ticks()

  def update_position(self):
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.rect = self.image.get_rect( center = (self.width//2 ,self.height//2 + 150) )
