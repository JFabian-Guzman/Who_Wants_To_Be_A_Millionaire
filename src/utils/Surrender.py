from config.settings import *
from os.path import join


SURRENDER_POSITION = (300,90)
class Surrender(pygame.sprite.Sprite):
  def __init__(self, groups, event_manager):
    super().__init__(groups)
    self.screen = pygame.display.get_surface()
    self.event_manager = event_manager
    self.click_handled = False
    self.current_level = 0
    self.disable = False
    self.is_modal_display = False
    self.run_animation = False

    self.sprites = []
    self.current_sprite = 0

    self.sprites.append(pygame.image.load(join("assets", "img", 'btn.png')).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img", "hover_btn_animation1.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img", "hover_btn_animation2.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img", "hover_btn_animation3.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img", "hover_btn_animation4.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img", "hover_btn_animation5.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img", "hover_btn_animation6.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img", "hover_btn_animation7.png")).convert_alpha())
    self.sprites.append(pygame.image.load(join("assets", "img", "hover_btn_animation8.png")).convert_alpha())  

    self.image = pygame.image.load(join("assets", "img" ,"btn.png")).convert_alpha()
    self.rect = self.image.get_rect(center = SURRENDER_POSITION)
    
    self.text = TEXT.render("Surrender", True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def update(self):
    self.screen.blit(self.text, self.text_rect)
    if not self.is_modal_display:
      self.check_surrender()
    if self.run_animation:
      self.animate()

  def set_level(self, level):
    self.current_level = level

  def set_disable(self, *args):
    self.disable = args[0]

  def check_surrender(self):
    if pygame.mouse.get_pressed()[0] and not self.disable: 
        if not self.click_handled:
          if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.event_manager.notify("display_surrender_modal")
          self.click_handled = True
          return
    else:
        self.click_handled = False

  def on_hover(self):
    self.start_animation()

  def reset_hover(self):
    self.current_sprite = 0 
    self.image = self.sprites[self.current_sprite]

  def switch_modal_display(self):
    self.is_modal_display = not self.is_modal_display

  def animate(self):
    self.current_sprite += 0.8
    if self.current_sprite >= len(self.sprites):
        self.current_sprite = len(self.sprites) - 1
        self.stop_animation()
    self.image = self.sprites[int(self.current_sprite)]

  def start_animation(self):
    self.run_animation = True

  def stop_animation(self):
    self.run_animation = False