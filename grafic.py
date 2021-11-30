import pygame
import objects
import time
import os

pygame.font.init()


WINDOW_WIDTH = 1536
WINDOW_HEIGHT = 864
FIGURE_H_WIDTH = 117
FIGURE_H_HEIGHT = 172
FIGURE_B_WIDTH = FIGURE_B_HEIGHT = 200
FIGURE_H_CEN_X = (WINDOW_WIDTH - FIGURE_H_WIDTH) // 2
FIGURE_H_Y = WINDOW_HEIGHT - FIGURE_H_HEIGHT - 70
FIGURE_H_END_X = (WINDOW_WIDTH - 117) // 2
FIGURE_H_END_Y = WINDOW_HEIGHT // 2 + 10
FIGURE_B_X = (WINDOW_WIDTH - FIGURE_B_WIDTH) // 2
FIGURE_B_Y = WINDOW_HEIGHT // 2 - FIGURE_B_HEIGHT - 10


class Sections:
    def __init__(self):
        self.menu_finished = False
        self.game_finished = True
        self.game_again = False
        self.profile_finished = True
        self.flag_list = [self.menu_finished, self.profile_finished]
        self.FPS = 60
        self.countdown = 0
        self.font = pygame.font.Font(None, 500)
        self.text = self.font.render('', True, 'black')
        self.text_width = self.text.get_width()
        self.text_height = self.text.get_height()
        self.click_flag = False
        self.figures_active = True
        self.countdown_time = time.time()
        self.click_time = time.time()
        self.human_figure = 0
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def menu(self):
        pygame.display.update()
        clock = pygame.time.Clock()
        game_button = objects.Button(300, 400, 100, 100, 'red', self.game_enter, 'game', 20, 30, 40, 'black')
        profile_button = objects.Button(600, 400, 100, 100, 'cyan', self.profile_enter, 'profile', 20, 30, 40, 'black')
        exit_button = objects.Button(900, 400, 100, 100, 'blue', self.total_exit, 'exit', 20, 30, 40, 'black')
        menu_button_list = [game_button, profile_button, exit_button]
        while not self.menu_finished:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.total_exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in menu_button_list:
                        button.click(event)
            self.screen.fill('grey')
            for button in menu_button_list:
                button.draw(self.screen)
            pygame.display.update()

    def game(self, bot_figure, victory_count, draw_count, defeat_count):
        pygame.display.update()
        clock = pygame.time.Clock()
        game_sprites = pygame.sprite.Group()
        back_button = objects.Button(0, 0, 100, 100, 'purple', self.menu_enter, 'back', 20, 30, 40, 'black')
        human_rock = objects.Figure(FIGURE_H_CEN_X - 170, FIGURE_H_Y, FIGURE_H_WIDTH, FIGURE_H_HEIGHT,
                                    'Камень человека.gif', game_sprites, FIGURE_H_END_X, FIGURE_H_END_Y)
        human_scissors = objects.Figure(FIGURE_H_CEN_X, FIGURE_H_Y, FIGURE_H_WIDTH, FIGURE_H_HEIGHT,
                                        'Ножницы человека.gif', game_sprites, FIGURE_H_END_X, FIGURE_H_END_Y)
        human_paper = objects.Figure(FIGURE_H_CEN_X + 170, FIGURE_H_Y, FIGURE_H_WIDTH, FIGURE_H_HEIGHT,
                                     'Бумага человека.gif', game_sprites, FIGURE_H_END_X, FIGURE_H_END_Y)
        start_button = objects.Button(0, 500, 100, 100, 'purple', self.game_restart, 'start', 20, 30, 40, 'black')
        figure_list = [human_rock, human_scissors, human_paper]
        game_button_list = [back_button, start_button]
        self.click_flag = False
        self.game_again = False
        self.figures_active = True
        self.human_figure = 0
        self.font = pygame.font.Font(None, 500)
        self.text = self.font.render('', True, 'black')
        result = 0
        self.countdown_tick()
        if bot_figure == 1:
            fullname = os.path.join('img', 'Камень бота.gif')
        elif bot_figure == 2:
            fullname = os.path.join('img', 'Ножницы бота.gif')
        else:
            fullname = os.path.join('img', 'Бумага бота.gif')
        image = pygame.image.load(fullname).convert()
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        bot_figure_image = pygame.transform.scale(image, (FIGURE_B_WIDTH, FIGURE_B_HEIGHT))
        while not self.game_finished and not self.game_again:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_enter()
                elif event.type == pygame.MOUSEBUTTONDOWN and self.click_flag:
                    for button in game_button_list:
                        button.click(event)
                    for figure in figure_list:
                        if figure.active:
                            figure.click(event)
                            if figure.move_flag:
                                self.human_figure = figure_list.index(figure) + 1
                                for fig in figure_list:
                                    fig.active = False
                                break
            for figure in figure_list:
                if figure.move_flag:
                    figure.move()
            if self.countdown > 0:
                if time.time() - self.countdown_time > 1:
                    self.countdown_tick()
                    self.countdown_time = time.time()
            elif not self.click_flag:
                self.text = self.font.render('', True, 'black')
                self.text_width = self.text.get_width()
                self.text_height = self.text.get_height()
                self.click_flag = True
                self.click_time = time.time()
            if self.click_flag and time.time() - self.click_time > 0.5 and self.figures_active:
                for figure in figure_list:
                    figure.active = False
                self.font = pygame.font.Font(None, 350)
                self.text = self.font.render('', True, 'black')
                if self.human_figure == 0:
                    self.text = self.font.render('Не сыграно!', True, 'black')
                elif (self.human_figure, bot_figure) in [(1, 3), (2, 1), (3, 2)]:
                    self.text = self.font.render('Поражение!', True, 'black')
                    result = -1
                elif (self.human_figure, bot_figure) in [(1, 2), (2, 3), (3, 1)]:
                    self.text = self.font.render('Победа!', True, 'black')
                    result = 1
                else:
                    self.text = self.font.render('Ничья!', True, 'black')
                self.text_width = self.text.get_width()
                self.text_height = self.text.get_height()
                self.figures_active = False
            self.screen.fill('pink')
            if self.click_flag and time.time() - self.click_time > 0.25:
                self.screen.blit(bot_figure_image, (FIGURE_B_X, FIGURE_B_Y))
            for button in game_button_list:
                button.draw(self.screen)
            game_sprites.draw(self.screen)
            self.screen.blit(self.text, ((WINDOW_WIDTH - self.text_width) // 2,
                                         (WINDOW_HEIGHT - self.text_height) // 2))
            pygame.display.update()
        return self.human_figure, result

    def profile(self):
        pygame.display.update()
        clock = pygame.time.Clock()
        self.profile_finished = False
        back_button = objects.Button(0, 0, 100, 100, 'orange', self.menu_enter, 'back', 20, 30, 40, 'black')
        profile_button_list = [back_button]
        while not self.profile_finished:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_enter()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in profile_button_list:
                        button.click(event)
            self.screen.fill('green')
            for button in profile_button_list:
                button.draw(self.screen)
            pygame.display.update()

    def menu_enter(self):
        self.menu_finished = False
        self.game_finished = True
        self.profile_finished = True
        self.flag_list = [self.menu_finished, self.game_finished, self.profile_finished]

    def game_enter(self):
        self.menu_finished = True
        self.game_finished = False
        self.game_again = False
        self.profile_finished = True
        self.flag_list = [self.menu_finished, self.game_finished, self.profile_finished]

    def profile_enter(self):
        self.menu_finished = True
        self.game_finished = True
        self.profile_finished = False
        self.flag_list = [self.menu_finished, self.game_finished, self.profile_finished]

    def total_exit(self):
        self.menu_finished = True
        self.game_finished = True
        self.profile_finished = True
        self.flag_list = [self.menu_finished, self.game_finished, self.profile_finished]

    def game_restart(self):
        self.game_again = True

    def countdown_tick(self):
        if self.countdown == 0:
            self.countdown = 5
            self.countdown_time = time.time()
        else:
            self.countdown -= 1
        if self.countdown > 0:
            self.text = self.font.render(str(self.countdown), True, 'black')
        self.text_width = self.text.get_width()
        self.text_height = self.text.get_height()
