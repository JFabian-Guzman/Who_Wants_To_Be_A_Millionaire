from .State import *
from utils.EventManager import *

class StateMachine:
  def __init__(self, event_manager: EventManager):
    self.event_manager = event_manager
    self.current_state = None
    self.states = dict()
    self.isUpdated = False

  def add_state(self, name: str ,state: State):
    if name in self.states:
      raise ValueError(f"State '{name}' is already added to the StateMachine.")
    self.states[name] = state

  def set_state(self, state: str):
    if self.current_state:
      self.current_state.off()
    self.isUpdated = False
    self.current_state = self.states[state]
    self.isUpdated = True

  def update_state(self, data):
    # print("UPDATE STATE ", state)
    # if self.current_state:
    #   self.current_state.off()

    # self.current_state = self.states[state]
    if self.current_state and self.isUpdated:
      self.current_state.on()

  def set_up_machine_events(self):
    self.event_manager.subscribe("update_state", self.update_state)
    self.event_manager.subscribe("set_state", self.set_state)

  def handle_events(self, event: str, data):
    self.event_manager.notify(event, data)
