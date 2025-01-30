from State import *
from utils.Publisher import *

class StateMachine:
  def __init__(self, publisher: Publisher):
    self.publisher = publisher
    self.current_state = None
    self.states = dict()

  def add_state(self, name: str ,state: State):
    if name in self.states:
      raise ValueError(f"State '{name}' is already added to the StateMachine.")
    self.states[name] = state

  def update_state(self, state: str):
    if self.current_state:
      self.current_state.off()

    if state not in self.states:
      raise ValueError(f"State '{state}' does not exist in the StateMachine.")

    self.current_state = self.states[state]
    self.current_state.on()
  

  def set_up_events(self, event: str, *args):
    self.pusblisher.subrscribe("update_state", self.update_state)

