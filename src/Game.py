from config.settings import *
from os.path import join
from screens.Menu import *

class Game: 
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Who wants to be a millionaire?")
    self.clock = pygame.time.Clock()
    self.running = True

    # groups 
    self.all_sprites = pygame.sprite.Group()

    # Menu
    self.menu = Menu()

    # Background
    background_img = pygame.image.load(join("assets","img" , "background.jpeg")).convert()
    background = pygame.transform.scale(background_img, self.screen.get_size())

    # Logo
    ucr_logo = pygame.image.load(join("assets", "img", "ucr_logo.png")).convert_alpha()
    ucr_logo = pygame.transform.scale(ucr_logo, (300, 50))
    elm_logo = pygame.image.load(join("assets", "img", "elm_logo.png")).convert_alpha()
    elm_logo = pygame.transform.scale(elm_logo, (300, 50))
    elm_rect = elm_logo.get_rect(center = (WINDOW_WIDTH // 2, 25))
    tcu_logo = pygame.image.load(join("assets", "img", "tcu_logo.png")).convert_alpha()

    overlay = pygame.Surface(self.screen.get_size())
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128) # Transparency level

    banner = pygame.Surface(BANNER["SIZE"])
    banner.fill(COLORS["WHITE"])

    banner.blit(ucr_logo, (0, 0))
    banner.blit(elm_logo, elm_rect)

    self.screen.blit(background, (0,0))
    self.screen.blit(overlay, (0, 0)) # Reduce the brightness of the background
    self.screen.blit(banner, (0, WINDOW_HEIGHT - 50))
  
  def run(self):
    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
      #draw
      pygame.display.update()
      self.menu.draw()
    pygame.quit()