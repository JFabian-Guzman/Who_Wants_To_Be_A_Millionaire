from abc import ABC, abstractmethod
from utils.EventManager import *

class State(ABC):
  def __init__(self, event_manager: EventManager):
    self.event_manager = event_manager

  @abstractmethod
  def draw(self):
    pass

  @abstractmethod
  def update(self):
    pass

  def listen(self, state):
    self.current_state = state

  def on(self):
    self.draw()
    self.update()
