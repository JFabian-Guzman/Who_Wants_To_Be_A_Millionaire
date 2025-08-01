from config.settings import *
from os.path import join
from utils.PathHandler import *

class ErrorMessage(pygame.sprite.Sprite):
    def __init__(self, position, name):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load(resource_path(join("assets", "img", name + '.png'))).convert_alpha()
        self.rect = self.image.get_rect(midright=position)

    def draw(self):
        self.screen.blit(self.image, self.rect)


