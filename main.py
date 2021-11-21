# import grafic.py разблокировать когда будет готов файл grafic.py

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
    project = SuperProject()
#    menu()
    while not project.finished:
        pass


if __name__ == "__main__":
    main()
