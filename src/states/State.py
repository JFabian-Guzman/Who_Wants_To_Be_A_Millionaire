from abc import ABC, abstractmethod
from utils.Publisher import *

class State(ABC):
  def __init__(self, publisher: Publisher):
    self.publisher = publisher

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

  def off(self):
    pass
  