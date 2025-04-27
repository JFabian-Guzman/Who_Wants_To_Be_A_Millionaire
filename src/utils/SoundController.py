from config.settings import *
from os.path import join

class SoundController(pygame.sprite.Sprite):
  def __init__(self, group, event_manager):
    super().__init__(group)
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.on = True
    self.click_handled = False

    self.event_manager = event_manager

    self.sound_on = pygame.image.load(join("assets", "img", "sound_on.png")).convert_alpha()
    self.sound_off = pygame.image.load(join("assets", "img", "sound_off.png")).convert_alpha()

    position = (self.width - 50, 50)
    self.image = self.sound_on
    self.rect = self.image.get_rect(center=position)

  def draw(self):
    self.screen.blit(self.image, self.rect)

  def update(self):
    self.check_hover()
    self.check_click()

  def check_click(self):
    if pygame.mouse.get_pressed()[0]:
      if self.rect.collidepoint(pygame.mouse.get_pos()):
        if not self.click_handled:
          self.switch()
          self.click_handled = True
    else:
      self.click_handled = False

  def check_hover(self):
    if self.rect.collidepoint(pygame.mouse.get_pos()):
      self.event_manager.notify("change_cursor", 'hover')

  def switch(self):
    self.on = not self.on
    if self.on == True:
      self.turn_on()
    else:
      self.turn_off()

  def turn_on(self):
    pygame.mixer.music.set_volume(0.3)  # Restore volume
    for i in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(i).set_volume(1)  # Restore sound effects volume
    self.image = self.sound_on

  def turn_off(self):
    pygame.mixer.music.set_volume(0)  # Mute music
    for i in range(pygame.mixer.get_num_channels()):
        pygame.mixer.Channel(i).set_volume(0)  # Mute all sound effects
    self.image = self.sound_off
  

  def update_position(self):
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    position = (self.width - 50, 50)
    self.rect = self.image.get_rect(center=(position))
