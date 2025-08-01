from config.settings import *
from os.path import join
from utils.PathHandler import *

class Question(pygame.sprite.Sprite):
  def __init__(self , groups, event_manager):
    super().__init__(groups)
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()

    self.image = pygame.image.load(resource_path(join("assets", "img" ,"question.png"))).convert_alpha()
    self.rect = self.image.get_rect(center = (self.width//2, self.height//2 - 160))
    self.screen = pygame.display.get_surface()
    self.event_manager = event_manager
    self.title = ''
    self.text = TEXT.render(self.title, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def update(self):
    self.screen.blit(self.text, self.text_rect)
    self.display_question()

  def display_question(self):
    self.text = TEXT.render(self.title, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def wrap_text(self, text):
    if len(text) > 54:
        mid = len(text) // 2
        if ord(text[mid]) >= 65 and ord(text[mid]) <= 90 or ord(text[mid]) >= 97 and ord(text[mid]) <= 122:
          return text[:mid] + "-\n" + text[mid:]
        else:
          return text[:mid] + "\n" + text[mid:]
    return text

  def get_rect(self):
    return self.rect

  def get_title(self):
    return self.title
  
  def change_question(self, *args):
    self.title = self.wrap_text(args[0])

  def update_position(self):
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.rect = self.image.get_rect(center = (self.width//2, self.height//2 - 160))

  def set_up_question_events(self):
    self.event_manager.subscribe("change_question_text", self.change_question)

 

