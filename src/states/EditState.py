from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *
from utils.TextInput import *
from utils.CheckAnswer import *

BTN_POSITION = ( WINDOW_WIDTH//2 - 350, 75)
TITLE_POSITION = (WINDOW_WIDTH/2  , 75)
INPUT_POSITION = (WINDOW_WIDTH/2   ,WINDOW_HEIGHT/2+ 100)
EDIT_BTN_POSITION = ( WINDOW_WIDTH//2 + 350, 75)

class Edit(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)

    self.id = ''
    self.inputs = []
    self.option_rects = []
    self.answer_selector = []
    self.title = TITLE.render("Edit Question", True, COLORS["BLACK"])
    self.warning = ''


    self.quesiton_background = pygame.image.load(join("assets", "img" ,"question.png")).convert_alpha()
    self.option_background = pygame.image.load(join("assets", "img" ,"option.png")).convert_alpha()
    self.title_background = pygame.image.load(join("assets", "img" ,"score.png")).convert_alpha()



    self.title_rect = self.title.get_rect(center= TITLE_POSITION)
    self.question_rect = self.quesiton_background.get_rect(center = (WINDOW_WIDTH/2,250))
    self.title_background_rect = self.title_background.get_rect(center = TITLE_POSITION)

    self.inputs.append(TextInput(self.question_rect.center, 875, 60, event_manager, 'question'))


    for index, position in enumerate(OPTION_POSITIONS):
      self.option_rects.append(self.option_background.get_rect(center=position))
      self.inputs.append(TextInput(position, 350, 60, event_manager, 'option'))
      

    for index, rect in enumerate(self.option_rects):
      offset = 230 if index < 2 else -230
      check_position = (rect.center[0] + offset, rect.center[1])
      check_item = Check(check_position, self.elements)
      self.answer_selector.append(check_item)
      self.interactive_elements.append(check_item)

    
    self.back_btn = Button(self.elements,BTN_POSITION, event_manager, 'negative_btn', 'Go Back', 'WHITE')
    self.edit_btn = Button(self.elements,EDIT_BTN_POSITION, event_manager, 'btn', 'Save', 'BLACK')



    for i in range(5):
      self.inputs[i].set_up_input_events()

    self.edit_data = []

    self.interactive_elements.append(self.back_btn)
    self.interactive_elements.append(self.edit_btn)


  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.title_background, self.title_background_rect)
    self.screen.blit(self.quesiton_background, self.question_rect)
    self.draw_text()
  
    self.screen.blit(self.title, self.title_rect)
    for i in range(4):
      self.screen.blit(self.option_background, self.option_rects[i])

    for input in self.inputs:
      input.draw()
    
  def draw_text(self):
    warning_text = TEXT.render(self.warning, True, COLORS['AMBER'])
    warning_rect = warning_text.get_rect(center = (WINDOW_WIDTH/2,175))
    self.screen.blit(warning_text, warning_rect)

  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.check_click()

  def set_data(self, *args):
    data = args[0]
    # Question text
    self.inputs[0].set_text(data[0])
    # Options text
    options = data[1].split(',')
    for i in range(0,4):
      option = options[i].strip()
      self.inputs[i + 1].set_text(option)
      if option == data[2]: #answer
        print("SET TO TRUE")
        self.answer_selector[i].change_state(True)
    # ID
    self.id = data[3]


  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        self.check_back_click()
        self.check_input_click()
        self.check_edit_click()
        self.check_option_click()
        self.click_handled = True
    else:
        self.click_handled = False

  def check_back_click(self):
    if self.back_btn.rect.collidepoint(pygame.mouse.get_pos()):
      self.back_btn.check_notify_state("questions")
      self.clear()

  def check_input_click(self):
    for input in self.inputs:
      if input.rect.collidepoint(pygame.mouse.get_pos()):
        input.toggle_active(True)
      else:
        input.toggle_active(False)

  def check_edit_click(self):
    if self.edit_btn.rect.collidepoint(pygame.mouse.get_pos()):
      # Remove the prev data to append the new one
      self.edit_data.clear()
      for input in self.inputs:
        self.edit_data.append(input.get_input_text())
      # Search the option with active check(answer)  
      for index, check in enumerate(self.answer_selector):
        print("state: " + str(check.get_state()))
        if check.get_state():
          self.edit_data.append(self.inputs[index + 1].get_input_text())
      self.edit_data.append(self.id)
      
      self.event_manager.notify("edit_file", self.edit_data)
      self.event_manager.notify("set_state", "questions")
    
  def check_option_click(self):
    for check in self.answer_selector:
      if check.rect.collidepoint(pygame.mouse.get_pos()):
        for other_check in self.answer_selector:
          other_check.change_state(False)
        # Set the clicked option to True
        check.change_state(True)
        break

  def clear(self):
    self.warning = ''
    for check in self.answer_selector:
      check.change_state(False)
  
  def set_warning(self, *args):
    self.warning = args[0]

  def set_up_edit_events(self):
    self.event_manager.subscribe("set_edit_data", self.set_data)
    self.event_manager.subscribe("warning", self.set_warning)

