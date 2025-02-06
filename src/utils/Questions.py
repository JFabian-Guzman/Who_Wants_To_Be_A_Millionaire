from config.settings import *
from os.path import isfile, join
import json

class Question(pygame.sprite.Sprite):
  def __init__(self , groups, event_manager):
    super().__init__(groups)
    pygame.font.init()  
    self.image = pygame.image.load(join("assets", "img" ,"question.png")).convert_alpha()
    self.rect = self.image.get_rect(center = (WINDOW_WIDTH/2,200))
    self.screen = pygame.display.get_surface()
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 20)
    self.event_manager = event_manager
    self.text = self.font.render("", True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)
    self.current_level = 0

  def update(self):
    self.screen.blit(self.text, self.text_rect)
    self.read_question()

  def read_question(self):
    if isfile(join("data", "Questions.json")):
      with open(join("data", "Questions.json"), "r") as file:
        data = json.load(file)
        actual_question = data[self.current_level]["question"]
        self.text = self.font.render(actual_question, True, COLORS["WHITE"])
        self.text_rect = self.text.get_rect(center = self.rect.center)

  def get_rect(self):
    return self.rect

  def get_title(self):
    return self.title
  
  def update_level(self, *args):
    self.current_level += 1

  def set_up_question_events(self):
    self.event_manager.subscribe("update_level", self.update_level)



