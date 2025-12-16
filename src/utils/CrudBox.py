from config.settings import *
from os.path import join
from utils.Icon import *
from utils.PathHandler import *
from utils.CheckAnswer import *

class CrudBox(pygame.sprite.Sprite):
    def __init__(self, question, options, answer, id, position, event_manager, elements):
        super().__init__()

        self.screen = pygame.display.get_surface()
        self.interactive_elements = []
        self.event_manager = event_manager
        self.elements = elements

        self.image = pygame.image.load(resource_path(join("assets", "img", "crud_box.png"))).convert_alpha()
        self.rect = self.image.get_rect(center=position)

        self.pencil_icon = Icon((self.rect.midright[0] - 80, self.rect.midright[1] + 45), "pencil")
        self.trash_icon = Icon((self.rect.midright[0] - 25, self.rect.midright[1] + 45), "trash")
        check_position = (self.rect.right + 50, self.rect.centery)
        self.check = Check(check_position, self.elements)
        self.id = id
        self.data = [question, options, answer, id]

        self.interactive_elements.append(self.pencil_icon)
        self.interactive_elements.append(self.trash_icon)
        self.interactive_elements.append(self.check)

        self.setup_text_elements(question, options, answer)

    def setup_text_elements(self, question, options, answer):
        wrap_question =  self.wrap_text(question)
        wrap_options = options.split(",")
        wrap_answer = answer

        self.question = SMALL_TEXT.render("Question: " + wrap_question, True, COLORS["WHITE"])
        self.question_rect = self.question.get_rect(midleft=(self.rect.midleft[0] + 20, self.rect.midleft[1] - 45))
        self.options_title = SMALL_TEXT.render("Options:", True, COLORS["WHITE"])
        self.options_title_rect = self.options_title.get_rect(midleft=(self.rect.midleft[0] + 20, self.rect.midleft[1] - 25)  )
        self.options = TINY_TEXT.render("[" + wrap_options[0] + "," + wrap_options[1] + "\n\n" + wrap_options[2] + "," + wrap_options[3] + "]", True, COLORS["WHITE"])
        self.options_rect = self.options.get_rect(midleft=(self.rect.midleft[0] + 20, self.rect.midleft[1] + 5)  )
        self.answer = SMALL_TEXT.render("Answer: " + wrap_answer, True, COLORS["WHITE"])
        self.answer_rect = self.answer.get_rect(midleft=(self.rect.midleft[0] + 20, self.rect.midleft[1] + 45))

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.question, self.question_rect)
        self.screen.blit(self.options_title, self.options_title_rect)
        self.screen.blit(self.options, self.options_rect)
        self.screen.blit(self.answer, self.answer_rect)
        self.pencil_icon.draw()
        self.trash_icon.draw()
        self.elements.draw(self.screen)

    def get_interactive_elements(self):
        return self.interactive_elements

    def get_id(self):
        return self.id
    
    def wrap_text(self, text):
        wrap_text = text
        if len(text) > 90:
            split = len(text) - 10
            if len(text) > 105:
                split = len(text) - 40
            if text[split].isalpha():
                wrap_text = text[:split] + "-\n" + text[split:]
            else:
                wrap_text = text[:split] + "\n" + text[split:]
        return wrap_text
    
    def check_option_selected(self):
        # Deprecated: initialization of the checkbox state is handled by QuestionsState
        # via FileManager.is_question_active(id). Left here for compatibility.
        pass

    def change_to_edit(self):
        self.event_manager.notify("set_edit_data", self.data)
        self.event_manager.notify("set_state", "edit")