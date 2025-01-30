from config.settings import *
from os.path import join
from states.Menu import *
from utils.Cursor import *
from utils.Groups import *
from utils.Publisher import *
from states.StateMachine import *

class Game: 
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Who wants to be a millionaire?")
    self.clock = pygame.time.Clock()
    self.fps = 60
    self.running = True
    self.publisher = Publisher()
    pygame.mouse.set_visible(False)

    # groups 
    self.global_sprites = pygame.sprite.Group()

    # Menu
    self.cursor = Cursor(self.global_sprites)
    self.menu = Menu(self.publisher,self.cursor)
    self.state_machine = StateMachine(self.publisher)

    # Add states to the state_machine
    self.state_machine.add_state("menu", self.menu)

    #set_up_events
    self.menu.set_up_menu_handlers()
    self.state_machine.set_up_events()

    # Background
    background_img = pygame.image.load(join("assets","img" , "background.jpeg")).convert()
    self.background = pygame.transform.scale(background_img, self.screen.get_size())
    self.overlay = pygame.Surface(self.screen.get_size())
    self.overlay.fill((0, 0, 0))
    self.overlay.set_alpha(128) # Transparency level
    self.banner = pygame.Surface(BANNER["SIZE"])
    self.banner_rect = self.banner.get_rect(bottom = WINDOW_HEIGHT)
    
  
  def draw_banner(self):
    self.banner.fill(COLORS["WHITE"])
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

    self.banner.blit(ucr_logo, ucr_rect)
    self.banner.blit(elm_logo, elm_rect)
    self.banner.blit(tcu_logo, tcu_rect)
    self.screen.blit(self.banner, self.banner_rect)

  def draw_background(self):
    self.screen.blit(self.background, (0, 0))
    self.screen.blit(self.overlay, (0, 0))
    self.draw_banner()


  def run(self):
    while self.running:
      dt = self.clock.tick() / 1000
      fps = self.clock.get_fps()  
      # print(f"FPS: {fps:.2f}")
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
      #draw
      self.draw_background()
      
      self.global_sprites.update()

      self.state_machine.handle_events("update_state","menu")
      self.state_machine.handle_events("test")

      self.global_sprites.draw(self.screen)
      pygame.display.update()
      self.clock.tick(self.fps)
    pygame.quit()