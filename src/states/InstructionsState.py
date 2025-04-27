from config.settings import *
from os.path import join
from .State import *
from utils.Box import *
from utils.Button import *

class Instructions(State):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.box = Box(self.elements)
        box_rect = self.box.get_rect()

        self.setup_positions(box_rect)
        self.setup_text_elements()
        self.setup_buttons()

        self.display_continue = True
        self.click_handled = False
        self.display_extra_instructions = False

    def setup_positions(self, box_rect):
        self.title_position = (box_rect.centerx, box_rect.top + 50)
        self.instruction_position = (box_rect.centerx, box_rect.centery - 20)
        self.right_btn_pos = (box_rect.right - 150, box_rect.bottom - 75)
        self.mid_btn_pos = (box_rect.centerx, box_rect.bottom - 75)
        self.left_btn_pos = (box_rect.left + 150, box_rect.bottom - 75)

    def setup_text_elements(self):
        self.title = TITLE.render("Instructions", True, COLORS["AMBER"])
        self.title_rect = self.title.get_rect(center=self.title_position)

        self.instructions = TEXT.render(INSTRUCTIONS, True, COLORS["WHITE"])
        self.instructions_rect = self.instructions.get_rect(center=self.instruction_position)

    def setup_buttons(self):
        self.continue_btn = Button(None, self.right_btn_pos , self.event_manager)
        self.back_btn = Button(self.elements, self.left_btn_pos, self.event_manager, 'negative_btn', 'Go Back', 'WHITE')
        self.lifeline_btn = Button(None, self.right_btn_pos, self.event_manager, 'btn', 'Lifelines', 'BLACK')
        self.gamemode_btn = Button(None, self.mid_btn_pos, self.event_manager, 'btn', 'Gamemodes', 'BLACK')
        self.interactive_elements.append(self.back_btn)
        self.interactive_elements.append(self.lifeline_btn)
        self.interactive_elements.append(self.continue_btn)
        self.interactive_elements.append(self.gamemode_btn)

    def update_btn_pos(self):
        self.back_btn.update_position(self.left_btn_pos)
        self.continue_btn.update_position(self.right_btn_pos)
        self.lifeline_btn.update_position(self.right_btn_pos)
        self.gamemode_btn.update_position(self.mid_btn_pos)

    def draw(self):
        self.elements.draw(self.screen)
        self.screen.blit(self.title, self.title_rect)
        self.screen.blit(self.instructions, self.instructions_rect)
        if self.display_continue:
            self.continue_btn.draw()
            self.continue_btn.update()
            
        if self.display_extra_instructions:
            self.lifeline_btn.draw()
            self.lifeline_btn.update()
            self.gamemode_btn.draw()
            self.gamemode_btn.update()
        

    def update(self):
        self.elements.update()
        self.check_click()
        self.update_cursor_state()

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled:
                if self.display_continue:
                    self.continue_btn.check_notify_state("player")
                else:
                    self.lifeline_btn.check_notify_state("lifeline_instructions")
                    self.gamemode_btn.check_notify_state("gamemode_instructions")
                self.event_manager.notify("clear_player_data")
                self.back_btn.check_notify_state("menu")
                self.click_handled = True
        else:
            self.click_handled = False

    def display_continue_btn(self, *args):
        self.display_extra_instructions = False
        self.display_continue = True
        if self.lifeline_btn in self.interactive_elements:
            self.interactive_elements.remove(self.lifeline_btn)
        if self.gamemode_btn in self.interactive_elements:
            self.interactive_elements.remove(self.gamemode_btn)
        if not self.continue_btn in self.interactive_elements:
            self.interactive_elements.append(self.continue_btn)
        
    def erase_continue_btn(self, *args):
        self.display_extra_instructions = True
        self.display_continue = False
        if self.continue_btn in self.interactive_elements:
            self.interactive_elements.remove(self.continue_btn)
        if not self.lifeline_btn in self.interactive_elements:
            self.interactive_elements.append(self.lifeline_btn)
        if not self.gamemode_btn in self.interactive_elements:
            self.interactive_elements.append(self.gamemode_btn)

    def update_size(self, *args):
        self.box.updates_position()
        box_rect = self.box.get_rect()
        self.setup_positions(box_rect)
        self.setup_text_elements()
        self.update_btn_pos()
        
    def set_up_instruction_events(self):
        self.event_manager.subscribe("display_continue_btn", self.display_continue_btn)
        self.event_manager.subscribe("erase_continue_btn", self.erase_continue_btn)
        self.event_manager.subscribe("update_size", self.update_size)