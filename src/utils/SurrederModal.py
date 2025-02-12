from config.settings import *
from os.path import join
from utils.Button import *

TEXT_POSITION = (WINDOW_WIDTH//2  ,WINDOW_HEIGHT//2 - 30)

class SurrenderModal(pygame.sprite.Sprite):
  def __init__(self , event_manager):
    super().__init__()
    self.elements = pygame.sprite.Group()
    self.screen = pygame.display.get_surface()
    self.interactive_elements = []
    self.event_manager = event_manager
    self.click_handled = True

    self.image = pygame.image.load(join("assets", "img" ,"question.png")).convert_alpha()
    self.rect = self.image.get_rect(center = MODAL_POSITION)

    self.surrender_message = "You will keep your winnings.\n\nAre you sure you want to surrender?"
    self.text = TEXT.render(self.surrender_message, True, COLORS["WHITE"])
    self.text_rect = self.text.get_rect(center=TEXT_POSITION)

    self.overlay = pygame.Surface(self.screen.get_size())
    self.overlay.fill((0, 0, 0))
    self.overlay.set_alpha(128)


    self.no_btn = Button(self.elements,MODAL_BTN_LEFT_POSITION, event_manager, 'negative_btn', 'No', 'WHITE')
    self.yes_btn = Button(self.elements,MODAL_BTN_RIGHT_POSITION, event_manager, 'btn', 'Yes')

    self.interactive_elements.append(self.no_btn)
    self.interactive_elements.append(self.yes_btn)

  def draw(self):
    self.screen.blit(self.overlay, (0, 0))
    self.screen.blit(self.image, self.rect)
    self.screen.blit(self.text, self.text_rect)
    self.elements.draw(self.screen)

  def update(self):
    self.elements.update()
    self.update_cursor_state()
    self.check_click()


  def check_click(self):
    if pygame.mouse.get_pressed()[0]: 
      if not self.click_handled:
        if self.yes_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
          self.event_manager.notify("display_win_screen")
        self.event_manager.notify("display_surrender_modal")
        self.click_handled = True
    else:
        self.click_handled = False

  def update_cursor_state(self):
    for element in self.interactive_elements:
      if element.rect.collidepoint(pygame.mouse.get_pos()):
        self.event_manager.notify("change_cursor", 'hover')
        break
      else:
        self.event_manager.notify("change_cursor", 'default')