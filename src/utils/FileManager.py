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
        # Default new questions to inactive
        new_data["active"] = "False"
  
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
  
  def get_selected_category(self):
    for category in self.categories:
      if category["selected"]:
        return category["category"]

  def get_last_level(self):
    for level in range(len(self.data)):
        if not self.data[level]:  
            return level if level > 0 else 0
    return len(self.data)
  
  def set_category(self, new_category):
    for category in self.categories:
      if category["category"] == new_category:
        category["selected"] = True
      else:
        category["selected"] = False
    try:
      with open(self.categories_file, "w", encoding="utf-8") as f:
        json.dump(self.categories, f, indent=2, ensure_ascii=False)
    except Exception as e:
      print("Error saving categories file:", e)

  def check_selected_question(self, *args):
    """Search for a question with the given id in the questions file.
    Notifies "check_selected_question_result" with a tuple (id, found_bool).
    """
    id = args[0]
    found = False
    # Load data
    try:
      with open(self.questions_file, "r", encoding="utf-8") as file:
        data_file = json.load(file)
    except Exception:
      data_file = []

    # search nested lists as well as top-level objects
    def _iter_items(items):
      for item in items:
        if isinstance(item, dict):
          yield item
        elif isinstance(item, list):
          for sub in _iter_items(item):
            yield sub

    for obj in _iter_items(data_file):
      if obj.get("id") == id:
        # interpret 'active' which may be a string or boolean
        active = obj.get("active", False)
        if isinstance(active, str):
          found = active.strip().lower() == "true"
        else:
          found = bool(active)
        break

    # Notify result
    try:
      self.event_manager.notify("check_selected_question_result", (id, found))
    except Exception:
      pass

  def is_question_active(self, id):
    """Return True if question with id has active set to True (string or bool)."""
    try:
      with open(self.questions_file, "r", encoding="utf-8") as file:
        data_file = json.load(file)
    except Exception:
      return False

    def _iter_items(items):
      for item in items:
        if isinstance(item, dict):
          yield item
        elif isinstance(item, list):
          for sub in _iter_items(item):
            yield sub

    for obj in _iter_items(data_file):
      if obj.get("id") == id:
        active = obj.get("active", False)
        if isinstance(active, str):
          return active.strip().lower() == "true"
        return bool(active)
    return False

  def set_question_active(self, *args):
    """Set the 'active' attribute for a question by id. Expects (id, state) where state is bool.
    When setting a question active=True, ensure all other questions on the same level are set to False so
    only one question per level remains active.
    """
    id, state = args[0]
    try:
      with open(self.questions_file, "r", encoding="utf-8") as file:
        data_file = json.load(file)
    except Exception:
      data_file = []

    def _iter_items(items):
      for item in items:
        if isinstance(item, dict):
          yield item
        elif isinstance(item, list):
          for sub in _iter_items(item):
            yield sub

    # find level of the target question
    target_level = None
    for obj in _iter_items(data_file):
      if obj.get("id") == id:
        target_level = obj.get("level")
        break

    updated = False
    if state and target_level is not None:
      # set target active and other questions on same level inactive
      for obj in _iter_items(data_file):
        if obj.get("level") == target_level:
          if obj.get("id") == id:
            if obj.get("active") != "True":
              obj["active"] = "True"
              updated = True
          else:
            if obj.get("active") != "False":
              obj["active"] = "False"
              updated = True
    else:
      # simply set the target inactive
      for obj in _iter_items(data_file):
        if obj.get("id") == id:
          if obj.get("active") != "False":
            obj["active"] = "False"
            updated = True
          break

    if updated:
      try:
        with open(self.questions_file, "w", encoding="utf-8") as file:
          json.dump(data_file, file, indent=4, ensure_ascii=False)
        # reload in-memory data and refresh UI
        try:
          self.load_data()
        except Exception:
          pass
        try:
          self.event_manager.notify("fetch_questions")
        except Exception:
          pass
      except Exception as e:
        print("Error saving questions file:", e)

  def set_up_file_events(self):
    self.event_manager.subscribe("load_data", self.load_data)
    self.event_manager.subscribe("check_selected_question", self.check_selected_question)
    self.event_manager.subscribe("edit_file", self.edit_file)
    self.event_manager.subscribe("set_question_active", self.set_question_active)
    self.event_manager.subscribe("add_file", self.add_file)
    self.event_manager.subscribe("delete", self.delete)
    self.event_manager.subscribe("get_podium", self.get_podium)
    self.event_manager.subscribe("write_podium", self.write_podium)
    self.event_manager.subscribe("set_category", self.set_category)