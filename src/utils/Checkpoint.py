from config.settings import *
from os.path import join

class Checkpoint(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.screen = pygame.display.get_surface()
    self.sprites = []
    self.current_sprite = 0
    self.run_animation = False

    self.sprites.append(pygame.image.load(join("assets", "img", 'btn.png')).convert_alpha())
    self.sprites.append(None)
    self.sprites.append(pygame.image.load(join("assets", "img", 'btn.png')).convert_alpha())
    self.sprites.append(None)
    self.sprites.append(pygame.image.load(join("assets", "img", 'btn.png')).convert_alpha())
    self.sprites.append(None)
    self.sprites.append(pygame.image.load(join("assets", "img", 'btn.png')).convert_alpha())
    self.sprites.append(None)

    self.image = self.sprites[self.current_sprite]
    self.rect = self.image.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))

    self.text = TEXT.render("Checkpoint", True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center=self.rect.center)

  def draw(self):
    if self.image:
      self.screen.blit(self.image, self.rect)

  def update(self):
    if self.image:
      self.write_text()
    self.animate()

  def write_text(self):
    self.screen.blit(self.text, self.text_rect)

  def animate(self):
    self.current_sprite += 0.05
    if self.current_sprite >= len(self.sprites):
        self.current_sprite = len(self.sprites) - 1
        self.stop_animation()
    self.image = self.sprites[int(self.current_sprite)]

  def start_animation(self):
    self.run_animation = True

  def stop_animation(self):
    self.run_animation = False

  def restart_animation(self):
    self.current_sprite = 0