import grafic
import pygame
import neural_network

sections = grafic.Sections()
neuron = neural_network.NeuralNetwork()


class Project:
    """Главный класс работы программы"""

    def __init__(self):
        """функция создания переменных"""
        self.finished = False  # флаг завершения программы
        self.win_score_player = None  # счёт побед игрока
        self.draw_score_player = None  # счёт ничей игрока
        self.defeat_score_player = None  # счёт поражений игрока
        self.last_choices = [1, 2, 3, 1, 3]  # список последних выборов игрока

    def updating_last_choices(self, new_choice):
        """обновление списка последних ходов игрока"""
        for i in range(4):
            self.last_choices[i] = self.last_choices[i + 1]
        self.last_choices[4] = new_choice

    def game(self):
        """метод одной итерации игры"""
        neuron.predicting(self.last_choices)
        player_figure, result = sections.game(neural_network.round_to(neuron.prediction), self.win_score_player,
                                              self.draw_score_player,
                                              self.defeat_score_player)
        if player_figure != 0:  # проверяем сыграл ли человек
            self.updating_last_choices(player_figure)
            # обновление очков результатов
            if result == 1:
                self.win_score_player += 1
            elif result == 0:
                self.draw_score_player += 1
            elif result == -1:
                self.defeat_score_player += 1

    def profile(self):
        """метод записи информации профиля"""
        self.win_score_player, self.draw_score_player, self.defeat_score_player = sections.profile(
            self.win_score_player, self.draw_score_player, self.defeat_score_player)


def main():
    pygame.init()
    project = Project()
    with open ('players.txt', 'r') as file:
        file_string = file.read()
        sections.file_list = file_string.split('\n')
    while not project.finished:
        if not sections.menu_finished:
            sections.menu()
        elif not sections.profile_finished:
            project.profile()
        elif not sections.game_finished:
            project.game()
        else:
            project.finished = True
    pygame.quit()


if __name__ == "__main__":
    main()
