from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.CrudBox import *
from utils.PaginationBox import *
from utils.AddQuestions import *

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
    self.add_box = AddQuestion(self.elements)
    

    self.file_manager = file_manager
    self.level = 1
    self.data = self.file_manager.get_data()[self.level]
    self.full_pages = 0
    self.remaining_questions = 0
    self.boxes = []
    self.page_number = 0
    self.pagination = []
    self.active_pagination = []
    for i in range(9):
      self.pagination.append(PaginationBox(((WINDOW_WIDTH / 2 - 200) + (50 * i), (WINDOW_HEIGHT / 2 + 260)), str(i + 1))) 

    
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
    self.clear_data()
    self.set_pagination()
    self.load_page()

  def clear_data(self):
    self.page_number = 0
    self.interactive_elements.clear()
    self.boxes.clear()
    self.active_pagination.clear()

  def set_pagination(self):
    self.data = self.file_manager.get_data()[self.level]
    row_length = len(self.data)
    self.full_pages = row_length // 3
    self.remaining_questions = row_length % 3
    total_pages = self.full_pages if self.remaining_questions == 0 else self.full_pages + 1

    for i in range(total_pages):
      self.active_pagination.append(self.pagination[i])
      
    self.update_interactive_elements()

  def load_page(self):
    self.boxes.clear()
    first_question_i = self.page_number * 3
    last_question_i = first_question_i + 3 if self.page_number < self.full_pages else first_question_i + self.remaining_questions
    for i in range(first_question_i, last_question_i):
        question = self.data[i]["question"]
        options = ", ".join(self.data[i]["options"])
        answer = self.data[i]["answer"]
        id = self.data[i]["id"]
        self.boxes.append(CrudBox(question, options, answer,id, (WINDOW_WIDTH / 2, (WINDOW_HEIGHT / 2 - 150) + (150 * (i - first_question_i))), self.event_manager))

  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        self.btn_click()
        self.pagination_click()
        self.edit_click()
        self.add_click()
        self.click_handled = True
    else:
        self.click_handled = False

  def btn_click(self):
    self.back_btn.check_notify_state("manage questions")

  def pagination_click(self):
    for page in self.active_pagination:
      if page.rect.collidepoint(pygame.mouse.get_pos()):
        self.page_number = page.get_number() - 1
        self.load_page()

  def add_click(self):
    if self.add_box.rect.collidepoint(pygame.mouse.get_pos()):
      self.event_manager.notify("set_state", "add")

  def set_level(self, level):
    self.level = level

  def set_up_question_events(self):
    self.event_manager.subscribe("fetch_questions", self.fetch_data)
    self.event_manager.subscribe("level", self.set_level)

  def check_hover_on_icons(self):
    for box in self.boxes:
      if box.get_interactive_elements()[0].rect.collidepoint(pygame.mouse.get_pos()) or box.get_interactive_elements()[1].rect.collidepoint(pygame.mouse.get_pos()):
        self.event_manager.notify("change_cursor", 'hover')
        break

  def edit_click(self):
    for box in self.boxes:
        if box.get_interactive_elements()[0].rect.collidepoint(pygame.mouse.get_pos()):
            box.change_to_edit()
            return

  def update_interactive_elements(self):
    self.interactive_elements.append(self.back_btn)
    self.interactive_elements.append(self.add_box)
    for pagination_box in self.active_pagination:
      self.interactive_elements.append(pagination_box)
