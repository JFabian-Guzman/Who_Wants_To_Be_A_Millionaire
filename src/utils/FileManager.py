from os.path import isfile, join
import json

class FileManager():
  def __init__(self, event_manager):
    super().__init__()
    self.data = [[]]
    self.event_manager = event_manager

  def load_data(self, *args):
    print("loaded")
    if isfile(join("data", "Questions.json")):
      with open(join("data", "Questions.json"), "r") as file:
        data_file = json.load(file)
        # 15 = Difficulty levels
        self.data = [[] for row in range(15)]
        for data in data_file:
          self.data[data["level"]].append(data)

  def get_data(self):
    return self.data

  def set_up_file_events(self):
    self.event_manager.subscribe("load_data", self.load_data)
