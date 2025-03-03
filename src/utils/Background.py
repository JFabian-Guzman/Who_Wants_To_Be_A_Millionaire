from config.settings import *
from os.path import join

class Background:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.load_background_image()
        self.create_overlay()
        self.create_banner()

    def load_background_image(self):
        background_img = pygame.image.load(join("assets", "img", "background.jpeg")).convert()
        self.background = pygame.transform.scale(background_img, self.screen.get_size())

    def create_overlay(self):
        self.overlay = pygame.Surface(self.screen.get_size())
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(128)  # Transparency level

    def create_banner(self):
        self.banner = pygame.Surface(BANNER["SIZE"])
        self.banner_rect = self.banner.get_rect(bottom=WINDOW_HEIGHT)

    def draw_banner(self):
        self.banner.fill(COLORS["WHITE"])
        self.draw_logos()
        self.screen.blit(self.banner, self.banner_rect)

    def draw_logos(self):
        ucr_logo, ucr_rect = self.load_logo("ucr_logo.png", (300, 60), left=0, centery=BANNER["SIZE"][1] // 2)
        elm_logo, elm_rect = self.load_logo("elm_logo.png", (300, 50), center=(WINDOW_WIDTH // 2, BANNER["SIZE"][1] // 2))
        tcu_logo, tcu_rect = self.load_logo("tcu_logo.png", (30, 60), center=(WINDOW_WIDTH - 100, BANNER["SIZE"][1] // 2))

        self.banner.blit(ucr_logo, ucr_rect)
        self.banner.blit(elm_logo, elm_rect)
        self.banner.blit(tcu_logo, tcu_rect)

    def load_logo(self, filename, size, **kwargs):
        logo = pygame.image.load(join("assets", "img", filename)).convert_alpha()
        logo = pygame.transform.scale(logo, size)
        rect = logo.get_rect(**kwargs)
        return logo, rect

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.overlay, (0, 0))
        self.draw_banner()