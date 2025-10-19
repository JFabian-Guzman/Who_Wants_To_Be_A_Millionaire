from config.settings import *
from os.path import join
from utils.Option import *
from utils.Logo import *
from .State import *
from utils.Button import *
from utils.CheckAnswer import *


class Categories(State):
    def __init__(self, event_manager, file_manager):
        super().__init__(event_manager)
        self.file_manager = file_manager
        self.categories = []
        self.category_rects = []
        self.answer_selector = []
        self.click_handled = True
        self.is_category_animating = False
        self.set_up_text()
        self.create_categories()
        self.setup_category_position()
        self.set_up_answer_selectors()
        self.set_up_elements()

    def create_categories(self):
        categories = self.file_manager.get_categories()
        for i in range(len(categories)):
            category_instance = Option(categories[i]["category"], (0, 0), self.elements)
            self.categories.append(category_instance)
            self.interactive_elements.append(category_instance)

    def set_up_text(self):
        self.title_background = pygame.image.load(resource_path(join("assets", "img", "score.png"))).convert_alpha()
        self.text = TITLE.render("Categories", True, COLORS["BLACK"])

    def set_up_elements(self):
        self.back_btn = Button(self.elements, self.left_btn_pos , self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.interactive_elements.append(self.back_btn)

    def set_up_answer_selectors(self):
        for index, rect in enumerate(self.category_rects):
            offset = 230 if index % 2 == 0 else -230
            check_position = (rect.center[0] + offset, rect.center[1])
            check_item = Check(check_position, self.elements)
            self.answer_selector.append(check_item)
            self.interactive_elements.append(check_item)

    def setup_category_position(self):
        self.left_btn_pos = (self.width//2 - 350, 75)
        cols = 2
        for i, category in enumerate(self.categories):
            row = i // cols # calculates the row number for the current category
            col = i % cols # even -> left - odd -> righ
            x_position = ((self.width // 2) // 2) + (self.width // 2 * col)
            y_position = self.height // 4 + (self.height // 8 * row)
            category.update_position((x_position, y_position))
            self.category_rects.append(category.rect)
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
                self.btn_click()
                self.check_category_click()
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

    def btn_click(self):
        self.back_btn.check_notify_state("menu")

    def check_category_click(self):
        if self.click_handled:
            return
        mouse_pos = pygame.mouse.get_pos()
        for check in self.answer_selector:
            if check.rect.collidepoint(mouse_pos):
                for other_check in self.answer_selector:
                    other_check.change_state(False)
                check.change_state(True)
                self.click_handled = True
                self.update_category()
                return

    def update_category(self):
        for index, check in enumerate(self.answer_selector):
            if check.get_state():
                self.event_manager.notify("set_category",self.categories[index].get_title())
                return True
        return False

    def set_up_category_events(self):
        self.event_manager.subscribe("update_size", self.update_size)