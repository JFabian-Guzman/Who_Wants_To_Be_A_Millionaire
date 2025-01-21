from config.settings import *
from os.path import join

class Game: 
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Who wants to be a millionaire?")
    self.clock = pygame.time.Clock()
    self.running = True

    # Background
    background_img = pygame.image.load(join("assets", "background.jpeg")).convert()
    background = pygame.transform.scale(background_img, self.screen.get_size())

    overlay = pygame.Surface(self.screen.get_size())
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128) # Transparency level

    self.screen.blit(background, (0,0))
    self.screen.blit(overlay, (0, 0)) # Reduce the brightness of the background
  
  def run(self):
    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
      #draw
      pygame.display.update()
    pygame.quit()