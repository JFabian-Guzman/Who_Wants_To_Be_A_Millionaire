from config.settings import *
from os.path import join

class Cursor(pygame.sprite.Sprite):
  def __init__(self,groups, event_manager):
    super().__init__(groups)
    self.image = pygame.image.load(join("assets", "img", "cursor.png")).convert_alpha()
    self.rect = self.image.get_rect()
    self.screen = pygame.display.get_surface()
    self.collision = False
    self.event_manager = event_manager

  def change_mouse_image(self, *args):
    mouse_type = args[0]
    if mouse_type == 'hover':
      self.image = pygame.image.load(join("assets", "img", "hover_cursor.png")).convert_alpha()
    elif mouse_type == 'default':
      self.image = pygame.image.load(join("assets", "img", "cursor.png")).convert_alpha()
    elif mouse_type == 'text':
      self.image = pygame.image.load(join("assets", "img", "text_cursor.png")).convert_alpha()


  def update(self):
    self.rect.topleft = pygame.mouse.get_pos()

  def set_up_cursor_events(self):
    self.event_manager.subscribe('change_cursor', self.change_mouse_image)
