from config.settings import *
from os.path import join

class Heart(pygame.sprite.Sprite):
  def __init__(self, position):
    super().__init__()
    self.screen = pygame.display.get_surface()
    self.current_sprite = 0
    self.sprites = []
    self.shield_animation = False
    self.reverse_animation = False
    self.active = True

    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation1.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation2.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation3.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation4.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation5.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"heart_animation6.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img" ,"disable_heart.png")).convert_alpha())

    self.shield_sprites = []
    self.shield_sprites.append(pygame.image.load(join("assets", "img" ,"heart.png")).convert_alpha())
    self.shield_sprites.append(pygame.image.load(join("assets", "img" ,"shield_heart_animation1.png")).convert_alpha())
    self.shield_sprites.append(pygame.image.load(join("assets", "img" ,"shield_heart_animation2.png")).convert_alpha())
    self.shield_sprites.append(pygame.image.load(join("assets", "img" ,"shield_heart_animation3.png")).convert_alpha())
    self.shield_sprites.append(pygame.image.load(join("assets", "img" ,"shield_heart_animation4.png")).convert_alpha())
    self.shield_sprites.append(pygame.image.load(join("assets", "img" ,"shield_heart_animation5.png")).convert_alpha())
    self.shield_sprites.append(pygame.image.load(join("assets", "img" ,"shield_heart_animation6.png")).convert_alpha())

    self.image = self.sprites[self.current_sprite]
    self.rect = self.image.get_rect(center=position)
    self.run_animation = False

  def draw(self):
    self.screen.blit(self.image, self.rect)

  def update(self):
    if self.run_animation and self.active:
      if self.shield_animation :
          self.animate_shield()
      else:
          self.animate_destruction()

  def disable(self):
    self.start_animation()
    

  def enable(self):
    self.stop_animation()
    self.current_sprite = 0
    self.image = self.sprites[self.current_sprite]
    self.active = True

  def animate_destruction(self):
    self.current_sprite += 0.105
    if self.current_sprite >= len(self.sprites):
        self.active = False
        self.current_sprite = len(self.sprites) - 1
        self.stop_animation()
    self.image = self.sprites[int(self.current_sprite)]

  def animate_shield(self):
    if self.reverse_animation:
        self.current_sprite -= 0.105
        if self.current_sprite <= 0:
            self.current_sprite = 0
            self.stop_animation()
    else:
        self.current_sprite += 0.105
        if self.current_sprite >= len(self.shield_sprites):
            self.current_sprite = len(self.shield_sprites) - 1
            self.stop_animation()
    self.image = self.shield_sprites[int(self.current_sprite)]

  def stop_animation(self):
    self.run_animation = False

  def start_animation(self, shield=False, reverse=False):
    self.run_animation = True
    self.shield_animation = shield
    self.reverse_animation = reverse
    if reverse:
        self.current_sprite = len(self.shield_sprites) - 1
    else:
        self.current_sprite = 0

  def update_position(self, position):
    self.rect = self.image.get_rect(center=position)