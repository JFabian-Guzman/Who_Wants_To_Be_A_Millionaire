from config.settings import *
from os.path import join
from utils.Icon import *

class CrudBox(pygame.sprite.Sprite):
  def __init__(self, question, options, id , position, event_manager):
    super().__init__()

    self.screen = pygame.display.get_surface()
    self.interactive_elements = []

    self.id = id
    self.event_manager = event_manager

    self.image = pygame.image.load(join("assets", "img" ,"crud_box.png")).convert_alpha()
    self.rect = self.image.get_rect(center = position)

    self.pencil_icon = Icon((self.rect.midright[0] - 80, self.rect.midright[1] + 40),"pencil")
    self.trash_icon = Icon((self.rect.midright[0] - 25, self.rect.midright[1] + 40),"trash")


    self.interactive_elements.append(self.pencil_icon)
    self.interactive_elements.append(self.trash_icon )

    wrap_options = self.wrap_text(options)

    self.question = TEXT.render("Question:" + question, True, COLORS["WHITE"])
    self.question_rect = self.question.get_rect(midleft = (self.rect.midleft[0] + 20, self.rect.midleft[1] - 25))
    self.options = TEXT.render("Options:" + wrap_options, True, COLORS["WHITE"])
    self.options_rect = self.options.get_rect(midleft = (self.rect.midleft[0] + 20, self.rect.midleft[1] + 25))

  def draw(self):
    self.screen.blit(self.image, self.rect)
    self.screen.blit(self.question, self.question_rect)
    self.screen.blit(self.options, self.options_rect)
    self.pencil_icon.draw()
    self.trash_icon.draw()

  def get_interactive_elements(self):
    return self.interactive_elements

  def wrap_text(self, text):
        wrap_text = text
        if len(text) > 60:
            split = len(text) - 10
            if ord(text[split]) >= 65 and ord(text[split]) <= 90 or ord(text[split]) >= 97 and ord(text[split]) <= 122:
              wrap_text =  text[:split] + "-\n\n" + text[split:]
            else:
              wrap_text = text[:split] + "\n\n" + text[split:]
        return wrap_text
