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


def statistics_draw(win_count, draw_count, defeat_count, win_button, draw_button, defeat_button):
    """
    Присваивание текстов кнопкам вывода статистики (используется класс кнопок с функцией do_nothing)

    :param win_count: количество побед игрока
    :param draw_count: количество ничей игрока
    :param defeat_count: количество поражений игрока
    :param win_button: объект вывода текста побед игрока
    :param draw_button: объект вывода текста ничей игрока
    :param defeat_button: объект вывода текста поражений игрока
    """
    game_counts = win_count + draw_count + defeat_count
    if game_counts == 0:
        win_button.text = 'Побед: ' + ' ' * (13 - len(str(win_count))) + str(win_count)
        draw_button.text = 'Ничьи: ' + ' ' * (14 - len(str(draw_count))) + str(draw_count)
        defeat_button.text = 'Поражений: ' + ' ' * (5 - len(str(defeat_count))) + str(defeat_count)
    else:
        win_button.text = 'Побед: ' + ' ' * (13 - len(str(win_count))) + str(win_count) + ' ' * 9 + \
                          str(round(win_count * 100 / game_counts)) + '%'
        draw_button.text = 'Ничьи: ' + ' ' * (14 - len(str(draw_count))) + str(draw_count) + ' ' * 9 + \
                           str(round(draw_count * 100 / game_counts)) + '%'
        defeat_button.text = 'Поражений: ' + ' ' * (5 - len(str(defeat_count))) + str(defeat_count) + \
                             ' ' * 9 + str(100 - round(win_count * 100 / game_counts) -
                                           round(draw_count * 100 / game_counts)) + '%'


