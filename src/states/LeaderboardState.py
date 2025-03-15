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

    self.set_up_ui()


  def set_up_ui(self):
    self.title_background = pygame.image.load(join("assets", "img", "score.png")).convert_alpha()
    self.title_background_rect = self.title_background.get_rect(center=TITLE_POSITION)
    self.text = TITLE.render("Leaderboard", True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center=TITLE_POSITION)
    self.back_btn = Button(self.elements, BTN_POSITION, self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
    self.podiums = []

    for i in range(5):
      position = (WINDOW_WIDTH//2 , WINDOW_HEIGHT//2 - 175 + (100 * i))
      self.podiums.append(PodiumBox(self.elements,position))

    self.interactive_elements.append(self.back_btn)

  def draw(self):
    self.elements.draw(self.screen)
    self.screen.blit(self.title_background, self.title_background_rect)
    self.screen.blit(self.text, self.text_rect)
    for podium in self.podiums:
      podium.draw()
    
  def set_podiums(self, players):
    sorted_players = sorted(players, key=lambda player: player["Points"], reverse=True)
    for i, podium in enumerate(self.podiums):
      podium.set_data(sorted_players[i]["Name"],str(sorted_players[i]["Points"]),i)

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

  def set_up_leaderboard_events(self):
    self.event_manager.subscribe("set_podiums", self.set_podiums)
