from config.settings import *
from os.path import join
from .State import *
from utils.Button import *
from utils.Box import *

from utils.CheckAnswer import *

BTN_POSITION = (WINDOW_WIDTH // 2 - 350, 75)
TITLE_POSITION = (WINDOW_WIDTH / 2, 75)
INPUT_POSITION = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100)
EDIT_BTN_POSITION = (WINDOW_WIDTH // 2 + 350, 75)

class Edit(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.id = ''
        self.inputs = []
        self.option_rects = []
        self.answer_selector = []
        self.warning = ''
        self.error = ''
        self.edit_data = []

        self.setup_text()
        self.setup_ui()
        self.setup_inputs(event_manager)
        self.setup_buttons(event_manager)
        self.setup_answer_selectors()

    def setup_ui(self):
        
        self.question_background = pygame.image.load(join("assets", "img", "question.png")).convert_alpha()
        self.option_background = pygame.image.load(join("assets", "img", "option.png")).convert_alpha()
        self.title_background = pygame.image.load(join("assets", "img", "score.png")).convert_alpha()
        self.question_rect = self.question_background.get_rect(center=(self.width//2, self.height//2 - 100))
        self.title_background_rect = self.title_background.get_rect(center=(self.width//2, 75))
        self.title_rect = self.title.get_rect(center= self.title_background_rect.center)

    def setup_inputs(self, event_manager):
        self.question_input = TextInput(self.question_rect.center, 875, 60, event_manager, 'question')
        self.inputs.append(self.question_input)
        self.positions = [
            (self.width // 2 - 375, self.height // 2 + 100),
            (self.width // 2 - 375, self.height // 2 + 200),
            (self.width // 2 + 375, self.height // 2 + 100),
            (self.width // 2 + 375, self.height // 2 + 200)
        ]
        for position in self.positions:
            self.option_rects.append(self.option_background.get_rect(center=position))
            self.inputs.append(TextInput(position, 350, 60, event_manager, 'option'))
        for input in self.inputs:
            input.set_up_input_events()

    def setup_buttons(self, event_manager):
        self.back_btn = Button(self.elements, (self.width // 2 - 350, 75), event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.edit_btn = Button(self.elements, (self.width // 2 + 350, 75), event_manager, 'btn', 'Save', 'BLACK')
        self.interactive_elements.append(self.back_btn)
        self.interactive_elements.append(self.edit_btn)

    def setup_answer_selectors(self):
        for index, rect in enumerate(self.option_rects):
            offset = 230 if index < 2 else -230
            check_position = (rect.center[0] + offset, rect.center[1])
            check_item = Check(check_position, self.elements)
            self.answer_selector.append(check_item)
            self.interactive_elements.append(check_item)

    def setup_text(self):
        self.title = TITLE.render("Edit Question", True, COLORS["BLACK"])
        self.warning_text = TEXT.render(self.warning, True, COLORS['AMBER'])
        self.error_text = TEXT.render(self.error, True, COLORS['RED'])

    def draw(self):
        self.elements.draw(self.screen)
        self.screen.blit(self.title_background, self.title_background_rect)
        self.screen.blit(self.question_background, self.question_rect)
        self.draw_warning()
        self.draw_error()
        self.screen.blit(self.title, self.title_rect)
        for i in range(4):
            self.screen.blit(self.option_background, self.option_rects[i])
        for input in self.inputs:
            input.draw()

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
                self.check_edit_click()
                self.check_option_click()
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

    def check_edit_click(self):
        error = False
        if self.edit_btn.rect.collidepoint(pygame.mouse.get_pos()):
            self.edit_data.clear()
            for input in self.inputs:
                option_text = input.get_input_text()
                if option_text == '':
                    self.show_error('option')
                    error = True
                elif option_text in self.edit_data:
                    self.show_error('duplicate')
                    error = True
                else:
                    self.edit_data.append(option_text)
            if not self.check_answer_selected():
                self.show_error('answer')
                error = True
            self.edit_data.append(self.id)
            if not error:
                self.event_manager.notify("edit_file", self.edit_data)
                self.event_manager.notify("set_state", "questions")
                self.clear()

    def check_answer_selected(self):
        for index, check in enumerate(self.answer_selector):
            if check.get_state():
                self.edit_data.append(self.inputs[index + 1].get_input_text())
                return True
        return False

    def show_error(self, type):
        if type == 'option':
            self.error = 'Oops! Make sure to fill in all the inputs'
        elif type == 'duplicate':
            self.error = 'Each option should be unique. Please check and try again!'
        elif type == 'answer':
            self.error = 'Please select an answer before proceeding'

    def check_option_click(self):
        for check in self.answer_selector:
            if check.rect.collidepoint(pygame.mouse.get_pos()):
                for other_check in self.answer_selector:
                    other_check.change_state(False)
                check.change_state(True)
                break

    def clear(self):
        self.warning = ''
        self.error = ''
        for check in self.answer_selector:
            check.change_state(False)

    def set_warning(self, *args):
        self.warning = args[0]

    def set_data(self, *args):
        data = args[0]
        self.inputs[0].set_text(data[0])
        options = data[1].split(',')
        for i in range(4):
            option = options[i].strip()
            self.inputs[i + 1].set_text(option)
            if option == data[2]:
                self.answer_selector[i].change_state(True)
        self.id = data[3]

    def update_size(self, *args):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        self.back_btn.update_position((self.width // 2 - 350, 75))
        self.edit_btn.update_position((self.width // 2 + 350, 75))
        self.question_rect = self.question_background.get_rect(center=(self.width//2, self.height//2 - 100))
        self.title_background_rect = self.title_background.get_rect(center=(self.width//2, 75))
        self.title_rect = self.title.get_rect(center= self.title_background_rect.center)
        self.question_input.update_position(self.question_rect.center)
        self.warning_rect = self.warning_text.get_rect(center=(self.question_rect.center[0], self.question_rect.top + 45))
        self.error_rect = self.error_text.get_rect(center=(self.question_rect.center[0], self.question_rect.top + 70))
        self.positions = [
            (self.width // 2 - 375, self.height // 2 + 100),
            (self.width // 2 - 375, self.height // 2 + 200),
            (self.width // 2 + 375, self.height // 2 + 100),
            (self.width // 2 + 375, self.height // 2 + 200)
        ]
        for i, position in enumerate(self.positions):
            self.option_rects[i].center = position
        for i, input in enumerate(self.inputs[1::]):
            input.update_position(self.positions[i - 1])
        for index, rect in enumerate(self.option_rects):
            offset = 230 if index < 2 else -230
            check_position = (rect.center[0] + offset, rect.center[1])
            self.answer_selector[index].update_position(check_position)


    def set_up_edit_events(self):
        self.event_manager.subscribe("set_edit_data", self.set_data)
        self.event_manager.subscribe("warning", self.set_warning)
        self.event_manager.subscribe("update_size", self.update_size)
    