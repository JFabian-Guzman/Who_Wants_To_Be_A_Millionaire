from config.settings import *
from os.path import join
from utils.Coin import *

SCORE_POSITION = (WINDOW_WIDTH/2,310)
class Score(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.screen = pygame.display.get_surface()
    self.elements = pygame.sprite.Group()

    self.image = pygame.image.load(join("assets", "img" ,"score.png")).convert_alpha()
    self.rect = self.image.get_rect(center = SCORE_POSITION)

    self.current_level = 0
    self.practice_mode = False
    self.correct_answers = 0
    self.wrong_answers = 0

    self.update_rewards()
    COIN_POSITION = (self.text_rect.right + 20, self.text_rect.centery - 2)
    Coin(COIN_POSITION, self.elements)
    
    self.update_score_board()
    CHECK_POSITION = (self.positive_score_rect.right + 20, self.positive_score_rect.centery + 25)
    print(CHECK_POSITION)
    self.correct_icon = pygame.image.load(join("assets", "img" ,"correct.png")).convert_alpha()
    self.correct_rect = self.image.get_rect(midleft = CHECK_POSITION)
    X_POSITION = (self.negative_score_rect.right +20, self.negative_score_rect.centery + 25)
    self.wrong_icon = pygame.image.load(join("assets", "img" ,"wrong.png")).convert_alpha()
    self.wrong_rect = self.image.get_rect(midleft = X_POSITION)

  def update(self):
    if self.practice_mode:
      self.screen.blit(self.positive_score, self.positive_score_rect)
      self.screen.blit(self.negative_score, self.negative_score_rect)
      self.screen.blit(self.correct_icon, self.correct_rect)
      self.screen.blit(self.wrong_icon, self.wrong_rect)
    else:
      self.screen.blit(self.text, self.text_rect)
      self.elements.draw(self.screen)
      self.update_rewards()


  def update_rewards(self):
    self.text = TITLE.render(REWARDS[self.current_level], True, COLORS["BLACK"])
    self.text_rect = self.text.get_rect(center = self.rect.center)

  def update_score_board(self):
    self.positive_score = TITLE.render(str(self.correct_answers), True, COLORS["BLACK"])
    self.positive_score_rect = self.text.get_rect(center = (self.rect.centerx + 100, self.rect.centery))
    self.negative_score = TITLE.render(str(self.wrong_answers), True, COLORS["BLACK"])
    self.negative_score_rect = self.text.get_rect(center = (self.rect.centerx - 100, self.rect.centery))

  def next_level(self):
    self.current_level += 1

  def restart(self):
    self.current_level = 0

  def get_rect(self):
    return self.rect
  
  def set_practice_mode(self,state):
    self.practice_mode = state

  def set_correct_answers(self, value):
    self.correct_answers = value

  def set_wrong_answers(self, value):
    self.wrong_answers = value

  def get_title(self):
    return self.title
