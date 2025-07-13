from config.settings import *
from os.path import join
from utils.PathHandler import *

class Icon(pygame.sprite.Sprite):
    def __init__(self, position, name):
        super().__init__()
        self.screen = pygame.display.get_surface()

        self.icon = pygame.image.load(resource_path(join("assets", "img", name + '.png'))).convert_alpha()
        self.icon_hover = pygame.image.load(resource_path(join("assets", "img", name + '_hover.png'))).convert_alpha()
        self.image = self.icon
        self.rect = self.image.get_rect(midright=position)

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def on_hover(self):
        self.image = self.icon_hover

    def reset_hover(self):
        self.image = self.icon
