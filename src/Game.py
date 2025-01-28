from config.settings import *
from os.path import join
from screens.Menu import *
from utils.Cursor import *
from utils.Groups import *

class Game: 
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Who wants to be a millionaire?")
    self.clock = pygame.time.Clock()
    self.fps = 60
    self.running = True
    pygame.mouse.set_visible(False)

    # groups 
    self.global_sprites = pygame.sprite.Group()

    # Menu
    self.cursor = Cursor(self.global_sprites)
    self.menu = Menu(self.cursor)

    # Background
    background_img = pygame.image.load(join("assets","img" , "background.jpeg")).convert()
    self.background = pygame.transform.scale(background_img, self.screen.get_size())
    self.overlay = pygame.Surface(self.screen.get_size())
    self.overlay.fill((0, 0, 0))
    self.overlay.set_alpha(128) # Transparency level
    banner = pygame.Surface(BANNER["SIZE"])
    self.draw_banner(banner)



    self.screen.blit(banner, (0, WINDOW_HEIGHT - 70))
    
  
  def draw_banner(self, banner):
    banner.fill(COLORS["WHITE"])
    # logos
    ucr_logo = pygame.image.load(join("assets", "img", "ucr_logo.png")).convert_alpha()
    ucr_logo = pygame.transform.scale(ucr_logo, (300, 60))
    ucr_rect = ucr_logo.get_rect(left=0, centery = BANNER["SIZE"][1] // 2)
    elm_logo = pygame.image.load(join("assets", "img", "elm_logo.png")).convert_alpha()
    elm_logo = pygame.transform.scale(elm_logo, (300, 50))
    elm_rect = elm_logo.get_rect(center = (WINDOW_WIDTH // 2, BANNER["SIZE"][1] // 2))
    tcu_logo = pygame.image.load(join("assets", "img", "tcu_logo.png")).convert_alpha()
    tcu_logo = pygame.transform.scale(tcu_logo, (30, 60))
    tcu_rect = tcu_logo.get_rect(center = (WINDOW_WIDTH - 100, BANNER["SIZE"][1] // 2))

    banner.blit(ucr_logo, ucr_rect)
    banner.blit(elm_logo, elm_rect)
    banner.blit(tcu_logo, tcu_rect)

  def run(self):
    while self.running:
      dt = self.clock.tick() / 1000
      fps = self.clock.get_fps()  
      print(f"FPS: {fps:.2f}")
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
      #draw
      self.screen.blit(self.background, (0,0))
      self.screen.blit(self.overlay, (0, 0)) # Reduce the brightness of the background
      # self.menu.draw()
      # self.cursor.draw()
      # self.cursor.update()
      # self.menu.update()
      self.global_sprites.update()

      self.menu.draw()
      self.menu.update()

      self.global_sprites.draw(self.screen)
      pygame.display.update()
      self.clock.tick(self.fps)
    pygame.quit()