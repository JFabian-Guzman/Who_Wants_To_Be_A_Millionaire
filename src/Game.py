from config.settings import *
from os.path import join
from states.MenuState import *
from utils.Cursor import *
from utils.Groups import *
from utils.EventManager import *
from states.StateMachine import *
from utils.Background import *
from states.PlayState import *

class Game: 
  def __init__(self):
    # Initialize the game
    pygame.init()
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Who wants to be a millionaire?")
    self.clock = pygame.time.Clock()
    self.fps = 60
    self.running = True
    self.event_manager = EventManager()
    pygame.mouse.set_visible(False)

    # groups
    self.global_sprites = pygame.sprite.Group()

    # Initialize objects
    self.background = Background()
    self.cursor = Cursor(self.global_sprites, self.event_manager)
    self.menu = Menu(self.event_manager,self.cursor)
    self.play = Play(self.event_manager, self.cursor)
    self.state_machine = StateMachine(self.event_manager)

    # Add states to the state_machine
    self.state_machine.add_state("menu", self.menu)
    self.state_machine.add_state("Play", self.play)

    #set up events
    self.state_machine.set_up_machine_events()
    self.cursor.set_up_cursor_events()

    #default state
    self.event_manager.notify("set_state", "menu")

  def run(self):
    while self.running:
      # dt = self.clock.tick() / 1000
      # fps = self.clock.get_fps()  
      # print(f"FPS: {fps:.2f}")
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
      # Draw
      self.background.draw_background()

      # Update
      self.global_sprites.update()

      # Event_handler
      self.state_machine.handle_events("update_state")

      # Draw global sprites last to ensure they are rendered on top of all other elements
      self.global_sprites.draw(self.screen)

      pygame.display.update()
      self.clock.tick(self.fps)
    pygame.quit()