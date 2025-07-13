from config.settings import *
from os.path import join
from utils.Coin import *
from utils.PathHandler import *

class Score(pygame.sprite.Sprite):
    def __init__(self, groups, position):
        super().__init__(groups)
        self.screen = pygame.display.get_surface()
        self.elements = pygame.sprite.Group()

        self.image = pygame.image.load(resource_path(join("assets", "img", "score.png"))).convert_alpha()
        self.rect = self.image.get_rect(center=position)

        self.current_level = 1
        self.practice_mode = False
        self.correct_answers = 0
        self.wrong_answers = 0
        self.score = 0

        self.update_rewards()
        self.add_coin()
        self.update_score_board()
        self.add_icons()

    def add_coin(self):
        coin_position = (self.text_rect.right + 40, self.text_rect.centery - 2)
        self.coin = Coin(coin_position, self.elements)

    def add_icons(self):
        check_position = (self.positive_score_rect.right + 20, self.positive_score_rect.centery)
        self.correct_icon = pygame.image.load(resource_path(join("assets", "img", "correct.png"))).convert_alpha()
        self.correct_rect = self.correct_icon.get_rect(midleft=check_position)

        x_position = (self.negative_score_rect.right + 20, self.negative_score_rect.centery)
        self.wrong_icon = pygame.image.load(resource_path(join("assets", "img", "wrong.png"))).convert_alpha()
        self.wrong_rect = self.wrong_icon.get_rect(midleft=x_position)

    def update(self):
        if self.practice_mode:
            self.update_practice_mode()
        else:
            self.update_normal_mode()

    def update_practice_mode(self):
        self.screen.blit(self.positive_score, self.positive_score_rect)
        self.screen.blit(self.negative_score, self.negative_score_rect)
        self.screen.blit(self.correct_icon, self.correct_rect)
        self.screen.blit(self.wrong_icon, self.wrong_rect)
        self.update_score_board()

    def update_normal_mode(self):
        self.screen.blit(self.text, self.text_rect)
        self.elements.draw(self.screen)

    def update_rewards(self):
        self.text = TITLE.render(str(self.score), True, COLORS["BLACK"])
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def update_score_board(self):
        self.positive_score = TITLE.render(str(self.correct_answers), True, COLORS["BLACK"])
        self.positive_score_rect = self.positive_score.get_rect(center=(self.rect.centerx + 100, self.rect.centery))

        self.negative_score = TITLE.render(str(self.wrong_answers), True, COLORS["BLACK"])
        self.negative_score_rect = self.negative_score.get_rect(center=(self.rect.centerx - 100, self.rect.centery))

    def next_level(self):
        self.current_level += 1

    def set_score(self, score):
        self.score = score
        self.update_rewards()

    def set_level(self, level):
        self.current_level = level

    def restart(self):
        self.current_level = 0
        self.correct_answers = 0
        self.wrong_answers = 0

    def get_rect(self):
        return self.rect

    def set_practice_mode(self, state):
        self.practice_mode = state

    def increment_correct_answers(self):
        self.correct_answers += 1

    def increment_wrong_answers(self):
        self.wrong_answers += 1

    def get_title(self):
        return self.title
    
    def update_position(self, position):
        self.rect = self.image.get_rect(center=position)
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.coin.update_position((self.text_rect.right + 40, self.text_rect.centery - 2))
        self.positive_score_rect = self.positive_score.get_rect(center=(self.rect.centerx + 100, self.rect.centery))
        self.negative_score_rect = self.negative_score.get_rect(center=(self.rect.centerx - 100, self.rect.centery))
        check_position = (self.positive_score_rect.right + 20, self.positive_score_rect.centery)
        self.correct_rect = self.correct_icon.get_rect(midleft=check_position)
        x_position = (self.negative_score_rect.right + 20, self.negative_score_rect.centery)
        self.wrong_rect = self.wrong_icon.get_rect(midleft=x_position)
