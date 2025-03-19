from config.settings import *
from os.path import join

class Option(pygame.sprite.Sprite):
  def __init__(self, text , position, groups):
    super().__init__(groups)

    self.sprites = []
    self.sprites_wrong_answer = []
    self.screen = pygame.display.get_surface()
    self.current_sprite = 0
    self.run_animation = False
    self.animation_callback = None
    self.is_wrong = False
    
    self.option_blue = pygame.image.load(join("assets", "img" ,"option.png")).convert_alpha()
    self.option_organe = pygame.image.load(join("assets", "img" ,"option_animation1.png")).convert_alpha()
    option_green = pygame.image.load(join("assets", "img" ,"option_animation2.png")).convert_alpha()
    option_red = pygame.image.load(join("assets", "img" ,"option_wrong.png")).convert_alpha()
    # Animation for correct answer
    self.sprites.append(self.option_blue)
    self.sprites.append(option_green)
    self.sprites.append(self.option_organe)
    self.sprites.append(option_green)
    self.sprites.append(self.option_organe)
    self.sprites.append(option_green)
    # Animation for wrong answer
    self.sprites_wrong_answer.append(self.option_organe)
    self.sprites_wrong_answer.append(option_red)
    self.sprites_wrong_answer.append(self.option_organe)
    self.sprites_wrong_answer.append(option_red)
    self.sprites_wrong_answer.append(self.option_organe)
    self.sprites_wrong_answer.append(option_red)

    self.image = self.sprites[self.current_sprite]
    self.rect = self.image.get_rect(center = position)
    self.display_text = self.wrap_text(text)
    
    self.text = TEXT.render(self.display_text, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def wrap_text(self, text):
        wrap_text = text
        if len(text) > 24:
            mid = len(text) // 2
            if ord(text[mid]) >= 65 and ord(text[mid]) <= 90 or ord(text[mid]) >= 97 and ord(text[mid]) <= 122:
              wrap_text =  text[:mid] + "-\n" + text[mid:]
            else:
              wrap_text = text[:mid] + "\n" + text[mid:]
        return wrap_text

  def update(self):
    self.screen.blit(self.text, self.text_rect)
    if self.run_animation:
      if self.is_wrong:
        self.animate_wrong_answer()
      else:
        self.animate_correct_answer()


  def animate_correct_answer(self):
    self.current_sprite += 0.105
    if self.current_sprite >= len(self.sprites):
      self.current_sprite = 0
      self.stop_animation()
    self.image = self.sprites[int(self.current_sprite)]
    
  def animate_wrong_answer(self):
    self.current_sprite += 0.105
    if self.current_sprite >= len(self.sprites_wrong_answer):
      self.current_sprite = 0
      self.stop_animation()
    self.image = self.sprites_wrong_answer[int(self.current_sprite)]

    
  
  def on_hover(self):
    if not self.run_animation:
      self.sprites[0] = self.option_organe
      self.image = self.sprites[0]

  def reset_hover(self):
    if not self.run_animation:
      self.sprites[0] = self.option_blue
      self.image = self.sprites[0]

  def get_rect(self):
    return self.rect
  
  def start_animation(self, callback=None, wrong=False):
    self.is_wrong = wrong
    self.run_animation = True
    self.animation_callback = callback

  def stop_animation(self):
    self.run_animation = False
    if self.animation_callback:
      self.animation_callback()

  def get_title(self):
    return self.display_text

  def set_title(self,text):
    self.title = text
    self.display_text = self.wrap_text(text)
    self.text = TEXT.render(self.display_text, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center = self.rect.center)



