from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *
from utils.TextInput import *

BTN_POSITION = ( WINDOW_WIDTH//2 - 350, 75)
TITLE_POSITION = (WINDOW_WIDTH/2  ,75)
INPUT_POSITION = (WINDOW_WIDTH/2   ,WINDOW_HEIGHT/2+ 100)

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

    self.inputs = []
    for i in range(6):
      position = (self.box.rect.left + 100, self.box.rect.top + 75 + i * 70)
      self.inputs.append(TextInput(position, 400, 30, event_manager))
      self.inputs[i].set_up_input_events()


    self.interactive_elements.append(self.back_btn)

    self.subtitles = [
      TEXT.render("Question", True, COLORS["AMBER"]),
      TEXT.render("Option A", True, COLORS["AMBER"]),
      TEXT.render("Option B", True, COLORS["AMBER"]),
      TEXT.render("Option C", True, COLORS["AMBER"]),
      TEXT.render("Option D", True, COLORS["AMBER"]),
      TEXT.render("Answer", True, COLORS["AMBER"])
    ]

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.title_background, self.title_background_rect)
    self.screen.blit(self.title, self.title_rect)
    for index, subtitle in enumerate(self.subtitles):
      self.screen.blit(subtitle, (self.box.rect.left + 100, self.box.rect.top + 50 + index * 70))

    for input in self.inputs:
      input.draw(self.screen)
    self.update_cursor_state()
    self.check_click()
    

  def update(self):
    self.elements.update()

  def set_data(self, *args):
    data = args[0]
    self.question = data[0]
    self.options = data[1]
    self.answer = data[2]

  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        self.back_btn.check_notify_state("questions")
        self.check_input_click()
        self.click_handled = True
    else:
        self.click_handled = False

  def check_input_click(self):
    for input in self.inputs:
      if input.rect.collidepoint(pygame.mouse.get_pos()):
        input.toggle_active(True)
      else:
        input.toggle_active(False)


  def set_up_edit_events(self):
    self.event_manager.subscribe("set_edit_data", self.set_data)