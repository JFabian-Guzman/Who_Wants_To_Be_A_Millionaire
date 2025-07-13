from config.settings import *
from os.path import join
from utils.Button import *
from utils.PathHandler import *

class PodiumBox(pygame.sprite.Sprite):
  def __init__(self, groups, position):
    super().__init__(groups)
    self.screen = pygame.display.get_surface()
    self.image = pygame.image.load(resource_path(join("assets", "img" ,"leaderboard_box.png"))).convert_alpha()
    self.rect = self.image.get_rect(center=position)
    self.podium = ["gold", "silver", "bronze", "fourth_place", "fifth_place"]
    self.player_name = ''
    self.player_points = ''
    self.medal = 0
    self.update_data()

  def draw(self):
    self.screen.blit(self.final_medal, self.medal_rect)
    self.screen.blit(self.player, self.player_rect)
    self.screen.blit(self.points, self.points_rect)

  def update_data(self):
    self.final_medal = pygame.image.load(resource_path(join("assets", "img" , self.podium[self.medal] + ".png"))).convert_alpha()
    self.medal_rect = self.final_medal.get_rect(midleft=(self.rect.midleft[0] + 10,self.rect.midleft[1]))
    self.player = TEXT.render(self.player_name, True, COLORS["WHITE"])
    self.player_rect = self.player.get_rect(center=self.rect.center)
    self.points = TEXT.render(self.player_points, True, COLORS["WHITE"])
    self.points_rect = self.points.get_rect(midright=(self.rect.midright[0] - 10 ,self.rect.midright[1] ))

  def set_data(self, name, points, positon):
    self.player_name = name
    self.player_points = points
    self.medal = positon
    self.update_data()

  def update_position(self, position):
    self.rect = self.image.get_rect(center=position)
    self.medal_rect = self.final_medal.get_rect(midleft=(self.rect.midleft[0] + 10,self.rect.midleft[1]))
    self.player_rect = self.player.get_rect(center=self.rect.center)
    self.points_rect = self.points.get_rect(midright=(self.rect.midright[0] - 10 ,self.rect.midright[1] ))
