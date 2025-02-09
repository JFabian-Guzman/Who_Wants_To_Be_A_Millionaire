from config.settings import *
from os.path import join
from .State import *
from utils.Box import *
from utils.Button import *

class Instructions(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)

    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.box = Box(self.elements, event_manager)

    self.font_title = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 22)
    self.font = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 13)
    self.text = self.font_title.render("Instructions", True, COLORS["AMBER"])
    box_rect = self.box.get_rect()
    self.text_rect = self.text.get_rect(center = (box_rect.centerx, box_rect.top + 50))
    self.instructions = self.font.render(INSTRUCTIONS, True, COLORS["WHITE"] )
    self.instructions_rect = self.instructions.get_rect(center = (box_rect.centerx, box_rect.centery - 20))

    self.continue_btn = Button((box_rect.midright[0] - 170, box_rect.midright[1] + 190), event_manager)
    self.back_btn = Button((box_rect.midleft[0] + 170, box_rect.midleft[1] + 190), event_manager, 'negative_btn', 'Go Back', 'WHITE')

    self.display_contiue = True
    self.click_handled = False

    self.interactive_elements.append(self.continue_btn)
    self.interactive_elements.append(self.back_btn)


  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.text, self.text_rect)
    self.screen.blit(self.instructions, self.instructions_rect)
    self.back_btn.draw()
    if self.display_contiue:
      self.continue_btn.draw()

  def update(self):
    self.elements.update()
    self.check_click()
    self.update_cursor_state()

  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        self.continue_btn.check_notify_state("rewards")
        self.back_btn.check_notify_state("menu")
        self.click_handled = True
    else:
        self.click_handled = False

  def display_continue_btn(self, *args):
    self.display_contiue = True 

  def erase_continue_btn(self, *args):
    self.display_contiue = False

  def set_up_instruction_events(self):
    self.event_manager.subscribe("display_continue_btn", self.display_continue_btn)
    self.event_manager.subscribe("erase_continue_btn", self.erase_continue_btn)