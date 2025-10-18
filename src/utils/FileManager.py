from os.path import isfile, join
import shutil
import os
import json
from utils.PathHandler import *

class FileManager():
  def __init__(self, event_manager):
    super().__init__()
    self.podium_file = os.path.join(os.getenv("LOCALAPPDATA"), "Millionaire", "podium.json")
    self.questions_file = os.path.join(os.getenv("LOCALAPPDATA"), "Millionaire", "questions.json")
    self.categories_file = os.path.join(os.getenv("LOCALAPPDATA"), "Millionaire", "categories.json")
    os.makedirs(os.path.dirname(self.podium_file),exist_ok=True)
    os.makedirs(os.path.dirname(self.questions_file),exist_ok=True)
    os.makedirs(os.path.dirname(self.categories_file),exist_ok=True)
    self.load_questions_to_local_storage()
    self.data = [[]]
    self.categories = []
    self.event_manager = event_manager

  def load_questions_to_local_storage(self): 
    quesitons_data = join("data", "Questions.json")
    categories_data = join("data", "Categories.json")
    if not os.path.exists(self.categories_file): 
      shutil.copy(categories_data, self.categories_file)
    if not os.path.exists(self.questions_file): 
      shutil.copy(quesitons_data, self.questions_file)

  def load_data(self, *args):
    if isfile(self.categories_file):
      with open(self.categories_file, "r", encoding="utf-8") as file:
        data_file = json.load(file)
        for categorie in data_file:
          self.categories.append(categorie)
    if isfile(self.questions_file):
      with open(self.questions_file, "r", encoding="utf-8") as file:
        data_file = json.load(file)
        # 15 = Difficulty levels
        self.data = [[] for row in range(15)]
        for data in data_file:
          self.data[data["level"]].append(data)


  def edit_file(self, *args):
        data = args[0]
        new_data = {
          "question": data[0],
          "options": [data[1], data[2], data[3], data[4]],
          "answer": data[5],
        }
        id = data[6]

        # Load data
        with open(self.questions_file, "r", encoding="utf-8") as file:
            try:
                data_file = json.load(file)
            except json.JSONDecodeError:
                print("Error: JSON file is corrupted.")
                return
        
        # Search and modify
        updated = False
        for obj in data_file:
            if obj.get("id") == id:
                obj.update(new_data)  
                updated = True
                break  

        # Save it in the file
        if updated:
            # Save the modified data back to the file
            with open(self.questions_file, "w", encoding="utf-8") as file:
                json.dump(data_file, file, indent=4)
        else:
            print(f"Error: Object with ID {id} not found.")

  def add_file(self, *args):
        data = args[0]
        new_data = {
          "id": '',
          "question": data[0],
          "answer": data[5],
          "options": [data[1], data[2], data[3], data[4]],
          "level": data[6]
        }
  
        # Load data
        with open(self.questions_file, "r", encoding="utf-8") as file:
            try:
                data_file = json.load(file)
            except json.JSONDecodeError:
                print("Error: JSON file is corrupted.")
                return

        # Find the next ID
        last_id = max((obj.get("id", -1) for obj in data_file), default=-1)
        new_id = last_id + 1
        new_data["id"] = new_id

        data_file.append(new_data)

        with open(self.questions_file, "w", encoding="utf-8") as file:
            json.dump(data_file, file, indent=4)

  def delete(self, *args):
    id = args[0]
    # Load data
    with open(self.questions_file, "r", encoding="utf-8") as file:
        try:
            data_file = json.load(file)
        except json.JSONDecodeError:
            print("Error: JSON file is corrupted.")
            return
    
    # Search and delete
    initial_length = len(data_file)
    data_file = [obj for obj in data_file if obj.get("id") != id]
    
    if len(data_file) == initial_length:
        print(f"Error: Object with ID {id} not found.")
        return
    
    # Save the modified data back to the file
    with open(self.questions_file, "w", encoding="utf-8") as file:
        json.dump(data_file, file, indent=4)

  def create_player_file(self):
    if not os.path.exists(self.podium_file):
        with open(self.podium_file, "w", encoding="utf-8") as f:
            json.dump([], f)

  def get_podium(self, *args):
    self.create_player_file()
    if not os.path.exists(self.podium_file):  
      return []

    with open(self.podium_file, "r", encoding="utf-8") as file:
      data_file = json.load(file)
    self.event_manager.notify("set_podiums", data_file)

  def write_podium(self, *args):
    data = args[0]
    new_player = {
      "Name": data[0],
      "Points": data[1]
    }
    self.create_player_file()
    if not os.path.exists(self.podium_file):  
      return []
    with open(self.podium_file, "r", encoding="utf-8") as file:
      players = json.load(file)

    players.append(new_player)
    sorted_players = sorted(players, key=lambda player: player["Points"], reverse=True)
    # Top 5
    if len(sorted_players) > 5:
      sorted_players.pop()
    with open(self.podium_file, "w", encoding="utf-8") as file:
        json.dump(sorted_players, file, indent=4)

  def get_data(self):
    return self.data
  
  def get_categories(self):
    return self.categories
  
  def get_last_level(self):
    for level in range(len(self.data)):
        if not self.data[level]:  
            return level if level > 0 else 0
    return len(self.data) 

  def set_up_file_events(self):
    self.event_manager.subscribe("load_data", self.load_data)
    self.event_manager.subscribe("edit_file", self.edit_file)
    self.event_manager.subscribe("add_file", self.add_file)
    self.event_manager.subscribe("delete", self.delete)
    self.event_manager.subscribe("get_podium", self.get_podium)
    self.event_manager.subscribe("write_podium", self.write_podium)