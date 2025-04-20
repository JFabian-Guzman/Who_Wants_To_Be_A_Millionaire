from config.settings import *
from utils.Cursor import *
from .State import *
from utils.Option import *
from utils.Questions import *
from utils.Score import *
from utils.Surrender import *
from utils.ConfirmModal import *
from utils.SurrederModal import *
from utils.LifeLine import *
from utils.Heart import *
from utils.Clock import *
from utils.Checkpoint import *
import random

LIFELINE_1_POSITION = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 275)
LIFELINE_2_POSITION = (WINDOW_WIDTH / 2 + 75, WINDOW_HEIGHT / 2 - 275)
LIFELINE_3_POSITION = (WINDOW_WIDTH / 2 - 75, WINDOW_HEIGHT / 2 - 275)

class Play(State):
    def __init__(self, event_manager, file_manager):
        super().__init__(event_manager)

        self.save_score = 0
        self.current_level = 0
        self.question_index = 0
        self.total_lives = 0
        self.lives = 0
        self.number_questions = 0
        self.correct_answers = 0
        self.wrong_answer = 0
        self.final_score = 0
        self.click_handled = False
        self.display_modal = False
        self.display_surrender_modal = False
        self.active_shield = False
        self.practice_mode = False
        self.animating = False
        self.answer = ""
        self.difficulty = ""
        self.question = ""
        self.player_name  = ""
        self.options = []
        self.lifelines = []
        self.file_manager = file_manager
        self.start_time = pygame.time.get_ticks()
        self.sound = pygame.mixer.Sound(join("assets", "sounds" ,"game_start.mp3"))
        self.sound.set_volume(.5)
        

        self.setup_interactive_elements()
        self.setup_lifelines()
        self.setup_hearts()
        self.get_last_level()

        # Set up events
        self.question_obj.set_up_question_events()

    def setup_interactive_elements(self):
        self.positions = [
            (self.width // 2 - 375, self.height // 2 + 100),
            (self.width // 2 - 375, self.height // 2 + 200),
            (self.width // 2 + 375, self.height // 2 + 100),
            (self.width // 2 + 375, self.height // 2 + 200)
        ]
        for position in self.positions:
            self.interactive_elements.append(Option("", position, self.elements))
        self.question_obj = Question(self.elements, self.event_manager)
        self.question_rect = self.question_obj.get_rect()
        self.clock = Clock(self.elements)
        self.score = Score(self.elements, (self.question_rect.centerx, self.question_rect.bottom - 20))
        self.checkpoint = Checkpoint()
        self.surrender = Surrender(self.elements, self.event_manager, (self.question_rect.left + 150, self.question_rect.top + 15))
        self.modal = ConfirmModal(self.event_manager)
        self.surrender_modal = SurrenderModal(self.event_manager)
        self.interactive_elements.append(self.surrender)

    def setup_lifelines(self):
        self.shield_lifeline = Lifeline((self.question_rect.centerx , self.question_rect.top + 15), "shield_lifeline")
        self.fifty_fifty_lifeline = Lifeline((self.question_rect.centerx - 75 , self.question_rect.top + 15), "fifty_fifty_lifeline")
        self.switch_lifeline = Lifeline((self.question_rect.centerx + 75 , self.question_rect.top + 15), "switch_lifeline")
        self.interactive_elements.append(self.shield_lifeline)
        self.interactive_elements.append(self.fifty_fifty_lifeline)
        self.interactive_elements.append(self.switch_lifeline)

    def setup_hearts(self):
        self.hearts = []
        for i_heart in range(5):
            heart_position = (self.question_rect.right - 90 - (50 * i_heart), self.question_rect.top + 15)
            self.hearts.append(Heart(heart_position))

    def get_last_level(self):
        self.last_level = self.file_manager.get_last_level()

    def draw(self):
        self.elements.draw(self.screen)
        self.draw_lifelines()
        self.draw_hearts()
        if self.current_level % 5 == 0 and self.current_level > 0:
            self.checkpoint.draw()

    def draw_lifelines(self):
        self.shield_lifeline.draw()
        self.fifty_fifty_lifeline.draw()
        self.switch_lifeline.draw()

    def draw_hearts(self):
        for i in range(self.total_lives):
            self.hearts[i].draw()

    def update(self):
        self.elements.update()
        self.clock.update_time()    
        if self.display_modal:
            self.modal.draw()
            self.modal.update()
        elif self.display_surrender_modal:
            self.surrender_modal.draw()
            self.surrender_modal.update()
        else:
            self.update_cursor_state()
            self.display_options()
            self.click_option()
            self.click_lifeline()
            for heart in self.hearts:
                heart.update()
            for lifeline in self.lifelines:
                lifeline.update()
            if self.current_level % 5 == 0 and self.current_level > 0:
                self.checkpoint.update()
            

    def display_options(self):
        for i in range(4):
            self.interactive_elements[i].set_title(self.options[i])

    def generate_random_index(self, *args):
        self.number_questions = len(self.file_manager.get_data()[self.current_level])
        self.question_index = random.randrange(self.number_questions)
        if self.number_questions > 1:
            # Avoid generating the same question if a switch is made
            while self.question == self.file_manager.get_data()[self.current_level][self.question_index]["question"]:
                self.question_index = random.randrange(self.number_questions)

    def update_display_data(self, *args): 
        self.options = self.file_manager.get_data()[self.current_level][self.question_index]["options"]
        self.answer = self.file_manager.get_data()[self.current_level][self.question_index]["answer"]
        self.question = self.file_manager.get_data()[self.current_level][self.question_index]["question"]
        self.event_manager.notify("change_question", self.question)

    def shuffle_options(self, *args):
        random.shuffle(self.options)

    def click_option(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled and not self.animating:
                for i in range(4):
                    if self.interactive_elements[i].get_rect().collidepoint(pygame.mouse.get_pos()) and self.interactive_elements[i].get_title() != '':
                        self.modal.set_option(i)
                        self.switch_modal()
                        self.click_handled = True
                        return
        else:
            self.click_handled = False

    def play_sound(self, *args):
        self.sound.play()

    def click_lifeline(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.click_handled and not self.animating:
                for lifeline in self.lifelines:
                    if lifeline.get_rect().collidepoint(pygame.mouse.get_pos()):
                        self.animating = True
                        lifeline.start_animation(callback=lambda: self.handle_lifeline_click(lifeline))
                        self.click_handled = True
                        return
        else:
            self.click_handled = False

    def handle_lifeline_click(self, lifeline):
        if lifeline.get_type() == "fifty_fifty_lifeline":
            self.set_options(lifeline.fifty_fifty_lifeline(self.options, self.answer))
        elif lifeline.get_type() == "switch_lifeline":
            self.switch()
        elif lifeline.get_type() == "shield_lifeline":
            for heart in self.hearts:
                heart.start_animation(shield= True)
            self.active_shield = True
        self.lifelines.remove(lifeline)
        self.animating = False


    def switch(self):
        prev_index = self.question_index
        self.generate_random_index()
        if prev_index != self.question_index:
            self.update_display_data()
            self.shuffle_options()

    def start_game(self, *args):
        self.save_score = 0
        self.current_level = 0
        self.final_score = 0
        self.practice_mode = False
        self.score.set_practice_mode(False)
        self.score.set_score(self.final_score)

        self.get_last_level()
        self.load_difficulty()
        self.reset_hearts()
        self.score.restart()
        self.reset_lifelines()
        self.restart_timer()

    def load_difficulty(self):
        if self.difficulty == 'Practice':
            self.lives = 0
            self.correct_answers = 0
            self.wrong_answer = 0
            self.score.set_practice_mode(True)
            self.practice_mode = True
        elif self.difficulty == 'Easy':
            self.lives = 5
        elif self.difficulty == 'Normal':
            self.lives = 3
        elif self.difficulty == 'Hard':
            self.lives = 1

    def restart_timer(self):
        self.start_time = pygame.time.get_ticks()
        self.clock.restart_time()

    def calc_score(self):
        max_score = 100 * self.current_level
        elapsed_time = round((pygame.time.get_ticks() - self.start_time) / 1000)
        self.final_score += round(max_score / max(elapsed_time, 1))

    def reset_hearts(self):
        for i in range(self.lives):
            self.hearts[i].enable()
        self.total_lives = self.lives

    def reset_lifelines(self):
        self.lifelines.clear()
        self.lifelines.append(self.shield_lifeline)
        self.lifelines.append(self.fifty_fifty_lifeline)
        self.lifelines.append(self.switch_lifeline)

        self.fifty_fifty_lifeline.enable()
        self.switch_lifeline.enable()
        self.shield_lifeline.enable()

    def switch_modal(self, *args):
        self.display_modal = not self.display_modal
        self.surrender.set_disable(self.display_modal)

    def validate_answer(self, *args):
        option_position = args[0]
        option = self.interactive_elements[option_position]
        selected_option = option.get_title().lower()
        correct_answer = self.answer.lower()
        self.animating = True
        if selected_option == correct_answer:
            option.start_animation(callback=lambda: self.handle_correct_answer())
        else:
            option.start_animation(callback=lambda: self.handle_wrong_answer(option_position),wrong=True)

    def handle_correct_answer(self):
        self.current_level += 1
        self.calc_score()
        if self.active_shield:
            for heart in self.hearts:
                heart.start_animation(shield=True, reverse =True)
        self.active_shield = False

        # Save levels (5,10,15)
        if self.current_level % 5 == 0:
            self.save_score = self.final_score

        if self.practice_mode:
            self.score.increment_correct_answers()
            self.correct_answers += 1

        if self.current_level == self.last_level:
            self.display_final_screen()
            self.event_manager.notify("write_podium", (self.player_name, self.final_score))
        else:
            self.restart_timer()
            self.change_question()
            self.score.set_score(self.final_score)
            self.score.set_level(self.current_level + 1)

        self.animating = False

    def handle_wrong_answer(self, option_position):
        if self.active_shield:
            self.active_shield = False
            self.options[option_position] = ''
            for heart in self.hearts:
                heart.start_animation(shield=True, reverse =True)
            self.animating = False
            return

        if not self.practice_mode:
            self.hearts[self.total_lives - self.lives].disable()
            self.lives -= 1

        if self.lives == 0 and not self.practice_mode:
            self.event_manager.notify("game_over_message", (self.answer, self.save_score))
            self.event_manager.notify("set_state", "game over")
            self.event_manager.notify("write_podium", (self.player_name, self.save_score))
        elif self.practice_mode:
            self.current_level += 1
            self.wrong_answer += 1
            if self.current_level == self.last_level:
                self.display_practice_summary()
            else:
                self.change_question()
                self.score.increment_wrong_answers()
        self.animating = False

    def display_practice_summary(self):
        self.event_manager.notify("set_state", "practice summary")
        self.event_manager.notify("practice_results", (self.correct_answers, self.wrong_answer))

    def switch_surrender_modal(self, *args):
        self.click_handled = True
        self.display_surrender_modal = not self.display_surrender_modal
        self.surrender.switch_modal_display()

    def change_question(self):
        self.generate_random_index()
        self.update_display_data()
        self.shuffle_options()
        if self.current_level % 5 == 0:
            self.checkpoint.restart_animation()
    

    def display_final_screen(self, *args):
        if self.current_level == 0:
            self.event_manager.notify("set_state", "menu")
        elif self.practice_mode:
            self.display_practice_summary()
        else:
            self.event_manager.notify("set_state", "win")
            self.event_manager.notify("final_reward", self.final_score)

    def set_difficulty(self, *args):
        self.difficulty = args[0]

    def set_options(self, options):
        self.options = options

    def set_name(self, *args):
        self.player_name = args[0]

    def update_size(self, *args):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        self.positions = [
            (self.width // 2 - 375, self.height // 2 + 100),
            (self.width // 2 - 375, self.height // 2 + 200),
            (self.width // 2 + 375, self.height // 2 + 100),
            (self.width // 2 + 375, self.height // 2 + 200)
        ]
        for i, option in enumerate(self.interactive_elements[:4]):
            option.update_position(self.positions[i])
        self.clock.update_position()
        self.question_obj.update_position()
        self.question_rect = self.question_obj.get_rect()
        self.surrender.update_position((self.question_rect.left + 150, self.question_rect.top + 15))
        self.score.update_position((self.question_rect.centerx, self.question_rect.bottom - 20))
        self.surrender_modal.update_position()
        self.modal.update_position()
        self.checkpoint.update_position()
        lifeline_pos = [
            (self.question_rect.centerx , self.question_rect.top + 15), 
            (self.question_rect.centerx - 75 , self.question_rect.top + 15), 
            (self.question_rect.centerx + 75 , self.question_rect.top + 15)
        ]

        # Lifelines are in pos 5 to 8 of interactive_elements
        for i_pos_lifeline, lifeline in enumerate(self.interactive_elements[5:8], start=5):
            lifeline.update_position(lifeline_pos[i_pos_lifeline - 5])

        for i_heart, heart in enumerate(self.hearts):
            heart_position = (self.question_rect.right - 90 - (50 * i_heart), self.question_rect.top + 15)
            heart.update_position(heart_position)

        for item in self.interactive_elements:
            print(item)



    def set_up_play_events(self):
        self.event_manager.subscribe("display_question", self.update_display_data)
        self.event_manager.subscribe("choose_random_question", self.generate_random_index)
        self.event_manager.subscribe("shuffle_options", self.shuffle_options)
        self.event_manager.subscribe("start_game", self.start_game)
        self.event_manager.subscribe("switch_modal", self.switch_modal)
        self.event_manager.subscribe("validate_answer", self.validate_answer)
        self.event_manager.subscribe("display_surrender_modal", self.switch_surrender_modal)
        self.event_manager.subscribe("display_final_screen", self.display_final_screen)
        self.event_manager.subscribe("set_difficulty", self.set_difficulty)
        self.event_manager.subscribe("set_player_name", self.set_name)
        self.event_manager.subscribe("update_size", self.update_size)
        self.event_manager.subscribe("play_start_game_sound", self.play_sound)