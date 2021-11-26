import pygame
from objects import Button, Figure


class Sections:
    def __init__(self):
        self.menu_finished = False
        self.game_finished = True
        self.profile_finished = True
        self.flag_list = [self.menu_finished, self.game_finished, self.profile_finished]
        self.FPS = 60
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def menu(self):
        pygame.display.update()
        clock = pygame.time.Clock()
        game_button = Button(300, 400, 100, 100, 'red', self.game_enter, 'game', 20, 30, 40, 'black')
        profile_button = Button(600, 400, 100, 100, 'cyan', self.profile_enter, 'profile', 20, 30, 40, 'black')
        exit_button = Button(900, 400, 100, 100, 'blue', self.total_exit, 'exit', 20, 30, 40, 'black')
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

    def game(self):
        pygame.display.update()
        clock = pygame.time.Clock()
        game_sprites = pygame.sprite.Group()
        back_button = Button(0, 0, 100, 100, 'purple', self.menu_enter, 'back', 20, 30, 40, 'black')
        human_rock = Figure(540, 600, 117, 172, 'Камень человека.gif', game_sprites, 710, 400)
        human_scissors = Figure(710, 600, 117, 172, 'Ножницы человека.gif', game_sprites, 710, 400)
        human_paper = Figure(880, 600, 117, 172, 'Бумага человека.gif', game_sprites, 710, 400)
        figure_list = [human_rock, human_scissors, human_paper]
        game_button_list = [back_button]
        while not self.game_finished:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.menu_enter()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in game_button_list:
                        button.click(event)
                    for figure in figure_list:
                        figure.click(event)
            for figure in figure_list:
                if figure.move_flag:
                    figure.move()
            self.screen.fill('pink')
            for button in game_button_list:
                button.draw(self.screen)
            game_sprites.draw(self.screen)
            pygame.display.update()

    def profile(self):
        pygame.display.update()
        clock = pygame.time.Clock()
        self.profile_finished = False
        back_button = Button(0, 0, 100, 100, 'orange', self.menu_enter, 'back', 20, 30, 40, 'black')
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
