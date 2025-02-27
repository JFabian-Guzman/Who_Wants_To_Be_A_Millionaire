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

  def edit_file(self, *args):
        data = args[0]
        print("DATAAA:" + str(data))
        new_data = {
          "question": data[0],
          "options": [data[1], data[2], data[3], data[4]],
          "answer": data[5],
        }
        id = data[6]
        
        print(f"Editing object with ID {id}...")
        
        file_path = join("data", "Questions.json")
        if not isfile(file_path):
            print("Error: File not found.")
            return
        # Load data
        with open(file_path, "r") as file:
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
            with open(file_path, "w") as file:
                json.dump(data_file, file, indent=4)
            print(f"Successfully updated object with ID {id}.")
        else:
            print(f"Error: Object with ID {id} not found.")

  def get_data(self):
    return self.data

  def set_up_file_events(self):
    self.event_manager.subscribe("load_data", self.load_data)
    self.event_manager.subscribe("edit_file", self.edit_file)
