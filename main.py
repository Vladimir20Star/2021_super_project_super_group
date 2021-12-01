import grafic
import pygame
import neural_network

sections = grafic.Sections()


class Project:
    """Главный класс работы программы"""

    def __init__(self):
        """функция создания переменных"""
        self.finished = False  # флаг завершения программы
        self.win_score_player = 0  # счёт побед игрока
        self.draw_score_player = 0  # счёт ничей игрока
        self.defeat_score_player = 0  # счёт поражений игрока
        self.last_choices = [1, 2, 3, 2, 1]  # список последних выборов игрока

    def updating_last_choices(self, new_choice):
        """обновление списка последних ходов игрока"""
        for i in range(4):
            self.last_choices[i] = self.last_choices[i + 1]
        self.last_choices[4] = new_choice

    def game(self):
        """метод одной итерации игры"""
        bot_choice = neural_network.predicting(self.last_choices)
        player_figure, result = sections.game(bot_choice, self.win_score_player, self.draw_score_player,
                                              self.defeat_score_player)
        self.updating_last_choices(player_figure)
        # обновление очков результатов
        if result == 1:
            self.win_score_player += 1
        elif result == 0:
            self.draw_score_player += 1
        elif result == -1:
            self.defeat_score_player += 1


def main():
    pygame.init()
    project = Project()
    sections_sect_list = [sections.menu, sections.profile]
    while not project.finished:
        if False in sections.flag_list:
            sections_sect_list[sections.flag_list.index(False)]()
        elif not sections.game_finished:
            project.game()
        else:
            project.finished = True
    pygame.quit()


if __name__ == "__main__":
    main()
