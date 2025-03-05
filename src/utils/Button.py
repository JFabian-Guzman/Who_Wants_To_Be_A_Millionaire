from config.settings import *
from os.path import join

class Button(pygame.sprite.Sprite):
    def __init__(self, group, position, event_manager, type='btn', text='Continue', color='BLACK'):
        if group != None:
            super().__init__(group)
        else:
            super().__init__()
        self.screen = pygame.display.get_surface()
        self.sprites = []
        self.current_sprite = 0
        self.run_animation = False
        self.type = type

        self.sprites.append(pygame.image.load(join("assets", "img", type + '.png')).convert_alpha())
        self.sprites.append(pygame.image.load(join("assets", "img", "hover_"+ type + '_animation1.png')).convert_alpha())
        self.sprites.append(pygame.image.load(join("assets", "img", "hover_"+ type + '_animation2.png')).convert_alpha())
        self.sprites.append(pygame.image.load(join("assets", "img", "hover_"+ type + '_animation3.png')).convert_alpha())
        self.sprites.append(pygame.image.load(join("assets", "img", "hover_"+ type + '_animation4.png')).convert_alpha())
        self.sprites.append(pygame.image.load(join("assets", "img", "hover_"+ type + '_animation5.png')).convert_alpha())
        self.sprites.append(pygame.image.load(join("assets", "img", "hover_"+ type + '_animation6.png')).convert_alpha())
        self.sprites.append(pygame.image.load(join("assets", "img", "hover_"+ type + '_animation7.png')).convert_alpha())
        self.sprites.append(pygame.image.load(join("assets", "img", "hover_"+ type + '_animation8.png')).convert_alpha())

        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(center=position)

        self.text = TEXT.render(text, True, COLORS[color])
        self.text_rect = self.text.get_rect(center=self.rect.center)
        
        self.event_manager = event_manager

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.write_text()
        if self.run_animation:
            self.animate()

    def write_text(self):
        self.screen.blit(self.text, self.text_rect)

    def get_rect(self):
        return self.rect
    
    def on_hover(self):
        self.start_animation()

    def reset_hover(self):
        self.current_sprite = 0 
        self.image = self.sprites[self.current_sprite]

    def animate(self):
        self.current_sprite += 0.8
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = len(self.sprites) - 1
            self.stop_animation()
        self.image = self.sprites[int(self.current_sprite)]

    def start_animation(self):
        self.run_animation = True

    def stop_animation(self):
        self.run_animation = False

    def check_notify_state(self, state: str):
        state_change = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.event_manager.notify("set_state", state)
            state_change = True
        return state_change

