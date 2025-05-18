from config.settings import *
from os.path import join
from .State import *
from utils.Box import *
from utils.Button import *
from utils.LifeLine import *

class LifelineInstrucitions(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.box = Box(self.elements)
        box_rect = self.box.get_rect()

        self.setup_positions(box_rect)
        self.setup_text_elements()
        self.setup_buttons(box_rect)

        self.display_continue = True
        self.click_handled = False
        self.display_lifeline = False

    def setup_positions(self, box_rect):
        self.title_position = (box_rect.centerx, box_rect.top + 50)
        self.shield_position = (box_rect.left + 150, box_rect.centery - 125)
        self.fifty_position = (box_rect.left + 150, box_rect.centery - 25)
        self.switch_position = (box_rect.left + 150, box_rect.centery + 75)
        self.shield_text_position = (self.shield_position[0] + 50, self.shield_position[1])
        self.fifty_text_position = (self.fifty_position[0] + 50, self.fifty_position[1])
        self.switch_text_position = (self.switch_position[0] + 50, self.switch_position[1])

    def setup_text_elements(self):
        self.title = TITLE.render("Lifelines", True, COLORS["AMBER"])
        self.title_rect = self.title.get_rect(center=self.title_position)

        self.shield_text = TEXT.render(LIFELINE_INSTRUCTIONS["SHIELD"], True, COLORS["WHITE"])
        self.shield_text_rect = self.shield_text.get_rect(midleft=self.shield_text_position)

        self.fifty_text = TEXT.render(LIFELINE_INSTRUCTIONS["50/50"], True, COLORS["WHITE"])
        self.fifty_text_rect = self.fifty_text.get_rect(midleft=self.fifty_text_position)

        self.switch_text = TEXT.render(LIFELINE_INSTRUCTIONS["CHANGE_QUESTION"], True, COLORS["WHITE"])
        self.switch_text_rect = self.switch_text.get_rect(midleft=self.switch_text_position)


        self.shield_lifeline = Lifeline(self.shield_position, "shield_lifeline")
        self.fifty_fifty_lifeline = Lifeline(self.fifty_position, "fifty_fifty_lifeline")
        self.switch_lifeline = Lifeline(self.switch_position, "switch_lifeline")


    def setup_buttons(self, box_rect):
        self.back_btn = Button(self.elements, (box_rect.left + 150, box_rect.bottom - 75), self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.interactive_elements.append(self.back_btn)

    def draw(self):
        self.elements.draw(self.screen)
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.shield_text, self.shield_text_rect)
        self.screen.blit(self.fifty_text, self.fifty_text_rect)
        self.screen.blit(self.switch_text, self.switch_text_rect)
        self.shield_lifeline.draw()
        self.fifty_fifty_lifeline.draw()
        self.switch_lifeline.draw()

    def update(self):
        self.elements.update()
        self.check_click()
        self.update_cursor_state()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                self.back_btn.check_notify_state("instructions")
                self.click_handled = True
        else:
            self.click_handled = False


    def update_size(self, *args):
        self.box.updates_position()
        box_rect = self.box.get_rect()
        self.setup_positions(box_rect)
        self.setup_text_elements()
        self.back_btn.update_position((box_rect.left + 150, box_rect.bottom - 75))
        

    def set_up_lifeline_instructins_events(self):
        self.event_manager.subscribe("update_size", self.update_size)