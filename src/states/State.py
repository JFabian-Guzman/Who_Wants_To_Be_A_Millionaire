from abc import ABC, abstractmethod

class State(ABC):
  def __init__(self):
    self.current_state = 'Menu'

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
  