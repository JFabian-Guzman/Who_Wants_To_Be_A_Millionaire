from config.settings import *

class Game: 
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Who wants to be a millionaire?")
    self.clock = pygame.time.Clock()
    self.running = True
  
  def run(self):
    while self.running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
      self.screen.fill((0, 0, 0))
      pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
  game = Game()
  game.run()