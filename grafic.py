import pygame
import objects
import time
import os

pygame.init()
pygame.font.init()

WINDOW_WIDTH = pygame.display.Info().current_w
WINDOW_HEIGHT = pygame.display.Info().current_h
FIGURE_H_WIDTH = int(117 * WINDOW_WIDTH / 1536)
FIGURE_H_HEIGHT = int(172 * WINDOW_HEIGHT / 864)
FIGURE_B_WIDTH = FIGURE_B_HEIGHT = int(200 * WINDOW_WIDTH / 1536)
FIGURE_H_CEN_X = (WINDOW_WIDTH - FIGURE_H_WIDTH) // 2
FIGURE_H_Y = WINDOW_HEIGHT - FIGURE_H_HEIGHT - int(60 * WINDOW_HEIGHT / 864)
FIGURE_H_END_X = (WINDOW_WIDTH - 117) // 2
FIGURE_H_END_Y = FIGURE_H_Y - FIGURE_H_HEIGHT
FIGURE_B_X = (WINDOW_WIDTH - FIGURE_B_WIDTH) // 2
FIGURE_B_Y = FIGURE_H_END_Y - FIGURE_B_HEIGHT
BLACK = (0, 0, 0)


class Sections:
    def __init__(self):
        (self.menu_finished, self.game_finished, self.game_again, self.profile_finished, self.login,
         self.profile_login, self.click_flag, self.figures_active, self.text_enter, self.login_please_caption) = \
            False, True, False, True, False, True, False, True, False, False
        self.flag_list = [self.menu_finished, self.profile_finished]
        self.FPS = 60
        self.countdown = 0
        self.font_500 = pygame.font.Font(None, int(500 * WINDOW_WIDTH / 1536))
        self.font_350 = pygame.font.Font(None, int(350 * WINDOW_WIDTH / 1536))
        self.font_50 = pygame.font.Font(None, int(50 * WINDOW_WIDTH / 1536))
        self.font_40 = pygame.font.Font(None, int(40 * WINDOW_WIDTH / 1536))
        self.text = self.font_500.render('', True, BLACK)
        self.text_width, self.text_height = self.text.get_width(), self.text.get_height()
        self.login_please = self.font_50.render('Пожалуйста, введите логин в разделе profile.', True, BLACK)
        self.login_please_width = self.login_please.get_width()
        self.login_please_height = self.login_please.get_height()
        self.countdown_time = time.time()
        self.click_time = time.time()
        self.human_figure = 0
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.name = self.unfinished_name = ''
        self.name_caption = self.font_50.render(self.name, True, BLACK)
        self.name_caption_width = self.name_caption.get_width()
        self.name_caption_height = self.name_caption.get_height()

    def text_in(self, num):
        self.text_enter = False
        if num.key == pygame.K_RETURN:
            self.text_enter = True
        elif num.key == pygame.K_BACKSPACE:
            self.unfinished_name = self.unfinished_name[:-1]
        elif len(self.unfinished_name) < 20 and num.unicode != '$':
            self.unfinished_name += num.unicode

    def menu(self):
        pygame.display.update()
        clock = pygame.time.Clock()
        game_button = objects.Button(WINDOW_WIDTH // 2 - int(350 * WINDOW_WIDTH / 1536),
                                     WINDOW_HEIGHT // 2 - int(50 * WINDOW_HEIGHT / 864), int(100 * WINDOW_WIDTH / 1536),
                                     int(100 * WINDOW_HEIGHT / 864), 'red', self.game_check, 'game',
                                     int(40 * WINDOW_WIDTH / 1536), int(14 * WINDOW_WIDTH / 1536),
                                     int(35 * WINDOW_HEIGHT / 864), 'black')
        profile_button = objects.Button(WINDOW_WIDTH // 2 - int(50 * WINDOW_WIDTH / 1536),
                                        WINDOW_HEIGHT // 2 - int(50 * WINDOW_HEIGHT / 864),
                                        int(100 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'cyan',
                                        self.profile_enter, 'profile', int(40 * WINDOW_WIDTH / 1536),
                                        int(8 * WINDOW_WIDTH / 1536), int(35 * WINDOW_HEIGHT / 864), 'black')
        exit_button = objects.Button(WINDOW_WIDTH // 2 + int(250 * WINDOW_WIDTH / 1536),
                                     WINDOW_HEIGHT // 2 - int(50 * WINDOW_HEIGHT / 864), int(100 * WINDOW_WIDTH / 1536),
                                     int(100 * WINDOW_HEIGHT / 864), 'yellow', self.total_exit, 'exit',
                                     int(40 * WINDOW_WIDTH / 1536), int(23 * WINDOW_WIDTH / 1536),
                                     int(35 * WINDOW_HEIGHT / 864), 'black')
        menu_button_list = [game_button, profile_button, exit_button]
        self.login_please_caption = False
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
            if self.login_please_caption:
                self.screen.blit(self.login_please, ((WINDOW_WIDTH - self.login_please_width) // 2,
                                                     (WINDOW_HEIGHT - self.login_please_height * 10) // 2))
            pygame.display.update()

    def game(self, bot_figure, win_count, draw_count, defeat_count):
        pygame.display.update()
        clock = pygame.time.Clock()
        game_sprites = pygame.sprite.Group()
        back_button = objects.Button(0, 0, int(100 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'purple',
                                     self.menu_enter, 'back', int(40 * WINDOW_WIDTH / 1536),
                                     int(17 * WINDOW_WIDTH / 1536), int(35 * WINDOW_HEIGHT / 864), 'black')
        start_button = objects.Button(0, WINDOW_HEIGHT * 2 // 3 - int(50 * WINDOW_HEIGHT / 864),
                                      int(100 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'purple',
                                      self.game_restart, 'start', int(40 * WINDOW_WIDTH / 1536),
                                      int(16 * WINDOW_WIDTH / 1536), int(35 * WINDOW_HEIGHT / 864), 'black')
        name_button = objects.Button(WINDOW_WIDTH // 2 - int(250 * WINDOW_WIDTH / 1536), int(814 * WINDOW_HEIGHT / 864),
                                     int(500 * WINDOW_WIDTH / 1536), int(40 * WINDOW_HEIGHT / 864), 'green',
                                     self.nothing, self.name, int(40 * WINDOW_WIDTH / 1536),
                                     (int(500 * WINDOW_WIDTH / 1536) - self.name_caption_width) // 2,
                                     (int(44 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        the_rock_name_button = objects.Button(WINDOW_WIDTH // 2 - int(100 * WINDOW_WIDTH / 1536),
                                              int(220 * WINDOW_HEIGHT / 864), int(200 * WINDOW_WIDTH / 1536),
                                              int(40 * WINDOW_HEIGHT / 864), 'red', self.nothing, 'The Rock',
                                              int(40 * WINDOW_WIDTH / 1536), int(38 * WINDOW_WIDTH / 1536),
                                              (int(44 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        the_rock = objects.Figure(WINDOW_WIDTH // 2 - int(100 * WINDOW_WIDTH / 1536), int(10 * WINDOW_HEIGHT / 864),
                                  int(200 * WINDOW_WIDTH / 1536), int(200 * WINDOW_HEIGHT / 864), 'Скала.jpg',
                                  game_sprites, FIGURE_H_END_X, FIGURE_H_END_Y)
        win_button = objects.Button(WINDOW_WIDTH - int(275 * WINDOW_WIDTH / 1536), int(10 * WINDOW_HEIGHT / 864),
                                    int(265 * WINDOW_WIDTH / 1536), int(40 * WINDOW_HEIGHT / 864), 'green',
                                    self.nothing, 'Побед: ' + ' ' * (13 - len(str(win_count))) + str(win_count),
                                    int(40 * WINDOW_WIDTH / 1536), int(6 * WINDOW_WIDTH / 1536),
                                    (int(44 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        draw_button = objects.Button(WINDOW_WIDTH - int(275 * WINDOW_WIDTH / 1536), int(60 * WINDOW_HEIGHT / 864),
                                     int(265 * WINDOW_WIDTH / 1536), int(40 * WINDOW_HEIGHT / 864), 'yellow',
                                     self.nothing, 'Ничьи: ' + ' ' * (14 - len(str(draw_count))) + str(draw_count),
                                     int(40 * WINDOW_WIDTH / 1536), int(6 * WINDOW_WIDTH / 1536),
                                     (int(44 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        defeat_button = objects.Button(WINDOW_WIDTH - int(275 * WINDOW_WIDTH / 1536), int(110 * WINDOW_HEIGHT / 864),
                                       int(265 * WINDOW_WIDTH / 1536), int(40 * WINDOW_HEIGHT / 864), 'red',
                                       self.nothing,
                                       'Поражений: ' + ' ' * (5 - len(str(defeat_count))) + str(defeat_count),
                                       int(40 * WINDOW_WIDTH / 1536), int(6 * WINDOW_WIDTH / 1536),
                                       (int(44 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        human_rock = objects.Figure(FIGURE_H_CEN_X - int(200 * WINDOW_WIDTH / 1536), FIGURE_H_Y, FIGURE_H_WIDTH,
                                    FIGURE_H_HEIGHT, 'Камень человека.gif', game_sprites, FIGURE_H_END_X,
                                    FIGURE_H_END_Y)
        human_scissors = objects.Figure(FIGURE_H_CEN_X, FIGURE_H_Y, FIGURE_H_WIDTH, FIGURE_H_HEIGHT,
                                        'Ножницы человека.gif', game_sprites, FIGURE_H_END_X, FIGURE_H_END_Y)
        human_paper = objects.Figure(FIGURE_H_CEN_X + int(200 * WINDOW_WIDTH / 1536), FIGURE_H_Y, FIGURE_H_WIDTH,
                                     FIGURE_H_HEIGHT, 'Бумага человека.gif', game_sprites, FIGURE_H_END_X,
                                     FIGURE_H_END_Y)
        figure_list = [human_rock, human_paper, human_scissors]
        game_button_list = [back_button, start_button, name_button, the_rock_name_button, win_button, draw_button,
                            defeat_button]
        self.click_flag, self.game_again, self.figures_active = False, False, True
        self.human_figure = 0
        self.countdown = 5
        self.countdown_time = time.time()
        self.text = self.font_500.render(str(self.countdown), True, BLACK)
        self.text_width = self.text.get_width()
        self.text_height = self.text.get_height()
        self.name_caption = self.font_40.render(self.name, True, BLACK)
        self.name_caption_width = self.name_caption.get_width()
        self.name_caption_height = self.name_caption.get_height()
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
                            if figure.move_flag:
                                continue
                            figure.click(event)
                            if figure.move_flag:
                                if self.click_flag:
                                    if self.human_figure == 0:
                                        self.human_figure = figure_list.index(figure) + 1
                                        for fig in figure_list:
                                            fig.active = False
                                    else:
                                        figure.move_flag = False
                                        figure.image.set_colorkey((255, 0, 0))
                                else:
                                    self.human_figure = figure_list.index(figure) + 1
                                    for fig in figure_list:
                                        if fig != figure:
                                            fig.move_flag = False
                                            fig.image.set_colorkey((255, 0, 0))
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
                self.text = self.font_350.render('', True, BLACK)
                self.text_width = self.text.get_width()
                self.text_height = self.text.get_height()
                self.click_flag = True
                self.click_time = time.time()
            self.screen.fill('pink')
            if self.click_flag and time.time() - self.click_time > 0.5:
                if self.figures_active:
                    for figure in figure_list:
                        figure.active = False
                    if self.human_figure == 0:
                        self.text = self.font_350.render('Не сыграно!', True, BLACK)
                    elif (self.human_figure, bot_figure) in [(3, 1), (1, 2), (2, 3)]:
                        self.text = self.font_350.render('Поражение!', True, BLACK)
                        result = -1
                        defeat_count += 1
                    elif (self.human_figure, bot_figure) in [(2, 1), (3, 2), (1, 3)]:
                        self.text = self.font_350.render('Победа!', True, BLACK)
                        result = 1
                        win_count += 1
                    else:
                        self.text = self.font_350.render('Ничья!', True, BLACK)
                        draw_count += 1
                    self.text_width = self.text.get_width()
                    self.text_height = self.text.get_height()
                    self.figures_active = False
                    win_button.text = 'Побед: ' + ' ' * (13 - len(str(win_count))) + str(win_count)
                    draw_button.text = 'Ничьи: ' + ' ' * (14 - len(str(draw_count))) + str(draw_count)
                    defeat_button.text = 'Поражений: ' + ' ' * (5 - len(str(defeat_count))) + str(defeat_count)
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
        back_button = objects.Button(0, 0, int(100 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'orange',
                                     self.menu_enter, 'back', int(40 * WINDOW_WIDTH / 1536),
                                     int(17 * WINDOW_WIDTH / 1536), int(35 * WINDOW_HEIGHT / 864), 'black')
        login_button = objects.Button(WINDOW_WIDTH // 2 - int(250 * WINDOW_WIDTH / 1536),
                                      WINDOW_HEIGHT // 2 - int(50 * WINDOW_HEIGHT / 864),
                                      int(500 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'white',
                                      self.write_login, 'Ваш логин', int(40 * WINDOW_WIDTH / 1536),
                                      int(10 * WINDOW_WIDTH / 1536), int(35 * WINDOW_HEIGHT / 864), 'black')
        name_button = objects.Button(WINDOW_WIDTH // 2 - int(250 * WINDOW_WIDTH / 1536), int(180 * WINDOW_HEIGHT / 864),
                                     int(500 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'white',
                                     self.nothing, self.name, int(40 * WINDOW_WIDTH / 1536),
                                     (int(500 * WINDOW_WIDTH / 1536) - self.name_caption_width) // 2,
                                     (int(100 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        wins_button = objects.Button(WINDOW_WIDTH // 2 - int(150 * WINDOW_WIDTH / 1536), int(330 * WINDOW_HEIGHT / 864),
                                     int(300 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'white',
                                     self.nothing, 'wins:', int(30 * WINDOW_WIDTH / 1536),
                                     int(30 * WINDOW_WIDTH / 1536), int(40 * WINDOW_HEIGHT / 864), 'black')
        draws_button = objects.Button(WINDOW_WIDTH // 2 - int(150 * WINDOW_WIDTH / 1536),
                                      int(480 * WINDOW_HEIGHT / 864), int(300 * WINDOW_WIDTH / 1536),
                                      int(100 * WINDOW_HEIGHT / 864), 'white', self.nothing, 'draws:',
                                      int(30 * WINDOW_WIDTH / 1536), int(30 * WINDOW_WIDTH / 1536),
                                      int(40 * WINDOW_HEIGHT / 864), 'black')
        defeats_button = objects.Button(WINDOW_WIDTH // 2 - int(150 * WINDOW_WIDTH / 1536),
                                        int(630 * WINDOW_HEIGHT / 864), int(300 * WINDOW_WIDTH / 1536),
                                        int(100 * WINDOW_HEIGHT / 864), 'white', self.nothing, 'defeats:',
                                        int(30 * WINDOW_WIDTH / 1536), int(30 * WINDOW_WIDTH / 1536),
                                        int(40 * WINDOW_HEIGHT / 864), 'black')
        self.unfinished_name = ''
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

            if self.text_enter and self.unfinished_name != '':
                self.name = self.unfinished_name
                name_button.text = self.name
                self.profile_login, self.login = False, False
                self.name_caption = self.font_40.render(self.name, True, BLACK)
                self.name_caption_width = self.name_caption.get_width()
                self.name_caption_height = self.name_caption.get_height()
                name_button.x_text = (int(500 * WINDOW_WIDTH / 1536) - self.name_caption_width) // 2
                name_button.y_text = (int(100 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2
            if self.login:
                login_button.text = self.unfinished_name
            self.screen.fill('green')
            for button in profile_button_list:
                button.draw(self.screen)
            pygame.display.update()

    def game_check(self):
        if self.profile_login:
            self.login_please_caption = True
        else:
            self.game_enter()

    def nothing(self):
        pass

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
            self.text = self.font_500.render(str(self.countdown), True, BLACK)
        self.text_width = self.text.get_width()
        self.text_height = self.text.get_height()
