from config.settings import *
from os.path import join

class Option:
  def __init__(self, text , position):
    super().__init__()
    self.sprite = pygame.image.load(join("assets", "img" ,"option.png")).convert_alpha()
    self.rect = self.sprite.get_rect(center = position)
    self.screen = pygame.display.get_surface()
    self.text = text

  def write_text(self):
    # Initialize font
    pygame.font.init()
    font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 20)  
    
    # Render text
    text = font.render(self.text, True, COLORS["WHITE"])  # White color
    text_rect = text.get_rect(center = self.rect.center) 
    
    # Blit text onto the screen
    self.screen.blit(text, text_rect)

  def draw(self):
    self.screen.blit(self.sprite, self.rect)
    self.write_text()



