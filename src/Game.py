from config.settings import *
from os.path import join
from states.MenuState import *
from utils.Cursor import *
from utils.Groups import *
from utils.EventManager import *
from states.StateMachine import *
from utils.Background import *
from utils.FileManager import *
from states.PlayState import *
from states.InstructionsState import *
from states.CreditsState import *
from states.GlossaryState import *
from states.ManageQuestionsState import *
from states.RewardState import *
from states.WinState import *
from states.GameOverState import *

class Game:
  def __init__(self):
    # Initialize the game
    pygame.init()
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Who wants to be a millionaire?")
    self.clock = pygame.time.Clock()
    self.fps = 60
    self.running = True
    pygame.mouse.set_visible(False)

    # groups
    self.global_sprites = pygame.sprite.Group()

    # Initialize objects
    self.event_manager = EventManager()
    self.background = Background()
    self.cursor = Cursor(self.global_sprites, self.event_manager)
    # Load data before initializing the states
    self.file_manager = FileManager(self.event_manager)
    self.file_manager.set_up_file_events()
    self.event_manager.notify("load_data")
    # Initialize states
    self.state_machine = StateMachine(self.event_manager)
    self.menu = Menu(self.event_manager)
    self.play = Play(self.event_manager, self.file_manager)
    self.instructions = Instructions(self.event_manager)
    self.manage_questions = ManageQuestions(self.event_manager)
    self.credits = Credits(self.event_manager)
    self.glossary = Glossary(self.event_manager)
    self.rewards = Rewards(self.event_manager)
    self.win = Win(self.event_manager)
    self.game_over = GameOver(self.event_manager)
    

    # Add states to the state_machine
    self.state_machine.add_state("menu", self.menu)
    self.state_machine.add_state("game", self.play)
    self.state_machine.add_state("instructions", self.instructions)
    self.state_machine.add_state("manage questions", self.manage_questions)
    self.state_machine.add_state("credits", self.credits)
    self.state_machine.add_state("glossary", self.glossary)
    self.state_machine.add_state("rewards", self.rewards)
    self.state_machine.add_state("win", self.win)
    self.state_machine.add_state("game over", self.game_over)

    #set up events
    self.set_up_game_events()
    self.state_machine.set_up_machine_events()
    self.cursor.set_up_cursor_events()
    self.play.set_up_play_events()
    self.instructions.set_up_instruction_events()
    self.win.set_up_win_events()
    self.game_over.set_up_game_over_events()

    #default state
    self.event_manager.notify("set_state", "menu")
    

  def stop_game(self, *args):
    self.running = False

  def run(self):
    while self.running:
      dt = self.clock.tick() / 1000
      fps = self.clock.get_fps()  
      # print(f"FPS: {fps:.2f}")
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.stop_game()
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


  def set_up_game_events(self):
    self.event_manager.subscribe("stop_game", self.stop_game)

