from grafic import Sections
import pygame


class SuperProject:
    """Главный класс работы программы"""

    def __init__(self):
        """функция создания переменных"""
        self.finished = False  # флаг завершения программы
        self.score_player = 0  # счёт побед игрока
        self.score_bot = 0  # счёт побед бота
        self.last_choices = []  # список последних выборов игрока
        self.last_wins = []  # список последних побед/поражений в виде 1/0


def main():
    pygame.init()
    project = SuperProject()
    sections = Sections()
    sections_sect_list = [sections.menu, sections.game, sections.profile]
    while not project.finished:
        if False in sections.flag_list:
            sections_sect_list[sections.flag_list.index(False)]()
        else:
            project.finished = True
    pygame.quit()


if __name__ == "__main__":
    main()
