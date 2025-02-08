from config.settings import *
from os.path import join
from .State import *
from utils.Box import *
from utils.Button import *

class Credits(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.box = Box(self.elements, event_manager)
    self.font_title = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 20)
    self.font_subtitle = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 16)
    self.font_text = pygame.font.Font(join("assets", "fonts", "PressStart2P-Regular.ttf"), 14)
    box_rect = self.box.get_rect()
    self.title = self.font_title.render("Credits", True, COLORS["AMBER"])
    self.title_rect = self.title.get_rect(center = (box_rect.centerx, box_rect.top + 75))
    self.sub_title_1 = self.font_subtitle.render("Developer", True, COLORS["AMBER"])
    self.sub_title_1_rect = self.sub_title_1.get_rect(center = (box_rect.centerx, box_rect.top + 125))
    self.sub_title_2 = self.font_subtitle.render("Contributors", True, COLORS["AMBER"])
    self.sub_title_2_rect = self.sub_title_2.get_rect(center = (box_rect.centerx, box_rect.top + 225))
    self.developer = self.font_text.render(DEVELOPER, True, COLORS["WHITE"])
    self.developer_rect = self.developer.get_rect(center = (box_rect.centerx, box_rect.top + 175))
    self.contributors = self.font_text.render(CONTRIBUTORS, True, COLORS["WHITE"])
    self.contributors_rect = self.contributors.get_rect(center = (box_rect.centerx, box_rect.top + 300))
    
    self.back_btn = Button((box_rect.midleft[0] + 170, box_rect.midleft[1] + 190), event_manager, 'negative_btn', 'Go Back', 'WHITE')

    self.interactive_elements.append(self.back_btn)

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.title, self.title_rect)
    self.screen.blit(self.sub_title_1, self.sub_title_1_rect)
    self.screen.blit(self.sub_title_2, self.sub_title_2_rect)
    self.screen.blit(self.developer, self.developer_rect)
    self.screen.blit(self.contributors, self.contributors_rect)
    self.back_btn.draw()

  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.check_click()

  def check_click(self):
      if pygame.mouse.get_pressed()[0]: 
        if not self.click_handled:
          self.back_btn.check_notify_state("menu")
          self.click_handled = True
      else:
          self.click_handled = False
