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

  def update_state(self, state: str):
    if self.current_state:
      self.current_state.off()

    self.current_state = self.states[state]
    self.current_state.on()

  def set_up_machine_events(self):
    self.event_manager.subscribe("update_state", self.update_state)

  def handle_events(self, event: str, data):
    self.event_manager.notify(event, data)
