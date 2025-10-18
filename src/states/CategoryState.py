from config.settings import *
from os.path import join
from utils.Option import *
from utils.Logo import *
from .State import *

class Categories(State):
    def __init__(self, event_manager, file_manager):
        super().__init__(event_manager)
        self.file_manager = file_manager
        self.categories = []
        self.click_handled = True
        self.is_category_animating = False
        self.set_up_text()
        self.create_categories()
        self.setup_category_position()

    def create_categories(self):
        categories = self.file_manager.get_categories()
        for i in range(len(categories)):
            category_instance = Option(categories[i]["category"], (0, 0), self.elements)
            self.categories.append(category_instance)
            self.interactive_elements.append(category_instance)

    def set_up_text(self):
        self.title_background = pygame.image.load(resource_path(join("assets", "img", "score.png"))).convert_alpha()
        self.text = TITLE.render("Categories", True, COLORS["BLACK"])

    def setup_category_position(self):
        cols = 2
        for i, option in enumerate(self.categories):
            row = i // cols # calculates the row number for the current option
            col = i % cols # even -> left - odd -> righ
            x_position = ((self.width // 2) // 2) + (self.width // 2 * col)
            y_position = self.height // 4 + (self.height // 8 * row)
            option.update_position((x_position, y_position))
        self.title_background_rect = self.title_background.get_rect(center= (self.width // 2, 75))
        self.text_rect = self.text.get_rect(center= (self.width // 2, 75))

    def draw(self):
        self.elements.draw(self.screen)
        self.screen.blit(self.title_background, self.title_background_rect)
        self.screen.blit(self.text, self.text_rect)

    def update(self):
        self.elements.update()
        self.update_cursor_state()
        self.update_user_click()

    def update_user_click(self):
        if pygame.mouse.get_pressed()[0] :
            if (not self.click_handled and not self.is_category_animating):
                self.handle_category_click()
        else:
            self.click_handled = False

    def handle_category_click(self):
        mouse_pos = pygame.mouse.get_pos()
        for category in self.categories:
            if category.get_rect().collidepoint(mouse_pos):
                self.is_category_animating = True
                category.start_animation(callback=lambda: self.change_state(category), menu= True)
                self.click_handled = True    
                return

    def change_state(self, category):
        self.event_manager.notify("set_state", "levels")
        self.is_category_animating = False

    def update_size(self, *args):
        self.width, self.height  = self.screen.get_size()
        self.setup_category_position()


    def set_up_category_events(self):
        self.event_manager.subscribe("update_size", self.update_size)