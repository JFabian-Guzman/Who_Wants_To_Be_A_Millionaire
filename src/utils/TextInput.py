from config.settings import *

class TextInput:
    def __init__(self, position, width, height, event_manager):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = position
        self.input = ""
        self.active = False
        self.handled = False
        self.event_manager = event_manager
        self.color_active = pygame.Color('white')
        self.color_passive = (115, 115, 115)
        self.color = self.color_passive
        self.border_thickness = 2

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.border_thickness)
        text_surface = TEXT.render(self.input, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 7, self.rect.y + 7))
        

    def toggle_active(self, state):
        self.active = state
        if self.active:
            self.color = self.color_active
            self.border_thickness = 3
        else:
            self.color = self.color_passive
            self.border_thickness = 2
    
    def set_default_text(self, text):
        self.input = text
    
    def get_input_text(self):
        return self.input

    def check_keyboard_input(self, *args):
        event = args[0]
        print("UNICODE:" + event.unicode)
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.input = self.input[:-1]
            else:
                self.input += event.unicode

    def set_up_input_events(self):
        self.event_manager.subscribe("keyboard_input", self.check_keyboard_input)
