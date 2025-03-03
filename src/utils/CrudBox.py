from config.settings import *
from os.path import join
from utils.Icon import *

class CrudBox(pygame.sprite.Sprite):
    def __init__(self, question, options, answer, id, position, event_manager):
        super().__init__()

        self.screen = pygame.display.get_surface()
        self.interactive_elements = []
        self.event_manager = event_manager

        self.image = pygame.image.load(join("assets", "img", "crud_box.png")).convert_alpha()
        self.rect = self.image.get_rect(center=position)

        self.pencil_icon = Icon((self.rect.midright[0] - 80, self.rect.midright[1] + 40), "pencil")
        self.trash_icon = Icon((self.rect.midright[0] - 25, self.rect.midright[1] + 40), "trash")
        self.id = id
        self.data = [question, options, answer, id]

        self.interactive_elements.append(self.pencil_icon)
        self.interactive_elements.append(self.trash_icon)

        self.setup_text_elements(question, options, answer)

    def setup_text_elements(self, question, options, answer):
        wrap_options = self.wrap_text(options)
        wrap_answer = self.wrap_text(answer)

        self.question = TEXT.render("Question: " + question, True, COLORS["WHITE"])
        self.question_rect = self.question.get_rect(midleft=(self.rect.midleft[0] + 20, self.rect.midleft[1] - 45))
        self.options = TEXT.render("Options: " + wrap_options, True, COLORS["WHITE"])
        self.options_rect = self.options.get_rect(midleft=(self.rect.midleft[0] + 20, self.rect.midleft[1]))
        self.answer = TEXT.render("Answer: " + wrap_answer, True, COLORS["WHITE"])
        self.answer_rect = self.answer.get_rect(midleft=(self.rect.midleft[0] + 20, self.rect.midleft[1] + 45))

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.question, self.question_rect)
        self.screen.blit(self.options, self.options_rect)
        self.screen.blit(self.answer, self.answer_rect)
        self.pencil_icon.draw()
        self.trash_icon.draw()

    def get_interactive_elements(self):
        return self.interactive_elements

    def get_id(self):
        return self.id

    def wrap_text(self, text):
        wrap_text = text
        if len(text) > 60:
            split = len(text) - 10
            if text[split].isalpha():
                wrap_text = text[:split] + "-\n\n" + text[split:]
            else:
                wrap_text = text[:split] + "\n\n" + text[split:]
        return wrap_text

    def change_to_edit(self):
        self.event_manager.notify("set_edit_data", self.data)
        self.event_manager.notify("set_state", "edit")