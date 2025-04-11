from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.LevelBox import *

BTN_POSITION = ( WINDOW_WIDTH//2 - 350, 75)

class ManageQuestions(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.setup_ui(event_manager)
    self.setup_levels()


  def setup_ui(self, event_manager):
    self.back_btn = Button(self.elements, ( self.width//2 - 350, 75), event_manager, 'negative_btn', 'Go Back', 'WHITE')
    self.title_background = pygame.image.load(join("assets", "img", "score.png")).convert_alpha()
    self.title_background_rect = self.title_background.get_rect(center=(self.width//2, 75))
    self.title = TITLE.render("Question Manager\n     Levels", True, COLORS["BLACK"])
    self.title_rect = self.title.get_rect(center=self.title_background_rect.center)
    self.interactive_elements.append(self.back_btn)

  def setup_levels(self):
    self.levels = []
    for row in range(3):
      for col in range(1, 6):
        total_grid_width = (5 - 1) * 150  # gaps width
        
        # Calculate starting X to center the grid
        start_x = (self.width - total_grid_width) // 2

        # Calculate starting Y to center the grid vertically
        total_grid_height = (3 - 1) * 150  # gaps height
        start_y = (self.height - total_grid_height) // 2
        
        # Calculate position for each box
        position = (start_x + (col - 1) * 150, start_y + row * 150)
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

  def update_size(self, *args):
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.title_background_rect = self.title_background.get_rect(center=(self.width//2, 75))
    self.title_rect = self.title.get_rect(center=self.title_background_rect.center)
    self.back_btn.update_position(( self.width//2 - 350, 75))

    # Calculate grid dimensions
    cols = 5
    rows = 3
    spacing = 150  # Space between boxes
    # Total width/height occupied by the grid
    total_grid_width = (cols - 1) * spacing
    total_grid_height = (rows - 1) * spacing
    # Starting position to center the grid
    start_x = (self.width - total_grid_width) // 2
    start_y = (self.height - total_grid_height) // 2
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            if index < len(self.levels):  
                position = (
                    start_x + col * spacing,
                    start_y + row * spacing
                )
                self.levels[index].update_position(position)

  def level_click(self):
    for level in self.levels:
      if level.rect.collidepoint(pygame.mouse.get_pos()):
        self.event_manager.notify("level", int(level.get_number()) - 1)
        self.event_manager.notify("set_state", "questions")

  def set_up_manage_events(self):
    self.event_manager.subscribe("update_size", self.update_size)
