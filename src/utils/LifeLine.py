from config.settings import *
from os.path import join
import random

class Lifeline(pygame.sprite.Sprite):
  def __init__(self, position, icon):
    super().__init__()
    self.screen = pygame.display.get_surface()
    self.type = icon
    self.available = True
    self.sprites = []
    self.run_animation = False
    self.current_sprite = 0
    self.animation_callback = None
    self.hover_img = pygame.image.load(join("assets", "img" ,"lifeline_hover.png")).convert_alpha()

    self.sprites.append(pygame.image.load(join("assets", "img" ,"lifeline.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"lifeline_disable.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"lifeline.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"lifeline_disable.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"lifeline.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"lifeline_disable.png")).convert_alpha())

    self.image = self.sprites[self.current_sprite]
    self.rect = self.image.get_rect(center=position)
    self.icon = pygame.image.load(join("assets", "img" , icon + ".png")).convert_alpha()
    self.icon_rect = self.icon.get_rect(center=self.rect.center)

  def draw(self):
    self.screen.blit(self.image, self.rect)
    self.screen.blit(self.icon, self.icon_rect)

  def update(self):
    if self.run_animation:
      self.animate()

  def enable(self):
    self.current_sprite = 0
    self.image = self.sprites[self.current_sprite]
    self.available = True

  def fifty_fifty_lifeline(self, options, answer):
    if not self.available:
      return
    result = []
    random_option = random.choice(options)
    while random_option == answer or random_option == '':
      random_option = random.choice(options)
    # This keeps the original order of the options
    for option in options:
      if option == answer or option == random_option:
        result.append(option)
      else:
        result.append('')
    return result

  def animate(self):
    self.current_sprite += 0.075
    print(self.current_sprite)
    if self.current_sprite >= len(self.sprites):
        self.current_sprite = len(self.sprites) - 1
        self.stop_animation()
    self.image = self.sprites[int(self.current_sprite)]

  def on_hover(self):
    self.image = self.hover_img

  def reset_hover(self):
    self.image = self.sprites[self.current_sprite]

  def get_rect(self):
    return self.rect

  def get_type(self):
    return self.type

  def start_animation(self, callback=None):
    self.run_animation = True
    self.animation_callback = callback

  def stop_animation(self):
    self.run_animation = False
    if self.animation_callback:
      self.animation_callback()