class Sections:
    """
    Класс отсеков игры (menu, game, profile) и их составляющих
    """

    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        (self.menu_finished, self.game_finished, self.game_again, self.profile_finished, self.login,
         self.profile_login, self.time_end_flag, self.figures_active, self.text_enter, self.login_please_caption,
         self.login_in_file) = False, True, False, True, False, True, False, True, False, False, False
        (self.font_500, self.font_350, self.font_50, self.font_40) = \
            (pygame.font.Font(None, int(500 * WINDOW_WIDTH / 1536)),
             pygame.font.Font(None, int(350 * WINDOW_WIDTH / 1536)),
             pygame.font.Font(None, int(50 * WINDOW_WIDTH / 1536)),
             pygame.font.Font(None, int(40 * WINDOW_WIDTH / 1536)))
        self.flag_list = [self.menu_finished, self.profile_finished]
        self.FPS = 60
        self.countdown_time = self.click_time = time.time()
        self.human_figure = self.final_human_figure = self.bot_figure = self.countdown = self.player_index = 0
        self.game_sprites = pygame.sprite.Group()
        self.name = self.unfinished_name = ''
        self.file_list = []
        (self.text, self.login_please, self.name_caption) = \
            (self.font_500.render('', True, BLACK),
             self.font_50.render('Пожалуйста, введите логин в разделе profile.', True, BLACK),
             self.font_50.render(self.name, True, BLACK))
        (self.text_width, self.text_height, self.login_please_width, self.login_please_height, self.name_caption_width,
         self.name_caption_height) = (self.text.get_width(), self.text.get_height(), self.login_please.get_width(),
                                      self.login_please.get_height(), self.name_caption.get_width(),
                                      self.name_caption.get_height())

    def text_in(self, num):
        """
        Ввод текста с клавиатуры

        :param num: pygame.event
        """
        russuans_letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
        self.text_enter = False
        if num.key == pygame.K_RETURN:
            self.text_enter = True
        elif num.key == pygame.K_BACKSPACE:
            self.unfinished_name = self.unfinished_name[:-1]
        elif len(self.unfinished_name) < 20 and num.unicode != '$' and num.unicode not in russuans_letters:
            self.unfinished_name += num.unicode

    def menu_buttons_init(self):
        """
        Определение кнопок меню

        :return: кнопка секции game, кнопка секции profile,  кнопка выхода
        """
        game_button = objects.Button(WINDOW_WIDTH // 2 - int(400 * WINDOW_WIDTH / 1536),
                                     WINDOW_HEIGHT // 2 - int(75 * WINDOW_HEIGHT / 864), int(150 * WINDOW_WIDTH / 1536),
                                     int(150 * WINDOW_HEIGHT / 864), 'red', self.game_check, 'game',
                                     int(40 * WINDOW_WIDTH / 1536), int(35 * WINDOW_WIDTH / 1536),
                                     int(60 * WINDOW_HEIGHT / 864), 'black')
        profile_button = objects.Button(WINDOW_WIDTH // 2 - int(75 * WINDOW_WIDTH / 1536),
                                        WINDOW_HEIGHT // 2 - int(75 * WINDOW_HEIGHT / 864),
                                        int(150 * WINDOW_WIDTH / 1536), int(150 * WINDOW_HEIGHT / 864), 'cyan',
                                        self.profile_enter, 'profile', int(40 * WINDOW_WIDTH / 1536),
                                        int(30 * WINDOW_WIDTH / 1536), int(60 * WINDOW_HEIGHT / 864), 'black')
        exit_button = objects.Button(WINDOW_WIDTH // 2 + int(275 * WINDOW_WIDTH / 1536),
                                     WINDOW_HEIGHT // 2 - int(75 * WINDOW_HEIGHT / 864), int(150 * WINDOW_WIDTH / 1536),
                                     int(150 * WINDOW_HEIGHT / 864), 'yellow', self.total_exit, 'exit',
                                     int(40 * WINDOW_WIDTH / 1536), int(50 * WINDOW_WIDTH / 1536),
                                     int(60 * WINDOW_HEIGHT / 864), 'black')
        return game_button, profile_button, exit_button

    def menu(self):
        """Главный метод секции menu"""
        pygame.display.update()
        clock = pygame.time.Clock()
        game_button, profile_button, exit_button = self.menu_buttons_init()
        self.login_please_caption = False
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
            if self.login_please_caption:
                self.screen.blit(self.login_please, ((WINDOW_WIDTH - self.login_please_width) // 2,
                                                     (WINDOW_HEIGHT - self.login_please_height * 10) // 2))
            pygame.display.update()

    def game_active_buttons_init(self):
        """
        Определение скелетных кнопок секции game (back_button, start_button)

        :return: кнопка выхода в меню, кнопка старта
        """
        back_button = objects.Button(0, 0, int(100 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'purple',
                                     self.menu_enter, 'back', int(40 * WINDOW_WIDTH / 1536),
                                     int(17 * WINDOW_WIDTH / 1536), int(35 * WINDOW_HEIGHT / 864), 'black')
        start_button = objects.Button(0, WINDOW_HEIGHT * 2 // 3 - int(50 * WINDOW_HEIGHT / 864),
                                      int(100 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'purple',
                                      self.game_restart, 'start', int(40 * WINDOW_WIDTH / 1536),
                                      int(16 * WINDOW_WIDTH / 1536), int(35 * WINDOW_HEIGHT / 864), 'black')
        return back_button, start_button

    def game_names_and_pictures_buttons_init(self):
        """
        Определение кнопок вывода имени игрока, имени Скалы и фигуры вывода фото Скалы

        :return: кнопка вывода имени игрока, кнопка вывода 'The Rock', фигура вывода фото Скалы
        """
        name_button = objects.Button(WINDOW_WIDTH // 2 - int(259 * WINDOW_WIDTH / 1536), int(814 * WINDOW_HEIGHT / 864),
                                     int(517 * WINDOW_WIDTH / 1536), int(40 * WINDOW_HEIGHT / 864), 'green',
                                     self.nothing, self.name, int(40 * WINDOW_WIDTH / 1536),
                                     (int(517 * WINDOW_WIDTH / 1536) - self.name_caption_width) // 2,
                                     (int(44 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        the_rock_name_button = objects.Button(WINDOW_WIDTH // 2 - int(100 * WINDOW_WIDTH / 1536),
                                              int(220 * WINDOW_HEIGHT / 864), int(200 * WINDOW_WIDTH / 1536),
                                              int(40 * WINDOW_HEIGHT / 864), 'red', self.nothing, 'The Rock',
                                              int(40 * WINDOW_WIDTH / 1536), int(38 * WINDOW_WIDTH / 1536),
                                              (int(44 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        the_rock = objects.Figure(WINDOW_WIDTH // 2 - int(100 * WINDOW_WIDTH / 1536), int(10 * WINDOW_HEIGHT / 864),
                                  int(200 * WINDOW_WIDTH / 1536), int(200 * WINDOW_HEIGHT / 864), 'Скала.jpg',
                                  self.game_sprites, FIGURE_H_END_X, FIGURE_H_END_Y)
        return name_button, the_rock_name_button, the_rock

    def game_statistics_buttons_init(self, win_count, draw_count, defeat_count):
        """
        Определение кнопок вывода статистики игрока

        :param win_count: количество побед игрока
        :param draw_count: количество ничей игрока
        :param defeat_count: количество поражений игрока
        :return: кнопка вывода текста победы, кнопка вывода текста ничьей, кнопка вывода текста поражения
        """
        win_button = objects.Button(WINDOW_WIDTH - int(420 * WINDOW_WIDTH / 1536), int(10 * WINDOW_HEIGHT / 864),
                                    int(410 * WINDOW_WIDTH / 1536), int(40 * WINDOW_HEIGHT / 864), 'green',
                                    self.nothing, '', int(40 * WINDOW_WIDTH / 1536), int(6 * WINDOW_WIDTH / 1536),
                                    (int(44 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        draw_button = objects.Button(WINDOW_WIDTH - int(420 * WINDOW_WIDTH / 1536), int(60 * WINDOW_HEIGHT / 864),
                                     int(410 * WINDOW_WIDTH / 1536), int(40 * WINDOW_HEIGHT / 864), 'yellow',
                                     self.nothing, '', int(40 * WINDOW_WIDTH / 1536), int(6 * WINDOW_WIDTH / 1536),
                                     (int(44 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        defeat_button = objects.Button(WINDOW_WIDTH - int(420 * WINDOW_WIDTH / 1536), int(110 * WINDOW_HEIGHT / 864),
                                       int(410 * WINDOW_WIDTH / 1536), int(40 * WINDOW_HEIGHT / 864), 'red',
                                       self.nothing, '', int(40 * WINDOW_WIDTH / 1536), int(6 * WINDOW_WIDTH / 1536),
                                       (int(44 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        statistics_draw(win_count, draw_count, defeat_count, win_button, draw_button, defeat_button)
        return win_button, draw_button, defeat_button

    def game_figure_buttons_init(self):
        """
        Определение фигур, используемых человеком

        :return: фигура камня игрока, фигура ножниц игрока, фигура бумаги игрока
        """
        human_rock = objects.Figure(FIGURE_H_CEN_X - int(200 * WINDOW_WIDTH / 1536), FIGURE_H_Y, FIGURE_H_WIDTH,
                                    FIGURE_H_HEIGHT, 'Камень человека.gif', self.game_sprites, FIGURE_H_END_X,
                                    FIGURE_H_END_Y)
        human_scissors = objects.Figure(FIGURE_H_CEN_X, FIGURE_H_Y, FIGURE_H_WIDTH, FIGURE_H_HEIGHT,
                                        'Ножницы человека.gif', self.game_sprites, FIGURE_H_END_X, FIGURE_H_END_Y)
        human_paper = objects.Figure(FIGURE_H_CEN_X + int(200 * WINDOW_WIDTH / 1536), FIGURE_H_Y, FIGURE_H_WIDTH,
                                     FIGURE_H_HEIGHT, 'Бумага человека.gif', self.game_sprites, FIGURE_H_END_X,
                                     FIGURE_H_END_Y)
        return human_rock, human_scissors, human_paper

    def game_bot_figure_image_init(self):
        """
        Определение фигуры, которую выведет бот

        :return: сыгранная ботом фигура
        """
        if self.bot_figure == 1:
            fullname = os.path.join('img', 'Камень бота.gif')
        elif self.bot_figure == 2:
            fullname = os.path.join('img', 'Бумага бота.gif')
        else:
            fullname = os.path.join('img', 'Ножницы бота.gif')
        image = pygame.image.load(fullname).convert()
        color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        bot_figure_image = pygame.transform.scale(image, (FIGURE_B_WIDTH, FIGURE_B_HEIGHT))
        return bot_figure_image

    def game_variables_init(self):
        """
        Переопределяем переменные перед началом нового цикла (game() == 1 цикл игры)
        """
        self.game_sprites = pygame.sprite.Group()
        self.time_end_flag, self.game_again, self.figures_active = False, False, True
        self.human_figure = 0
        self.countdown = 5
        self.countdown_time = time.time()
        (self.text, self.name_caption) = (self.font_500.render(str(self.countdown), True, BLACK),
                                          self.font_40.render(self.name, True, BLACK))
        (self.text_width, self.text_height, self.name_caption_width, self.name_caption_height) = \
            (self.text.get_width(), self.text.get_height(), self.name_caption.get_width(),
             self.name_caption.get_height())

    def game_determining_outcome(self, win_count, draw_count, defeat_count):
        """
        Функция определения результата игры

        :param win_count: количество побед игрока
        :param draw_count: количество ничей игрока
        :param defeat_count: количество поражений игрока
        :return: результат (1 - победа, 0 - ничья, -1 - победа, если не сыграно то без разницы),
        количество побед, количество ничей, количество поражений
        """
        result = 0  # по умолчанию ничья
        if self.human_figure == 0:
            self.text = self.font_350.render('Не сыграно!', True, BLACK)
        elif (self.human_figure, self.bot_figure) in [(3, 1), (1, 2), (2, 3)]:
            self.text = self.font_350.render('Поражение!', True, BLACK)
            result = -1
            defeat_count += 1
        elif (self.human_figure, self.bot_figure) in [(2, 1), (3, 2), (1, 3)]:
            self.text = self.font_350.render('Победа!', True, BLACK)
            result = 1
            win_count += 1
        else:
            self.text = self.font_350.render('Ничья!', True, BLACK)
            draw_count += 1
        return result, win_count, draw_count, defeat_count

    def game_choice_processing(self, figure_list, figure):
        """
        Метод, переобозначающий, какая фигура выбрана

        :param figure_list: список всех фигур человека
        :param figure: выбранная человеком фигура
        """
        if self.time_end_flag:  # если время вышло
            if self.human_figure == 0:
                self.human_figure = figure_list.index(figure) + 1
                for fig in figure_list:
                    fig.active = False
            else:
                figure.move_flag = False
                figure.image.set_colorkey((255, 0, 0))  # возвращает фон, невыбранной фигуры
        else:  # если ещё время осталось
            self.human_figure = figure_list.index(figure) + 1
            for fig in figure_list:
                if fig != figure:
                    fig.move_flag = False
                    fig.image.set_colorkey((255, 0, 0))  # возвращает фон, невыбранной фигуры

    def game_events_processing(self, game_button_list, figure_list):
        """
        Обработка событий в секции game

        :param game_button_list: список кнопок секции game
        :param figure_list: список фигур игрока
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.menu_enter()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in game_button_list:
                    if button.text == 'start':
                        if self.time_end_flag:
                            button.click(event)
                    else:
                        button.click(event)
                for figure in figure_list:
                    if figure.active:
                        if figure.move_flag:
                            continue
                        figure.click(event)
                        if figure.move_flag:
                            self.game_choice_processing(figure_list, figure)
                            break

    def game_final_processing(self, figure_list, result, win_count, draw_count, defeat_count, win_button, draw_button,
                              defeat_button, bot_figure_image):
        """
        Обработка результатов одного цикла секции game

        :param figure_list: список фигур игрока
        :param result: результат (на входе ещё стоит 0 по умолчанию)
        :param win_count: количество побед
        :param draw_count: количество ничей
        :param defeat_count: количество поражений
        :param win_button: кнопка вывода текста победы
        :param draw_button: кнопка вывода текста ничьей
        :param defeat_button: кнопка вывода текста поражения
        :param bot_figure_image: изображение фигуры, которую сыграл бот
        :return: результат (1 - победа, 0 - ничья, -1 - победа, если не сыграно то без разницы)
        """
        if self.figures_active:
            for figure in figure_list:
                figure.active = False
            result, win_count, draw_count, defeat_count = \
                self.game_determining_outcome(win_count, draw_count, defeat_count)
            self.text_width = self.text.get_width()
            self.text_height = self.text.get_height()
            self.figures_active = False
            self.final_human_figure = self.human_figure
            statistics_draw(win_count, draw_count, defeat_count, win_button, draw_button, defeat_button)
        if self.human_figure != 0:
            self.screen.blit(bot_figure_image, (FIGURE_B_X, FIGURE_B_Y))
        return result

    def game_cycle_draw_objects(self, game_button_list):
        """
        Прорисовка объектов секции game во время игрового цикла

        :param game_button_list: список объектов секции game
        """
        for button in game_button_list:
            if button.text == 'start':
                if self.time_end_flag:
                    button.draw(self.screen)
            else:
                button.draw(self.screen)
        self.game_sprites.draw(self.screen)
        self.screen.blit(self.text, ((WINDOW_WIDTH - self.text_width) // 2,
                                     (WINDOW_HEIGHT - self.text_height) // 2))

    def game_countdown_processing(self):
        """
        Обработка обратного отсчёта и отслеживание его завершения
        """
        if self.countdown > 0:  # если обратный отсчёт не закончен
            if time.time() - self.countdown_time > 1:
                self.countdown_tick()
                self.countdown_time = time.time()
        elif not self.time_end_flag:
            self.text = self.font_350.render('', True, BLACK)
            self.text_width = self.text.get_width()
            self.text_height = self.text.get_height()
            self.time_end_flag = True
            self.click_time = time.time()

    def game_figure_moving(self, figure_list):
        """
        После завершения отсчёта начинает двигать выбранную игроком фигуру

        :param figure_list: список фигур игрока
        """
        if self.time_end_flag:
            for figure in figure_list:
                if figure.move_flag:
                    figure.move()

    def game_pre_drawing_processing(self, game_button_list, figure_list):
        """
        Обработка всех процессов секции game до вывода результата игры

        :param game_button_list: список кнопок секции game
        :param figure_list: список фигур игрока
        """
        self.game_events_processing(game_button_list, figure_list)
        self.game_figure_moving(figure_list)
        self.game_countdown_processing()

    def game(self, bot_figure, win_count, draw_count, defeat_count):
        """
        Главный метод секции game, собирающий остальные методы в единый алгоритм

        :param bot_figure: номер фигуры, которую покажет бот
        :param win_count: количество побед игрока
        :param draw_count: количество ничей игрока
        :param defeat_count: количество поражений игрока
        :return: ход игрока (1-к, 2-б, 3-н, 0-не сыграно), результат игры
        """
        pygame.display.update()
        clock = pygame.time.Clock()
        self.human_figure = self.final_human_figure = 0
        self.bot_figure = bot_figure
        self.game_variables_init()
        back_button, start_button = self.game_active_buttons_init()
        name_button, the_rock_name_button, the_rock = self.game_names_and_pictures_buttons_init()
        win_button, draw_button, defeat_button = self.game_statistics_buttons_init(win_count, draw_count, defeat_count)
        human_rock, human_scissors, human_paper = self.game_figure_buttons_init()
        figure_list = [human_rock, human_paper, human_scissors]
        game_button_list = [back_button, start_button, name_button, the_rock_name_button, win_button, draw_button,
                            defeat_button]
        result = 0
        bot_figure_image = self.game_bot_figure_image_init()
        while not self.game_finished and not self.game_again:
            clock.tick(self.FPS)
            self.game_pre_drawing_processing(game_button_list, figure_list)
            self.screen.fill('pink')
            if self.time_end_flag and time.time() - self.click_time > 0.5:
                result = self.game_final_processing(figure_list, result, win_count, draw_count, defeat_count,
                                                    win_button, draw_button, defeat_button, bot_figure_image)
            self.game_cycle_draw_objects(game_button_list)
            pygame.display.update()
        return self.final_human_figure, result

    def profile_active_buttons_init(self):
        """
        Определение кнопок выхода в меню и введения логина

        :return: кнопка выхода в меню, кнопка для введения логина
        """
        back_button = objects.Button(0, 0, int(100 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'orange',
                                     self.menu_enter, 'back', int(40 * WINDOW_WIDTH / 1536),
                                     int(17 * WINDOW_WIDTH / 1536), int(35 * WINDOW_HEIGHT / 864), 'black')
        login_button = objects.Button(WINDOW_WIDTH // 2 - int(250 * WINDOW_WIDTH / 1536),
                                      WINDOW_HEIGHT // 2 - int(50 * WINDOW_HEIGHT / 864),
                                      int(500 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'white',
                                      self.write_login, 'Ваш логин', int(40 * WINDOW_WIDTH / 1536),
                                      int(10 * WINDOW_WIDTH / 1536), int(35 * WINDOW_HEIGHT / 864), 'black')
        return back_button, login_button

    def profile_statistics_buttons_init(self):
        """
        Определение кнопок статистики секции profile

        :return: кнопка вывода имени игрока, кнопка вывода количества побед, кнопка вывода количества ничьих,
        кнопка вывода количества поражений
        """
        name_button = objects.Button(WINDOW_WIDTH // 2 - int(250 * WINDOW_WIDTH / 1536), int(180 * WINDOW_HEIGHT / 864),
                                     int(500 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'white',
                                     self.nothing, self.name, int(40 * WINDOW_WIDTH / 1536),
                                     (int(500 * WINDOW_WIDTH / 1536) - self.name_caption_width) // 2,
                                     (int(100 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2, 'black')
        win_button = objects.Button(WINDOW_WIDTH // 2 - int(150 * WINDOW_WIDTH / 1536), int(330 * WINDOW_HEIGHT / 864),
                                    int(300 * WINDOW_WIDTH / 1536), int(100 * WINDOW_HEIGHT / 864), 'white',
                                    self.nothing, '', int(30 * WINDOW_WIDTH / 1536),
                                    int(8 * WINDOW_WIDTH / 1536), int(40 * WINDOW_HEIGHT / 864), 'black')
        draw_button = objects.Button(WINDOW_WIDTH // 2 - int(150 * WINDOW_WIDTH / 1536),
                                     int(480 * WINDOW_HEIGHT / 864), int(300 * WINDOW_WIDTH / 1536),
                                     int(100 * WINDOW_HEIGHT / 864), 'white', self.nothing, '',
                                     int(30 * WINDOW_WIDTH / 1536), int(8 * WINDOW_WIDTH / 1536),
                                     int(40 * WINDOW_HEIGHT / 864), 'black')
        defeat_button = objects.Button(WINDOW_WIDTH // 2 - int(150 * WINDOW_WIDTH / 1536),
                                       int(630 * WINDOW_HEIGHT / 864), int(300 * WINDOW_WIDTH / 1536),
                                       int(100 * WINDOW_HEIGHT / 864), 'white', self.nothing, '',
                                       int(30 * WINDOW_WIDTH / 1536), int(8 * WINDOW_WIDTH / 1536),
                                       int(40 * WINDOW_HEIGHT / 864), 'black')
        return name_button, win_button, draw_button, defeat_button

    def profile_name_processing(self, name_button):
        """
        Доопределяет кнопку вывода имени игрока, задавая имя и координаты текста на основе его размеров

        :param name_button: кнопка вывода имени игрока
        """
        self.name = self.unfinished_name.strip()
        name_button.text = self.name
        self.profile_login, self.login = False, False
        self.name_caption = self.font_40.render(self.name, True, BLACK)
        self.name_caption_width = self.name_caption.get_width()
        self.name_caption_height = self.name_caption.get_height()
        name_button.x_text = (int(500 * WINDOW_WIDTH / 1536) - self.name_caption_width) // 2
        name_button.y_text = (int(100 * WINDOW_HEIGHT / 864) - self.name_caption_height) // 2

    def profile_events_processing(self, profile_button_list):
        """
        Обработка событий в секции profile

        :param profile_button_list: кнопки в секции profile
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.menu_enter()
            elif event.type == pygame.KEYDOWN and self.login:
                self.text_in(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in profile_button_list:
                    button.click(event)

    def profile_data_processing(self):
        """
        Определяет значения побед, ничьих, поражений игрока из файла (если новый логин, то 0,0,0)

        :return: определяет значения: побед игрока, ничьих игрока, поражений игрока
        """
        win_count, draw_count, defeat_count = 0, 0, 0
        for i in range(len(self.file_list)):
            player = self.file_list[i]
            if self.name == player[:player.find('$')]:
                self.player_index = i
                player_list = player.split('$')
                win_count, draw_count, defeat_count = [int(i) for i in [player_list[1], player_list[2],
                                                                        player_list[3]]]
                self.login_in_file = True
                break
        if not self.login_in_file:
            self.file_list.append(self.name + '$0$0$0')
            self.player_index = len(self.file_list) - 1
        return win_count, draw_count, defeat_count

    def profile_counts_processing(self, win_count, draw_count, defeat_count, win_button, draw_button, defeat_button):
        """
        Если победы и тп - None, то обновляет, доставая из файла, иначе выводит статистику а экран

        :param win_count: количество побед игрока
        :param draw_count: количество ничьих игрока
        :param defeat_count: количество поражений игрока
        :param win_button: кнопка вывода количества побед
        :param draw_button: кнопка вывода количества ничьих
        :param defeat_button: кнопка вывода количества поражений
        :return: обновлённые значения (если был None и ввели имя): количество побед игрока, количество ничьих игрока,
        количество поражений игрока
        """
        # None - флаг, что не ввели имя и не записали статистику, если не None, то возращаем без изменения
        if (win_count, draw_count, defeat_count) == (None, None, None):
            if self.name != '':
                win_count, draw_count, defeat_count = self.profile_data_processing()
        else:
            statistics_draw(win_count, draw_count, defeat_count, win_button, draw_button, defeat_button)
        return win_count, draw_count, defeat_count

    def profile(self, win_count, draw_count, defeat_count):
        """
        Главный метод секции profile,

        :param win_count: количество побед игрока
        :param draw_count: количество ничьих игрока
        :param defeat_count: количество поражений игрока
        :return: обновлённые значения (если был None и ввели имя): количество побед игрока, количество ничьих игрока,
        количество поражений игрока
        """
        pygame.display.update()
        clock = pygame.time.Clock()
        self.profile_finished, self.login, self.text_enter = False, False, False
        back_button, login_button = self.profile_active_buttons_init()
        name_button, win_button, draw_button, defeat_button = self.profile_statistics_buttons_init()
        self.unfinished_name = ''
        while not self.profile_finished:
            clock.tick(self.FPS)
            if self.profile_login:  # если ввели логин, то выводится информация про игрока
                profile_button_list = [back_button, login_button]
            else:
                profile_button_list = [back_button, name_button, win_button, draw_button, defeat_button]
            self.profile_events_processing(profile_button_list)
            if self.text_enter and self.unfinished_name.strip() != '':
                self.profile_name_processing(name_button)
            if self.login:
                login_button.text = self.unfinished_name
            win_count, draw_count, defeat_count = self.profile_counts_processing(win_count, draw_count, defeat_count,
                                                                                 win_button, draw_button,
                                                                                 defeat_button)
            self.screen.fill('green')
            for button in profile_button_list:
                button.draw(self.screen)
            pygame.display.update()
        return win_count, draw_count, defeat_count

    def game_check(self):
        """
         Проверка, введён ли логин и вызов секции game
        """
        if self.profile_login:
            self.login_please_caption = True
        else:
            self.game_enter()

    def nothing(self):
        """
        Пустая функция для создания кнопок вывода текста
        """
        pass

    def write_login(self):
        """
        Логин записан
        """
        self.login = True

    def menu_enter(self):
        """
        Вход в секцию menu
        """
        self.menu_finished, self.game_finished, self.profile_finished = False, True, True
        self.flag_list = [self.menu_finished, self.profile_finished]

    def game_enter(self):
        """
        Вход в секцию game
        """
        self.menu_finished, self.game_finished, self.profile_finished, self.game_again = True, False, True, False
        self.flag_list = [self.menu_finished, self.profile_finished]

    def profile_enter(self):
        """
        Вход в секцию
        """
        self.menu_finished, self.game_finished, self.profile_finished = True, True, False
        self.flag_list = [self.menu_finished, self.profile_finished]

    def total_exit(self):
        """
        Выход из программы
        """
        self.menu_finished, self.game_finished, self.profile_finished = True, True, True
        self.flag_list = [self.menu_finished, self.profile_finished]

    def game_restart(self):
        """
        Начало нового цикла секции game
        """
        self.game_again = True

    def countdown_tick(self):
        """
        Обновление обратного отсчёта
        """
        self.countdown -= 1
        if self.countdown > 0:
            self.text = self.font_500.render(str(self.countdown), True, BLACK)
        self.text_width = self.text.get_width()
        self.text_height = self.text.get_height()
