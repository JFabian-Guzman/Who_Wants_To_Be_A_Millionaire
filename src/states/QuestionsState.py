from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.CrudBox import *
from utils.PaginationBox import *
from utils.AddQuestions import *
from utils.DeleteModal import *
from utils.PathHandler import *
from utils.PathHandler import *

class Questions(State):
    def __init__(self, event_manager, file_manager):
        super().__init__(event_manager)
        self.file_manager = file_manager
        self.level = 1
        self.data = self.file_manager.get_data()[self.level]
        self.full_pages = 0
        self.remaining_questions = 0
        self.filtered_data = []
        self.boxes = []
        self.page_number = 0
        self.pagination = []
        self.active_pagination = []
        self.category = ""
        self.set_up_text()
        self.set_up_positions()
        self.set_up_elements()
        self.set_up_pagination()
        self.set_up_question_events()

    def set_up_elements(self):
        self.back_btn = Button(self.elements, self.left_btn_pos, self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.add_box = AddQuestion(self.elements)
        self.delete_modal = DeleteModal(self.event_manager)
        self.interactive_elements.append(self.back_btn)
        self.interactive_elements.append(self.add_box)

    def set_up_pagination(self):
        for i in range(9):
            self.pagination.append(PaginationBox((0,0), str(i + 1)))
        self.update_pagination_pos()

    def update_pagination_pos(self):
        for i, pag in enumerate(self.pagination):
            pag.update_position(((self.width // 2 - 200) + (50 * i), (self.height // 2 + 260)))

    def set_up_text(self):
        self.title_background = pygame.image.load(resource_path(join("assets", "img", "score.png"))).convert_alpha()
        self.title = TITLE.render("Question Manager\n    Level: " + str(self.level + 1), True, COLORS["BLACK"])

    def set_up_positions(self):
        self.left_btn_pos = (self.width//2 - 350, 75)
        self.title_background_rect = self.title_background.get_rect(center=(self.width//2 , 75))
        self.title_rect = self.title.get_rect(center=self.title_background_rect.center)

    def draw(self):
        self.elements.draw(self.screen)
        self.screen.blit(self.title_background, self.title_background_rect)
        self.draw_title()
        for pagination_box in self.active_pagination:
            pagination_box.draw()
        for box in self.boxes:
            box.draw()

    def draw_title(self):
        self.screen.blit(self.title, self.title_rect)

    def update(self):
        self.elements.update()
        if self.delete_modal.is_open():
            self.delete_modal.draw()
            self.delete_modal.update()
        else:
            self.update_cursor_state()
            self.check_click()
            self.check_hover_on_icons()

    def update_interactive_elements(self):
        for pagination_box in self.active_pagination:
            self.interactive_elements.append(pagination_box)

    def fetch_data(self, *args):
        self.clear_data()
        self.set_pagination()
        self.load_page()
        self.set_up_text()

    def clear_data(self):
        self.page_number = 0
        self.interactive_elements.clear()
        # destroy boxes so their interactive sprites (checks/icons) are removed
        for box in list(self.boxes):
            try:
                box.destroy()
            except Exception:
                pass
        self.boxes.clear()
        self.active_pagination.clear()
        self.interactive_elements.append(self.back_btn)
        self.interactive_elements.append(self.add_box)

    def set_pagination(self):
        self.data = self.file_manager.get_data()[self.level]
        self.filtered_data = []
        for question in self.data:
            if question["category"].lower() == self.category.lower():
                self.filtered_data.append(question)
        row_length = len(self.filtered_data)
        self.full_pages = row_length // 3
        self.remaining_questions = row_length % 3
        total_pages = self.full_pages if self.remaining_questions == 0 else self.full_pages + 1

        for i in range(total_pages):
            self.active_pagination.append(self.pagination[i])

        self.update_interactive_elements()

    def load_page(self):
        self.boxes.clear()
        first_question_i = self.page_number * 3
        last_question_i = first_question_i + 3 if self.page_number < self.full_pages else first_question_i + self.remaining_questions
        for i in range(first_question_i, last_question_i):
            question = self.filtered_data[i]["question"]
            options = ", ".join(self.filtered_data[i]["options"])
            answer = self.filtered_data[i]["answer"]
            id = self.filtered_data[i]["id"]
            box = CrudBox(question, options, answer, id, (self.width // 2, (self.height // 2 - 150) + (150 * (i - first_question_i))), self.event_manager, self.elements)
            # Initialize check state from file
            if self.file_manager.is_question_active(id):
                box.get_interactive_elements()[2].change_state(True)
            else:
                box.get_interactive_elements()[2].change_state(False)
            self.boxes.append(box)

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.btn_click()
                self.pagination_click()
                self.edit_click()
                self.add_click()
                self.delete_click()
                self.select_answer_click()
                self.click_handled = True
        else:
            self.click_handled = False

    def btn_click(self):
        if self.back_btn.rect.collidepoint(pygame.mouse.get_pos()):
            for box in list(self.boxes):
                try:
                    box.destroy()
                except Exception:
                    pass
            self.boxes.clear()
            self.back_btn.check_notify_state("levels")


    def pagination_click(self):
        for page in self.active_pagination:
            if page.rect.collidepoint(pygame.mouse.get_pos()):
                self.page_number = page.get_number() - 1
                self.load_page()

    def add_click(self):
        if self.add_box.rect.collidepoint(pygame.mouse.get_pos()):
            self.event_manager.notify("set_state", "add")

    def edit_click(self):
        for box in self.boxes:
            if box.get_interactive_elements()[0].rect.collidepoint(pygame.mouse.get_pos()):
                box.change_to_edit()
                return

    def delete_click(self):
        for box in self.boxes:
            if box.get_interactive_elements()[1].rect.collidepoint(pygame.mouse.get_pos()):
                self.delete_modal.set_id(box.get_id())
                self.delete_modal.show_modal()
                return

    def delete_click(self):
        for box in self.boxes:
            if box.get_interactive_elements()[1].rect.collidepoint(pygame.mouse.get_pos()):
                self.delete_modal.set_id(box.get_id())
                self.delete_modal.show_modal()
                return
            
    def select_answer_click(self):
        for box in self.boxes:
            if box.get_interactive_elements()[2].rect.collidepoint(pygame.mouse.get_pos()):
                check = box.get_interactive_elements()[2]
                if check.get_state() == True:
                    check.change_state(False)
                    self.event_manager.notify("set_questions", [self.level, -1])
                    # Update questions file active flag
                    self.event_manager.notify("set_question_active", [box.get_id(), False])
                else:
                    check.change_state(True)
                    self.event_manager.notify("set_questions", [self.level, box.get_id()])
                    # Update questions file active flag
                    self.event_manager.notify("set_question_active", [box.get_id(), True])
                return

    def set_level(self, level):
        self.level = level

    def update_size(self, *args):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        self.set_up_positions()
        self.back_btn.update_position((self.left_btn_pos))
        self.add_box.update_position()
        self.load_page()
        self.update_pagination_pos()
        self.delete_modal.update_position()

    def check_hover_on_icons(self):
        for box in self.boxes:
            if box.get_interactive_elements()[0].rect.collidepoint(pygame.mouse.get_pos()):
                box.get_interactive_elements()[0].on_hover()
                self.event_manager.notify("change_cursor", 'hover')
                break
            else:
                box.get_interactive_elements()[0].reset_hover()
            
            if  box.get_interactive_elements()[1].rect.collidepoint(pygame.mouse.get_pos()):
                box.get_interactive_elements()[1].on_hover()
                self.event_manager.notify("change_cursor", 'hover')
                break
            else:
                box.get_interactive_elements()[1].reset_hover()
            check = box.get_interactive_elements()[2]
            if  check.rect.collidepoint(pygame.mouse.get_pos()):
                if check.get_state() == True:
                    check.disable()
                else:
                    check.on_hover()
                self.event_manager.notify("change_cursor", 'hover')
                break
            else:
                check.reset_hover()

    def set_category_questions(self, category):
        self.category = category

    def set_up_question_events(self):
        self.event_manager.subscribe("fetch_questions", self.fetch_data)
        self.event_manager.subscribe("level", self.set_level)
        self.event_manager.subscribe("update_size", self.update_size)
        self.event_manager.subscribe("set_category_title", self.set_category_questions)