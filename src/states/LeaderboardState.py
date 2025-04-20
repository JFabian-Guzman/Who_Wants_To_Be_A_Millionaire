from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.PodiumBox import *

TITLE_POSITION = (WINDOW_WIDTH // 2, 75)
BTN_POSITION = (WINDOW_WIDTH // 2 - 350, 75)
class Leaderboard(State):
  def __init__(self, event_manager):
    super().__init__(event_manager)


    self.set_up_text()
    self.set_up_positions()
    self.set_up_elements()
    self.update_podium_pos()

  def set_up_elements(self):
    self.back_btn = Button(self.elements, self.left_btn_pos, self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
    self.podiums = []
    self.podium_len = 0
    for i in range(5):
      position = (self.width//2 , self.height//2 - 175 + (100 * i))
      self.podiums.append(PodiumBox(self.elements,position))

    self.interactive_elements.append(self.back_btn)

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.title_background, self.title_background_rect)
    self.screen.blit(self.text, self.text_rect)
    for i in range(self.podium_len):
      self.podiums[i].draw()

  def set_up_text(self):
    self.title_background = pygame.image.load(join("assets", "img", "score.png")).convert_alpha()
    self.text = TITLE.render("Leaderboard", True, COLORS["BLACK"])

  def set_up_positions(self):
    self.left_btn_pos = (self.width // 2 - 350, 75)
    self.title_background_rect = self.title_background.get_rect(center= (self.width // 2, 75))
    self.text_rect = self.text.get_rect(center= (self.width // 2, 75))

  def update_podium_pos(self):
    for i,podium in enumerate(self.podiums):
      podium.update_position((self.width//2 , self.height//2 - 175 + (100 * i)))

  def set_podiums(self, players):
    sorted_players = sorted(players, key=lambda player: player["Points"], reverse=True)
    self.podium_len = len(sorted_players)

    for i, player in enumerate(sorted_players):
      self.podiums[i].set_data(player["Name"],str(player["Points"]),i)

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


  def update_size(self, *args):
    self.screen = pygame.display.get_surface()
    self.width, self.height = self.screen.get_size()
    self.back_btn.update_position(self.left_btn_pos)
    self.set_up_positions()
    self.update_podium_pos()

  def set_up_leaderboard_events(self):
    self.event_manager.subscribe("update_size", self.update_size)
    self.event_manager.subscribe("set_podiums", self.set_podiums)
