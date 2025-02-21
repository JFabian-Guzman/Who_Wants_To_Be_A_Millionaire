from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.NumberBox import *

TITLE_POSITION = (WINDOW_WIDTH/2  ,75)
BTN_POSITION = ( WINDOW_WIDTH//2 - 350, 75)

class ManageQuestions(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)

    self.back_btn = Button(self.elements,BTN_POSITION, event_manager, 'negative_btn', 'Go Back', 'WHITE')
    self.boxs = []
    self.title_background = pygame.image.load(join("assets", "img" ,"score.png")).convert_alpha()
    self.title_background_rect = self.title_background.get_rect(center = TITLE_POSITION)
    self.title = TITLE.render("Question Manager", True, COLORS["BLACK"])
    self.title_rect = self.title.get_rect(center= TITLE_POSITION)


    for row in range(3):
      for col in range(6):
        position = (250 + (150 * col), WINDOW_HEIGHT // 2 - 150 + (150 * row))
        box = NumberBox(self.elements, position, str(row * 6 + col))
        self.boxs.append(box)
        self.interactive_elements.append(box)

    self.interactive_elements.append(self.back_btn)

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.title_background, self.title_background_rect)
    self.screen.blit(self.title, self.title_rect)

  def update(self):
    self.update_cursor_state()
    self.check_click()
    self.elements.update()

  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        self.back_btn.check_notify_state("menu")
        self.click_handled = True
    else:
        self.click_handled = False
    


