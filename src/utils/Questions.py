from config.settings import *
from os.path import join
from utils.PathHandler import *
import textwrap

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
    self.text_lines = []  # Initialize as list for multiline text
    self.text = TEXT.render(self.title, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def display_question(self):
    # Handle multiline question text properly
    text_lines = self.title.split('\n')
    self.text_lines = []
    line_height = TEXT.get_height()
    start_y = self.rect.centery - (len(text_lines) - 1) * line_height // 2
    for i, line in enumerate(text_lines):
      if line.strip():
        rendered_line = TEXT.render(line, True, COLORS["WHITE"])
        rect = rendered_line.get_rect(center=(self.rect.centerx, start_y + i * (line_height + 2)))
        self.text_lines.append((rendered_line, rect))

  def update(self):
    self.display_question()
    # Draw multiline text
    for line_surface, line_rect in self.text_lines:
      self.screen.blit(line_surface, line_rect)

  def wrap_text(self, text):
    max_width = 68  # for 'option' text
    if len(text) > max_width:
        wrapped_lines = textwrap.wrap(text, width=max_width)
        return "\n".join(wrapped_lines)
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
