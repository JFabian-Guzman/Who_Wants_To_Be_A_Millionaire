from config.settings import *

class TextInput:
    def __init__(self, position, width, height, event_manager, type):
        self.screen = pygame.display.get_surface()
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = position
        self.input = ""
        self.active = False
        self.handled = False
        self.event_manager = event_manager
        self.color_active = COLORS["WHITE"]
        self.color_passive = COLORS["GRAY"]
        self.color = self.color_passive
        self.border_thickness = 2
        self.backspace_delay = 100
        self.last_backspace_time = 0
        self.type = type

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect, self.border_thickness)
        self.draw_text()

    def update(self):
        self.check_keyboard_backspace()

    def draw_text(self):
        lines = self.wrap_text(self.input)
        y_offset = self.rect.top + 15  
        for line in lines:
            text_surface = TEXT.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(midtop=(self.rect.centerx, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += text_surface.get_height() + 5 
    
    def wrap_text(self, text):
        lines = []
        if (len(text) > 24 and self.type == 'option') or (len(text) > 48 and self.type == 'question'):
            mid = len(text) // 2
            first_half =  text[:mid]
            second_half =  text[mid:]
            if (ord(first_half[-1]) >= 65 and ord(first_half[-1]) <= 90 or ord(first_half[-1]) >= 97 and ord(first_half[-1]) <= 122) and (ord(second_half[0]) >= 65 and ord(second_half[0]) <= 90 or ord(second_half[0]) >= 97 and ord(second_half[0]) <= 122):
                first_half += "-"
                
            lines.append(first_half)
            lines.append(second_half)
        else:
            lines.append(text)
        return lines

    def toggle_active(self, state):
        self.active = state
        if self.active:
            self.color = self.color_active
            self.border_thickness = 3
        else:
            self.color = self.color_passive
            self.border_thickness = 2

    def set_text(self, text):
        self.input = text

    def get_input_text(self):
        return self.input
    
    def check_keyboard_backspace(self):
        key = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if self.active:
            if key[pygame.K_BACKSPACE] == True:
                if current_time - self.last_backspace_time > self.backspace_delay:
                    self.input = self.input[:-1]
                    self.last_backspace_time = current_time

    def check_keyboard_input(self, *args):
        event = args[0]
        if self.active:
            if event.key != pygame.K_BACKSPACE:
                if (self.type == 'option' and len(self.input) < MAX_LENGTH_OPTIONS) or (self.type == 'question' and len(self.input) < MAX_LENGTH_QUESTION) or (self.type == 'name' and len(self.input) < MAX_NAME_LENGTH):
                    self.event_manager.notify("warning", '')
                    self.input += event.unicode
                else:
                    if self.type == 'option':
                        self.event_manager.notify("warning", OPTION_MAX_LENGTH_WARNING)
                    else:
                        self.event_manager.notify("warning", QUESTION_MAX_LENGTH_WARNING)
                    

    def on_hover(self):
        self.color = self.color_active

    def reset_hover(self):
        if not self.active:
            self.color = self.color_passive

    def update_position(self, position):
        self.rect.center = position

    def set_up_input_events(self):
        self.event_manager.subscribe("keyboard_input", self.check_keyboard_input)