from .State import *
from utils.EventManager import *

class StateMachine:
  def __init__(self, event_manager: EventManager):
    self.event_manager = event_manager
    self.current_state = None
    self.states = dict()

  def add_state(self, name: str ,state: State):
    if name in self.states:
      raise ValueError(f"State '{name}' is already added to the StateMachine.")
    self.states[name] = state

  def set_state(self, state: str):
    if state == "play":
      state = "instructions"
      print("DISPLAY")
      self.event_manager.notify("display_continue_btn")
    elif state == "game":
      pygame.mixer.music.stop()
      self.event_manager.notify("play_start_game_sound")
      self.load_game()
    elif state == "instructions":
      print("ERASING")
      self.event_manager.notify("erase_continue_btn")
    elif state == "questions":
      self.event_manager.notify("load_data")
      self.event_manager.notify("fetch_questions")
    elif state == "leaderboard":
      self.event_manager.notify("get_podium")
    elif state == "win":
      self.event_manager.notify("play_win_sound")
    elif state == "game over":
      self.event_manager.notify("play_game_over_sound")
    elif state == "menu":
      if not pygame.mixer.music.get_busy():
          pygame.mixer.music.play(-1, 0.0)


    self.current_state = self.states[state]
    self.current_state.set_click_handle(True)

  def load_game(self):
    self.event_manager.notify("load_data")
    self.event_manager.notify("start_game")
    self.event_manager.notify("choose_random_question")
    self.event_manager.notify("display_question")
    self.event_manager.notify("shuffle_options")

  def update_state(self, *args):
    if self.current_state:
      self.current_state.on()

  def set_up_machine_events(self):
    self.event_manager.subscribe("update_state", self.update_state)
    self.event_manager.subscribe("set_state", self.set_state)

  def handle_events(self, event: str, data = ''):
    self.event_manager.notify(event, data)
