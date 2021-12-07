import pygame
import objects
import time
import os

pygame.init()
pygame.font.init()

WINDOW_WIDTH = pygame.display.Info().current_w
WINDOW_HEIGHT = pygame.display.Info().current_h
FIGURE_H_WIDTH = 117
FIGURE_H_HEIGHT = 172
FIGURE_B_WIDTH = FIGURE_B_HEIGHT = 200
FIGURE_H_CEN_X = (WINDOW_WIDTH - FIGURE_H_WIDTH) // 2
FIGURE_H_Y = WINDOW_HEIGHT - FIGURE_H_HEIGHT - 70
FIGURE_H_END_X = (WINDOW_WIDTH - 117) // 2
FIGURE_H_END_Y = WINDOW_HEIGHT // 2 + 10
FIGURE_B_X = (WINDOW_WIDTH - FIGURE_B_WIDTH) // 2
FIGURE_B_Y = WINDOW_HEIGHT // 2 - FIGURE_B_HEIGHT - 10
BLACK = (0, 0, 0)


class Sections:
    def __init__(self):
        (self.menu_finished, self.game_finished, self.game_again, self.profile_finished, self.login,
         self.profile_login, self.click_flag, self.figures_active) = False, True, False, True, False, True, False, True
        self.flag_list = [self.menu_finished, self.profile_finished]
        self.FPS = 60
        self.countdown = 0
        self.font = pygame.font.Font(None, 500)
        self.text = self.font.render('', True, BLACK)
        self.text_width = self.text.get_width()
        self.text_height = self.text.get_height()
        self.countdown_time = time.time()
        self.click_time = time.time()
        self.human_figure = 0
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.name = ''
        self.text_enter = False

    def text_in(self, num):
        self.text_enter = False
        if num.key == pygame.K_RETURN:
            self.text_enter = True
        elif num.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
        elif len(self.name) < 20 and num.key != pygame.K_SPACE:
            self.name += num.unicode

    def menu(self):
        pygame.display.update()
        clock = pygame.time.Clock()
        game_button = objects.Button(WINDOW_WIDTH // 2 - 350, WINDOW_HEIGHT // 2 - 50, 100, 100, 'red',
                                     self.game_enter, 'game', 20, 30, 40, 'black')
        profile_button = objects.Button(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 - 50, 100, 100, 'cyan',
                                        self.profile_enter, 'profile', 20, 30, 40, 'black')
        exit_button = objects.Button(WINDOW_WIDTH // 2 + 250, WINDOW_HEIGHT // 2 - 50, 100, 100, 'yellow',
                                     self.total_exit, 'exit', 20, 37, 40, 'black')
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

    def game(self, bot_figure, victory_count=0, draw_count=0, defeat_count=0):
        pygame.display.update()
        clock = pygame.time.Clock()
        game_sprites = pygame.sprite.Group()
        back_button = objects.Button(0, 0, 100, 100, 'purple', self.menu_enter, 'back', 20, 30, 40, 'black')
        start_button = objects.Button(0, WINDOW_HEIGHT * 2 // 3 - 50, 100, 100, 'purple', self.game_restart, 'start',
                                      20, 30, 40, 'black')
        human_rock = objects.Figure(FIGURE_H_CEN_X - 200, FIGURE_H_Y, FIGURE_H_WIDTH, FIGURE_H_HEIGHT,
                                    'Камень человека.gif', game_sprites, FIGURE_H_END_X, FIGURE_H_END_Y)
        human_scissors = objects.Figure(FIGURE_H_CEN_X, FIGURE_H_Y, FIGURE_H_WIDTH, FIGURE_H_HEIGHT,
                                        'Ножницы человека.gif', game_sprites, FIGURE_H_END_X, FIGURE_H_END_Y)
        human_paper = objects.Figure(FIGURE_H_CEN_X + 200, FIGURE_H_Y, FIGURE_H_WIDTH, FIGURE_H_HEIGHT,
                                     'Бумага человека.gif', game_sprites, FIGURE_H_END_X, FIGURE_H_END_Y)
        figure_list = [human_rock, human_paper, human_scissors]
        game_button_list = [back_button, start_button]
        self.click_flag, self.game_again, self.figures_active = False, False, True
        self.human_figure = 0
        self.countdown = 5
        self.countdown_time = time.time()
        self.font = pygame.font.Font(None, 500)
        self.text = self.font.render(str(self.countdown), True, BLACK)
        self.text_width = self.text.get_width()
        self.text_height = self.text.get_height()
        result = 0
        if bot_figure == 1:
            fullname = os.path.join('img', 'Камень бота.gif')
        elif bot_figure == 3:
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in game_button_list:
                        if button == start_button:
                            if self.click_flag:
                                button.click(event)
                        else:
                            button.click(event)
                    for figure in figure_list:
                        if figure.active:
                            figure.click(event)
                            if figure.move_flag:
                                self.human_figure = figure_list.index(figure) + 1
                                for fig in figure_list:
                                    fig.active = False
                                break
            if self.click_flag:
                for figure in figure_list:
                    if figure.move_flag:
                        figure.move()
            if self.countdown > 0:
                if time.time() - self.countdown_time > 1:
                    self.countdown_tick()
                    self.countdown_time = time.time()
            elif not self.click_flag:
                self.text = self.font.render('', True, BLACK)
                self.text_width = self.text.get_width()
                self.text_height = self.text.get_height()
                self.click_flag = True
                self.click_time = time.time()
            self.screen.fill('pink')
            if self.click_flag and time.time() - self.click_time > 0.5:
                if self.figures_active:
                    for figure in figure_list:
                        figure.active = False
                    self.font = pygame.font.Font(None, 350)
                    if self.human_figure == 0:
                        self.text = self.font.render('Не сыграно!', True, BLACK)
                    elif (self.human_figure, bot_figure) in [(3, 1), (1, 2), (2, 3)]:
                        self.text = self.font.render('Поражение!', True, BLACK)
                        result = -1
                    elif (self.human_figure, bot_figure) in [(2, 1), (3, 2), (1, 3)]:
                        self.text = self.font.render('Победа!', True, BLACK)
                        result = 1
                    else:
                        self.text = self.font.render('Ничья!', True, BLACK)
                    self.text_width = self.text.get_width()
                    self.text_height = self.text.get_height()
                    self.figures_active = False
                if self.human_figure != 0:
                    self.screen.blit(bot_figure_image, (FIGURE_B_X, FIGURE_B_Y))
            for button in game_button_list:
                if button == start_button:
                    if self.click_flag:
                        button.draw(self.screen)
                else:
                    button.draw(self.screen)
            game_sprites.draw(self.screen)
            self.screen.blit(self.text, ((WINDOW_WIDTH - self.text_width) // 2,
                                         (WINDOW_HEIGHT - self.text_height) // 2))
            pygame.display.update()
        return self.human_figure, result

    def profile(self):
        pygame.display.update()
        clock = pygame.time.Clock()
        self.profile_finished, self.login, self.text_enter = False, False, False
        back_button = objects.Button(0, 0, 100, 100, 'orange', self.menu_enter, 'back', 20, 30, 40, 'black')
        login_button = objects.Button(WINDOW_WIDTH // 3 - 50, WINDOW_HEIGHT // 2 - 50, 300, 100, 'white',
                                      self.write_login, 'ваш логин', 20, 30, 40, 'black')
        name_button = objects.Button(550, 180, 300, 100, 'white', self.nothing, self.name, 38, 30, 40, 'black')
        wins_button = objects.Button(550, 330, 300, 100, 'white', self.nothing, 'wins:', 30, 30, 40, 'black')
        draws_button = objects.Button(550, 480, 300, 100, 'white', self.nothing, 'draws:', 30, 30, 40, 'black')
        defeats_button = objects.Button(550, 630, 300, 100, 'white', self.nothing, 'defeats:', 30, 30, 40, 'black')
        while not self.profile_finished:
            clock.tick(self.FPS)
            if self.profile_login:  # если ввели логин, то выводится информация про игрока
                profile_button_list = [back_button, login_button]
            else:
                profile_button_list = [back_button, name_button, wins_button, draws_button, defeats_button]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_enter()
                elif event.type == pygame.KEYDOWN and self.login:
                    self.text_in(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in profile_button_list:
                        button.click(event)

            if self.login:
                login_button.text, name_button.text = self.name, self.name
            if self.text_enter and self.name != '':
                self.profile_login, self.login = False, False
            self.screen.fill('green')
            for button in profile_button_list:
                button.draw(self.screen)
            pygame.display.update()

    def nothing(self):
        print(1)

    def write_login(self):
        self.login = True

    def menu_enter(self):
        self.menu_finished, self.game_finished, self.profile_finished = False, True, True
        self.flag_list = [self.menu_finished, self.profile_finished]

    def game_enter(self):
        self.menu_finished, self.game_finished, self.profile_finished, self.game_again = True, False, True, False
        self.flag_list = [self.menu_finished, self.profile_finished]

    def profile_enter(self):
        self.menu_finished, self.game_finished, self.profile_finished = True, True, False
        self.flag_list = [self.menu_finished, self.profile_finished]

    def total_exit(self):
        self.menu_finished, self.game_finished, self.profile_finished = True, True, True
        self.flag_list = [self.menu_finished, self.profile_finished]

    def game_restart(self):
        self.game_again = True

    def countdown_tick(self):
        self.countdown -= 1
        if self.countdown > 0:
            self.text = self.font.render(str(self.countdown), True, BLACK)
        self.text_width = self.text.get_width()
        self.text_height = self.text.get_height()
