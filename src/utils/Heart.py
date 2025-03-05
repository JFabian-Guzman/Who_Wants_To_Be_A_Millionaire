from config.settings import *
from os.path import join

class Heart(pygame.sprite.Sprite):
  def __init__(self, position):
    super().__init__()
    self.screen = pygame.display.get_surface()
    self.current_sprite = 0
    self.sprites = []
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation1.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation2.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation3.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation4.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation5.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation6.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"disable_heart.png")).convert_alpha())

    self.image = self.sprites[self.current_sprite]
    self.rect = self.image.get_rect(center=position)
    self.run_animation = False

  def draw(self):
    self.screen.blit(self.image, self.rect)

  def update(self):
    if self.run_animation:
      self.animate()

  def disable(self):
    self.run_animation = True

  def enable(self):
    self.stop_animation()
    self.current_sprite = 0
    self.image = self.sprites[self.current_sprite]


  def animate(self):
    self.current_sprite += 0.105
    print(self.current_sprite)
    if self.current_sprite >= len(self.sprites):
      self.current_sprite = len(self.sprites) - 1
      self.stop_animation()
    self.image = self.sprites[int(self.current_sprite)]

  def stop_animation(self):
    self.run_animation = False