from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.LevelBox import *

TITLE_POSITION = (WINDOW_WIDTH/2  ,75)
BTN_POSITION = ( WINDOW_WIDTH//2 - 350, 75)

class ManageQuestions(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.setup_ui(event_manager)
    self.setup_levels()


  def setup_ui(self, event_manager):
    self.back_btn = Button(self.elements, BTN_POSITION, event_manager, 'negative_btn', 'Go Back', 'WHITE')
    self.title_background = pygame.image.load(join("assets", "img", "score.png")).convert_alpha()
    self.title_background_rect = self.title_background.get_rect(center=TITLE_POSITION)
    self.title = TITLE.render("Question Manager\n     Levels", True, COLORS["BLACK"])
    self.title_rect = self.title.get_rect(center=TITLE_POSITION)
    self.interactive_elements.append(self.back_btn)

  def setup_levels(self):
    self.levels = []
    for row in range(3):
        for col in range(1, 6):
            position = (175 + (150 * col), WINDOW_HEIGHT // 2 - 150 + (150 * row))
            level = LevelBox(self.elements, position, str(row * 5 + col))
            self.levels.append(level)
            self.interactive_elements.append(level)

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
        self.btn_click()
        self.level_click()
        self.click_handled = True
    else:
        self.click_handled = False
    
  def btn_click(self):
    self.back_btn.check_notify_state("menu")


  def level_click(self):
    for level in self.levels:
      if level.rect.collidepoint(pygame.mouse.get_pos()):
        self.event_manager.notify("level", int(level.get_number()) - 1)
        self.event_manager.notify("set_state", "questions")


