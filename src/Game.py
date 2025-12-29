from config.settings import *
from os.path import join
from states.MenuState import *
from utils.Cursor import *
from utils.EventManager import *
from states.StateMachine import *
from utils.Background import *
from utils.FileManager import *
from utils.PathHandler import *
from states.PlayState import *
from states.InstructionsState import *
from states.CreditsState import *
from states.CategoryState import *
from states.LeaderboardState import *
from states.ManageQuestionsState import *
from states.WinState import *
from states.GameOverState import *
from states.DifficultyState import *
from states.PracticeSummaryState import *
from states.QuestionsState import *
from states.EditState import * 
from states.AddState import *
from states.PlayerState import *
from states.LifelineInstructions import *
from utils.SoundController import *
from states.GamemodeInstructions import *


class Game:
  def __init__(self):
    # Initialize the game
    pygame.init()
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), RESIZABLE )
    self.icon_path = resource_path(join("assets", "img", "logo.png"))
    self.icon_surface = pygame.image.load(self.icon_path)
    pygame.display.set_caption("Who wants to be a millionaire?")
    pygame.display.set_icon(self.icon_surface)
    self.clock = pygame.time.Clock()
    self.fps = 60
    self.running = True
    pygame.mixer.music.load(resource_path(join("assets", "sounds", "bg_music.mp3")))
    pygame.mixer.music.set_volume(0.3)  # Set volume (0.0 to 1.0, where 1.0 is the max volume)
    pygame.mixer.music.play(-1, 0.0)
    pygame.mouse.set_visible(False)

    # groups
    self.global_sprites = pygame.sprite.Group()

    # Initialize objects
    self.event_manager = EventManager()
    self.background = Background()
    self.sound_controller = SoundController(self.global_sprites, self.event_manager)
    self.cursor = Cursor(self.global_sprites, self.event_manager)
    # Load data before initializing the states
    self.file_manager = FileManager(self.event_manager)
    self.file_manager.set_up_file_events()
    self.event_manager.notify("load_data")
    
    # Validate questions file integrity
    is_valid, errors = self.file_manager.validate_questions()
    if not is_valid:
      print("\n" + "="*70)
      print("ERROR: Questions file validation failed!")
      print("="*70)
      for error in errors:
        print(f"  • {error}")
      print("="*70 + "\n")
      raise RuntimeError(f"Invalid questions file. Found {len(errors)} error(s). See console output above.")
    
    # Initialize states
    self.state_machine = StateMachine(self.event_manager)
    self.menu = Menu(self.event_manager)
    self.play = Play(self.event_manager, self.file_manager)
    self.instructions = Instructions(self.event_manager)
    self.manage_questions = ManageQuestions(self.event_manager)
    self.credits = Credits(self.event_manager)
    self.leaderboard = Leaderboard(self.event_manager)
    self.win = Win(self.event_manager)
    self.game_over = GameOver(self.event_manager)
    self.difficulty = Difficulty(self.event_manager)
    self.practice_summary = Practice(self.event_manager)
    self.questions = Questions(self.event_manager , self.file_manager)
    self.edit = Edit(self.event_manager)
    self.add = Add(self.event_manager)
    self.player = Player(self.event_manager)
    self.lifeline_instructions = LifelineInstrucitions(self.event_manager)
    self.gamemode_instructions = GamemodeInstrucitions(self.event_manager)
    self.categories = Categories(self.event_manager, self.file_manager)

    # Add states to the state_machine
    self.state_machine.add_state("menu", self.menu)
    self.state_machine.add_state("game", self.play)
    self.state_machine.add_state("instructions", self.instructions)
    self.state_machine.add_state("levels", self.manage_questions)
    self.state_machine.add_state("credits", self.credits)
    self.state_machine.add_state("leaderboard", self.leaderboard)
    self.state_machine.add_state("win", self.win)
    self.state_machine.add_state("game over", self.game_over)
    self.state_machine.add_state("difficulty", self.difficulty)
    self.state_machine.add_state("practice summary", self.practice_summary)
    self.state_machine.add_state("questions", self.questions)
    self.state_machine.add_state("edit", self.edit)
    self.state_machine.add_state("add", self.add)
    self.state_machine.add_state("player", self.player)
    self.state_machine.add_state("lifeline_instructions", self.lifeline_instructions)
    self.state_machine.add_state("gamemode_instructions", self.gamemode_instructions)
    self.state_machine.add_state("categories", self.categories)
    
    #set up events
    self.set_up_game_events()
    self.menu.set_up_menu_events()
    self.state_machine.set_up_machine_events()
    self.cursor.set_up_cursor_events()
    self.play.set_up_play_events()
    self.instructions.set_up_instruction_events()
    self.win.set_up_win_events()
    self.game_over.set_up_game_over_events()
    self.practice_summary.set_up_practice_events()
    self.questions.set_up_question_events()
    self.edit.set_up_edit_events()
    self.add.set_up_add_events()
    self.player.set_up_player_events()
    self.leaderboard.set_up_leaderboard_events()
    self.difficulty.set_up_difficulty_events()
    self.credits.set_up_credits_events()
    self.manage_questions.set_up_manage_events()
    self.lifeline_instructions.set_up_lifeline_instructins_events()
    self.gamemode_instructions.set_up_gamemode_instructins_events()
    self.categories.set_up_category_events();

    #default state
    self.event_manager.notify("set_state", "menu")
    
  def stop_game(self, *args):
    self.running = False

  def run(self):
    min_width, min_height = WINDOW_WIDTH, WINDOW_HEIGHT
    while self.running:
        self.clock.tick(self.fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_game()
            elif event.type == VIDEORESIZE:
              new_width = max(event.dict['size'][0], min_width)
              new_height = max(event.dict['size'][1], min_height)
              self.screen = pygame.display.set_mode((new_width, new_height), RESIZABLE)
              self.background.update_elements_size()
              self.sound_controller.update_position()
              self.event_manager.notify("update_size")

            # Handle keyboard
            if event.type == pygame.KEYDOWN:
                self.event_manager.notify("keyboard_input", event)

        # Draw
        self.background.draw_background()

        # Update
        self.global_sprites.update()

        # Event_handler
        self.state_machine.handle_events("update_state")
        self.sound_controller.update()

        # Draw global sprites last to ensure they are rendered on top of all other elements
        self.global_sprites.draw(self.screen)

        pygame.display.update()

    pygame.quit()


  def set_up_game_events(self):
    self.event_manager.subscribe("stop_game", self.stop_game)

