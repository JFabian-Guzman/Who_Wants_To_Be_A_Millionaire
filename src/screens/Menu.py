from config.settings import *
from os.path import join

class Menu:
  def __init__(self):
    super().__init__()
    self.screen = pygame.display.get_surface()

  def option(self, title, position):
    option = pygame.image.load(join("assets", "img" ,"option.png")).convert_alpha()
    option_rect = option.get_rect(center = position)
    self.screen.blit(option, option_rect)

    # Initialize font
    pygame.font.init()
    font = pygame.font.Font(join("assets", "fonts", "PixelifySans-Regular.ttf"), 40)  
    
    # Render text
    text = font.render(title, True, COLORS["WHITE"])  # White color
    text_rect = text.get_rect(center = option_rect.center)  
    
    # Blit text onto the screen
    self.screen.blit(text, text_rect)


  def logo(self):
    logo = pygame.image.load(join("assets", "img" ,"logo.png")).convert_alpha()
    logo_rect = logo.get_rect(center=(WINDOW_WIDTH//2, 200))
    self.screen.blit(logo, logo_rect)

  def draw(self):
    self.logo()
    for option in MENU:
        self.option(option["TITLE"], option["POSITION"])

