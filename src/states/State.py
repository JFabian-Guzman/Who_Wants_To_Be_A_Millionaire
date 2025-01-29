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

  def on(self):
    self.draw()
    self.update()

  def off(self):
    pass
  