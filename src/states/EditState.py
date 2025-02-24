from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *

BTN_POSITION = ( WINDOW_WIDTH//2 - 350, 75)
TITLE_POSITION = (WINDOW_WIDTH/2  ,75)

class Edit(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.box = Box(self.elements)

    self.question = ''
    self.options = []
    self.answer = ''

    self.back_btn = Button(self.elements,BTN_POSITION, event_manager, 'negative_btn', 'Go Back', 'WHITE')

    self.title_background = pygame.image.load(join("assets", "img" ,"score.png")).convert_alpha()
    self.title_background_rect = self.title_background.get_rect(center = TITLE_POSITION)
    self.title = TITLE.render("Edit Question", True, COLORS["BLACK"])
    self.title_rect = self.title.get_rect(center= TITLE_POSITION)
    

    self.interactive_elements.append(self.back_btn)

    self.update_text()

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.question_text, self.question_rect)
    self.screen.blit(self.title_background, self.title_background_rect)
    self.screen.blit(self.title, self.title_rect)
    self.update_cursor_state()
    self.check_click()
    
  def update_text(self):
    self.question_text = TITLE.render(self.question, True, COLORS["WHITE"])
    self.question_rect = self.question_text.get_rect(center=(WINDOW_WIDTH/2  ,WINDOW_HEIGHT/2))

  def update(self):
    self.elements.update()

  def set_data(self, *args):
    data = args[0]
    print(data)
    self.question = data[0]
    self.options = data[1]
    self.answer = data[2]
    self.update_text()

  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        self.back_btn.check_notify_state("questions")
        self.click_handled = True
    else:
        self.click_handled = False


  def set_up_edit_events(self):
    self.event_manager.subscribe("set_edit_data", self.set_data)