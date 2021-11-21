from numpy import exp, array, dot


class Neyro01:
    """Нейрон, который угадывает цифру (0 или 1) исходя из последних 5 введенных цифр (0 или 1)"""
    def __init__(self):
        # берём веса по умолчанию (Сани)
        self.synaptic_weights = array([[6.274396785525139, 2.8022563714880935,
                                        1.7770268109380134, 3.5934672966388255, -8.614772205388231]]).T

    def neyro(self, neyro_set_inputs):
        """Формула для работы нейрона"""
        return 1 / (1 + exp(-dot(neyro_set_inputs, self.synaptic_weights) + array([[5]])))

    def start_weights_txt(self):
        """Достаёт начальные веса из файла 'weight.txt'"""
        e = [0, 0, 0, 0, 0]
        with open('weight.txt') as input_file:
            counter = 0
            for line in input_file:
                line = line.strip()
                e[counter] = float(line)
                counter += 1
            self.synaptic_weights = array([[e[0], e[1], e[2], e[3], e[4]]])

    def education(self):
        """Обучение:"""
        # Строчки для тренировки (использовал Саню)
        # Мой, не используется для обучения, но пусть будет на всякий случай
        # training = "0110001110100101111001011001010101010100011111001110" \
        #            "00111101001110110111011011010010101110010110100101110"

        # Саня, на нём работают эти коэффициеты
        training = "0110001001110100110101010010101010010101010101010010" \
                   "10101011101010010101010100110010000101010101010101000"

        training_int = [int(i) for i in training]  # перевод строки в последовательность цифр
        for num in range(10):  # итерация обучения
            for iteration in range(100000):
                print(num, ") ", 100 * iteration // 100000)  # выводит процент от обучения
                for i in range(len(training) - 5):
                    training_set_inputs = array([[training_int[i], training_int[i + 1],
                                                  training_int[i + 2], training_int[i + 3], training_int[i + 4]]])
                    training_set_outputs = array([[training_int[i + 5]]])
                    output = self.neyro(training_set_inputs)
                    self.synaptic_weights = dot(training_set_inputs.T, (training_set_outputs - output) * output * (
                                1 - output)) + self.synaptic_weights
            # Запись весов в файл после 100000 обучений
            with open('weight.txt', 'w') as out_file:
                for i in range(5):
                    print(self.synaptic_weights[i][0], file=out_file)

    def change(self, last_choice, next_1):
        """Обновляет последние введенные цифры (добавляет новую)"""
        for i in range(4):
            last_choice[i] = last_choice[i + 1]
        last_choice[4] = next_1
        return last_choice

    def online_game(self):
        """Ввод цифр по одной, каждый раз выводит предсказание (первые 5 угадываний рандомные, дальше норм)"""
        last = [0, 0, 0, 0, 0]  # список последних пяти цифр, изначально нули (поэтому первые пять по сути рандом)
        true = 0  # переменные подсчёта угаданных/неугаданных ответов neyro
        false = 0
        turns = int(input("Сколько раз хотите сыграть: "))

        for _ in range(turns):
            input_player = int(input("Ваш:"))
            # если нейрон выдаёт < 0.5, то ответ 0, иначе ответ 1
            neyro_answer = int(2 * self.neyro(array([[last[0], last[1], last[2], last[3], last[4]]])))
            print("наверное: ", neyro_answer)
            if neyro_answer == input_player:
                true += 1
                print("Угадал!")
            else:
                false += 1
                print("Не угадал(")
            last = self.change(last, input_player)
        print(true, false)
        print("neyro угадал ", 100 * true / (true + false), "% цифр")

    def offline_game(self):
        # первые строчки классические, полежат здесь, чтобы если что проверить работу
        # input_player = "110101010001010100101001001010110101010101011000100" \
        #                "100101010101101001010010010110101010100100101101010010"  # Саня
        # input_player = "100101010111111110011100000010111010001111001111101" \
        #                "00000111111111111110000000000110101010101100110"  # сломало

        # строчка ввода чисел
        input_player = input("Введите строку из нулей и единиц: ")
        input_player_int = [int(i) for i in input_player]

        true = 0  # переменные подсчёта угаданных/неугаданных ответов neyro
        false = 0

        for i in range(len(input_player) - 5):
            set_inputs = array([[input_player_int[i], input_player_int[i + 1], input_player_int[i + 2],
                                 input_player_int[i + 3], input_player_int[i + 4]]])  # предыдущие пять цифр из ввода
            set_outputs = array([[input_player_int[i + 5]]])  # правильный ответ
            output = self.neyro(set_inputs)
            if int(2 * output) == set_outputs:
                true += 1
            else:
                false += 1
        print(true, false)
        print("neyro угадал ", 100 * true / (true + false), "% цифр")
