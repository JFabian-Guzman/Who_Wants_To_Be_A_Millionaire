from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *
from utils.TextInput import *
from utils.CheckAnswer import *
from utils.PathHandler import *

class Add(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.inputs = []
        self.option_rects = []
        self.answer_selector = []
        self.new_data = []
        self.level = 0
        self.warning = ''
        self.error = ''
        self.category = ''
        self.title = None

        self.set_up_background()
        self.set_up_text()
        self.set_up_positions()
        self.set_up_inputs()
        self.set_up_answer_selectors()
        self.set_up_buttons()

    def set_up_background(self):
        self.question_background = pygame.image.load(resource_path(join("assets", "img", "question.png"))).convert_alpha()
        self.option_background = pygame.image.load(resource_path(join("assets", "img", "option.png"))).convert_alpha()
        self.title_background = pygame.image.load(resource_path(join("assets", "img", "score.png"))).convert_alpha()

    def set_up_inputs(self):
        self.question_input = TextInput(self.question_rect.center, 875, 60, self.event_manager, 'question')
        self.inputs.append(self.question_input)
        self.interactive_elements.append(self.question_input)

        for position in self.positions:
            self.option_rects.append(self.option_background.get_rect(center=position))
            input = TextInput(position, 350, 60, self.event_manager, 'option')
            self.inputs.append(input)
            self.interactive_elements.append(input)
        for input in self.inputs:
            input.set_up_input_events()

    def set_up_answer_selectors(self):
        for index, rect in enumerate(self.option_rects):
            offset = 230 if index < 2 else -230
            check_position = (rect.center[0] + offset, rect.center[1])
            check_item = Check(check_position, self.elements)
            self.answer_selector.append(check_item)
            self.interactive_elements.append(check_item)

    def set_up_buttons(self):
        self.back_btn = Button(self.elements, self.left_btn_pos, self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.add_btn = Button(self.elements, self.right_btn_pos, self.event_manager, 'btn', 'Save', 'BLACK')
        self.interactive_elements.append(self.back_btn)
        self.interactive_elements.append(self.add_btn)

    def set_up_text(self):
        # Handle multiline title
        title_text = "Add Question\n  Level: " + str(self.level + 1)
        title_lines = title_text.strip().split('\n')
        self.title_lines = []
        line_height = TITLE.get_height()
        start_y = 75 - (len(title_lines) - 1) * line_height // 2
        for i, line in enumerate(title_lines):
          if line.strip():
            rendered_line = TITLE.render(line.strip(), True, COLORS["BLACK"])
            rect = rendered_line.get_rect(center=(self.width//2, start_y + i * (line_height + 2)))
            self.title_lines.append((rendered_line, rect))
        self.warning_text = TEXT.render(self.warning, True, COLORS['AMBER'])
        self.error_text = TEXT.render(self.error, True, COLORS['RED'])

    def set_up_positions(self):
        self.positions = [
            (self.width // 2 - 375, self.height // 2 + 100),
            (self.width // 2 - 375, self.height // 2 + 200),
            (self.width // 2 + 375, self.height // 2 + 100),
            (self.width // 2 + 375, self.height // 2 + 200)
        ]
        self.question_rect = self.question_background.get_rect(center=(self.width//2, self.height//2 - 100))
        self.title_background_rect = self.title_background.get_rect(center=(self.width//2, 75))
        self.left_btn_pos = (self.width // 2 - 350, 75)
        self.right_btn_pos = (self.width // 2 + 350, 75)

    def update_input_position(self):
        for i, position in enumerate(self.positions):
            self.option_rects[i].center = position
        for i, input in enumerate(self.inputs[1::]):
            input.update_position(self.positions[i])

    def update_check_position(self):
        for index, rect in enumerate(self.option_rects):
            offset = 230 if index < 2 else -230
            check_position = (rect.center[0] + offset, rect.center[1])
            self.answer_selector[index].update_position(check_position)

    def draw(self):
        self.elements.draw(self.screen)
        self.screen.blit(self.title_background, self.title_background_rect)
        self.screen.blit(self.question_background, self.question_rect)
        self.draw_title()
        self.draw_warning()
        self.draw_error()
        for i in range(4):
            self.screen.blit(self.option_background, self.option_rects[i])
        for input in self.inputs:
            input.draw()

    def draw_title(self):
        for line_surface, line_rect in self.title_lines:
            self.screen.blit(line_surface, line_rect)

    def draw_warning(self):
        self.warning_text = TEXT.render(self.warning, True, COLORS['AMBER'])
        self.warning_rect = self.warning_text.get_rect(center=(self.question_rect.center[0], self.question_rect.top + 45))
        self.screen.blit(self.warning_text, self.warning_rect)

    def draw_error(self):
        self.error_text = TEXT.render(self.error, True, COLORS['RED'])
        self.error_rect = self.error_text.get_rect(center=(self.question_rect.center[0], self.question_rect.top + 70))
        self.screen.blit(self.error_text, self.error_rect)

    def update(self):
        self.elements.update()
        self.update_cursor_state()
        self.check_click()
        for input in self.inputs:
            input.update()


    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.check_back_click()
                self.check_input_click()
                self.check_option_click()
                self.check_add_click()
                self.click_handled = True
        else:
            self.click_handled = False

    def check_back_click(self):
        if self.back_btn.rect.collidepoint(pygame.mouse.get_pos()):
            self.back_btn.check_notify_state("questions")
            self.clear()

    def check_input_click(self):
        for input in self.inputs:
            if input.rect.collidepoint(pygame.mouse.get_pos()):
                input.toggle_active(True)
            else:
                input.toggle_active(False)

    def check_add_click(self):
        error = False
        answer_selected = False
        if self.add_btn.rect.collidepoint(pygame.mouse.get_pos()):
            self.new_data.clear()
            for input in self.inputs:
                option_text = input.get_input_text()
                if option_text == '':
                    self.show_error('option')
                    error = True
                elif option_text in self.new_data:
                    self.show_error('duplicate')
                    error = True
                else:
                    self.new_data.append(option_text)
            for index, check in enumerate(self.answer_selector):
                if check.get_state():
                    self.new_data.append(self.inputs[index + 1].get_input_text())
                    answer_selected = True
            if not answer_selected:
                self.show_error('answer')
                error = True
            self.new_data.append(self.level)
            self.new_data.append(self.category)
            if not error:
                self.event_manager.notify("add_file", self.new_data)
                self.event_manager.notify("set_state", "questions")
                self.clear()

    def show_error(self, type):
        if type == 'answer':
            self.error = 'Please select an answer before proceeding'
        elif type == 'option':
            self.error = 'Oops! Make sure to fill in all the inputs'
        elif type == 'duplicate':
            self.error = 'Each option should be unique. Please check and try again!'

    def check_option_click(self):
        for check in self.answer_selector:
            if check.rect.collidepoint(pygame.mouse.get_pos()):
                for other_check in self.answer_selector:
                    other_check.change_state(False)
                check.change_state(True)
                break

    def set_level(self, level):
        self.level = level
        # Update the title
        self.set_up_text()

    def clear(self):
        self.warning = ''
        self.error = ''
        for check in self.answer_selector:
            check.change_state(False)
        for input in self.inputs:
            input.set_text('')

    def set_warning(self, *args):
        self.warning = args[0]

    def update_size(self, *args):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        # Recompute title and layout for new size
        self.set_up_text()
        self.set_up_positions()
        self.question_input.update_position(self.question_rect.center)
        self.back_btn.update_position(self.left_btn_pos)
        self.add_btn.update_position(self.right_btn_pos)
        self.update_input_position()
        self.update_check_position()

    def set_category(self, category):
        self.category = category

    def set_up_add_events(self):
        self.event_manager.subscribe("level", self.set_level)
        self.event_manager.subscribe("warning", self.set_warning)
        self.event_manager.subscribe("update_size", self.update_size)
        self.event_manager.subscribe("set_category_title", self.set_category)