from config.settings import *
from os.path import join

class WinFlag(pygame.sprite.Sprite):
  def __init__(self, position ,groups):
    super().__init__(groups)
    pygame.font.init()  
    self.screen = pygame.display.get_surface()
    self.current_sprite = 0
    self.sprites = []
    self.sprites.append(pygame.image.load(resource_path(join("assets", "img" ,"win_flag.png"))).convert_alpha())
    self.sprites.append(pygame.image.load(resource_path(join("assets", "img" ,"Winflag_animation1.png"))).convert_alpha())
    self.sprites.append(pygame.image.load(resource_path(join("assets", "img" ,"Winflag_animation2.png"))).convert_alpha())
    self.sprites.append(pygame.image.load(resource_path(join("assets", "img" ,"Winflag_animation3.png"))).convert_alpha())
    self.sprites.append(pygame.image.load(resource_path(join("assets", "img" ,"Winflag_animation4.png"))).convert_alpha())
    self.sprites.append(pygame.image.load(resource_path(join("assets", "img" ,"Winflag_animation5.png"))).convert_alpha())
    self.sprites.append(pygame.image.load(resource_path(join("assets", "img" ,"Winflag_animation6.png"))).convert_alpha())
    self.sprites.append(pygame.image.load(resource_path(join("assets", "img" ,"Winflag_animation7.png"))).convert_alpha())


    self.image = self.sprites[self.current_sprite]
    self.rect = self.image.get_rect(center = position)

    self.text = GIGA_TITLE.render("Congratulations!", True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)
    
  def update(self):
    self.screen.blit(self.text, self.text_rect)
    self.animation()

  def animation(self):
    self.current_sprite += 0.1
    if self.current_sprite >= len(self.sprites):
        self.current_sprite = 0
    self.image = self.sprites[int(self.current_sprite)]

  def update_position(self, position):
    self.rect = self.image.get_rect(center = position)
    self.text_rect = self.text.get_rect(center = self.rect.center)