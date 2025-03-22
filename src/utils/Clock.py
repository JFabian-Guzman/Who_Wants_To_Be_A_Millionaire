from config.settings import *
from os.path import join


class Clock(pygame.sprite.Sprite):
  def __init__(self, group):
    super().__init__(group)
    self.screen = pygame.display.get_surface()
    self.image = pygame.image.load(join("assets", "img", "clock_circle.png")).convert_alpha()
    self.rect = self.image.get_rect( center = (WINDOW_WIDTH//2 ,WINDOW_HEIGHT//2 + 150) )
    self.start_time = pygame.time.get_ticks()
    
  def update_time(self):
    elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000

    text = TEXT.render(str(elapsed_time), True, COLORS["BLACK"])
    text_rect = text.get_rect(center = self.rect.center)
    self.screen.blit(text, text_rect)
  
  def restart_time(self):
    self.start_time = pygame.time.get_ticks()