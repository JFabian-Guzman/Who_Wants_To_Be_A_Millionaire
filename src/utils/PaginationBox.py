from config.settings import *
from os.path import join

class PaginationBox(pygame.sprite.Sprite):
    def __init__(self, position, number):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.image = pygame.image.load(join("assets", "img", 'pagination_box.png')).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        
        self.text = TEXT.render(number, True, COLORS["WHITE"])
        self.text_rect = self.text.get_rect(center = self.rect.center)

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text, self.text_rect)


