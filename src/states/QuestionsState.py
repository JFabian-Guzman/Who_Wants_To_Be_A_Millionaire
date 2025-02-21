from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.CrudBox import *
from utils.PaginationBox import *

TITLE_POSITION = (WINDOW_WIDTH/2  ,75)
BTN_POSITION = ( WINDOW_WIDTH//2 - 350, 75)

class Questions(State):
  def __init__(self, event_manager, file_manager):
    super().__init__(event_manager)
    
    self.back_btn = Button(self.elements,BTN_POSITION, event_manager, 'negative_btn', 'Go Back', 'WHITE')
    self.title_background = pygame.image.load(join("assets", "img" ,"score.png")).convert_alpha()
    self.title_background_rect = self.title_background.get_rect(center = TITLE_POSITION)
    self.title = TITLE.render("Question Manager", True, COLORS["BLACK"])
    self.title_rect = self.title.get_rect(center= TITLE_POSITION)
    self.file_manager = file_manager
    self.level = 1
    self.boxes = []
    self.pagination_number = 0
    self.pagination = []
    self.active_pagination = []
    for i in range(9):
      self.pagination.append(PaginationBox(((WINDOW_WIDTH / 2 - 200) + (50 * i), (WINDOW_HEIGHT / 2 + 260)), str(i + 1))) 
      # self.interactive_elements.append(self.pagination[i])

    self.interactive_elements.append(self.back_btn)

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.title_background, self.title_background_rect)
    self.screen.blit(self.title, self.title_rect)
    for pagination_box in self.active_pagination:
      pagination_box.draw()
    for box in self.boxes:
      box.draw()
    
    
  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.check_click()
    self.check_hover_on_icons()

  def fetch_data(self, *args):
    self.boxes.clear()
    data = self.file_manager.get_data()[self.level]
    row_length = len(data)
    print("ROW LENGTH: " + str(row_length))
    first_question_i = self.pagination_number * 3
    full_pages = row_length // 3
    remaining_questions = row_length % 3
    last_question_i = first_question_i + 3 if self.pagination_number < full_pages else first_question_i + remaining_questions
    total_pages = full_pages if remaining_questions == 0 else full_pages + 1
    for i in range(total_pages):
      self.active_pagination.append(self.pagination[i])
      self.interactive_elements.append(self.pagination[i])

    for i in range(first_question_i, last_question_i):
        question = data[i]["question"]
        options = ", ".join(data[i]["options"])
        id = data[i]["id"]
        self.boxes.append(CrudBox(question, options, id, (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2 - 150) + (150 * (i - first_question_i))), self.event_manager))

  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        self.back_btn.check_notify_state("manage questions")
        self.click_handled = True
    else:
        self.click_handled = False

  def set_level(self, level):
    self.level = level

  def set_up_read_events(self):
    self.event_manager.subscribe("fetch_questions", self.fetch_data)
    self.event_manager.subscribe("question_level", self.set_level)

  def check_hover_on_icons(self):
    for box in self.boxes:
      if box.get_interactive_elements()[0].rect.collidepoint(pygame.mouse.get_pos()) or box.get_interactive_elements()[1].rect.collidepoint(pygame.mouse.get_pos()):
        self.event_manager.notify("change_cursor", 'hover')
        break
