import numpy as np
import matplotlib.pyplot as plt
import json

"""
Модуль, отвечающий за нейросеть
"""


class NumpyEncoder(json.JSONEncoder):
    """
    Класс для перевод numpy.array в json
    """

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def round_to(x):
    """
    Функция, отвечающая за округление до ближайшего целого в пределах (0.5; 3.5)
    """
    if 0.5 <= x <= 1.5:
        return 1
    elif x >= 2.5:
        return 3
    else:
        return 2


class NeuralNetwork:
    """
    Класс нейросети
    """

    def __init__(self):
        with open("data/weights.json", "r") as file:
            json_loads = json.load(file)

        self.weights_1 = np.asarray(json_loads["weights_1"])  # Веса от входных нейронов к первому скрытому слою
        self.weights_2 = np.asarray(json_loads["weights_2"])  # Веса от скрытого слоя к выходному нейрону
        self.b1 = np.asarray(json_loads["b1"])  # Веса нейрона смещения, идущего к скрытому слою
        self.b2 = np.asarray(json_loads["b2"])  # Вес нейрона смещения, идущего к выходному нейрону

        self.input_h = np.zeros((3, 1))  # Вспомогательная переменная, равная значению скрытого слоя до
        # применения функции активации
        self.h = np.zeros((3, 1))   # Значения скрытых нейронов
        self.s = np.zeros((1, 1))  # Вспомогательная переменная, равная значению выходного нейрона
        # до применения функции активации
        self.prediction = np.zeros((1, 1))   # Предсказанное значение, как должен сходить бот

        self.learning_rate = 0.4  # Скорость обучения нейросети
        self.momentum = 0.7  # Момент для метода обратного распространения
        self.epochs = 30000  # Количество эпох обучения

    @staticmethod
    def activation(x):
        """
        Функция активации для нейросети
        """
        return 0.5 + 1.5 / (1 + np.exp(-x * 1.5 - 3)) + 1.5 / (1 + np.exp(-x * 1.5 + 3))

    @staticmethod
    def activation_derivative(x):
        """
        Производная функции активации
        """
        var_1 = np.exp(-x * 1.5 - 3)
        var_2 = np.exp(-x * 1.5 + 3)
        return 1.5 * var_1 * 1.5 / (1 + var_1) ** 2 + 1.5 * var_2 * 1.5 / (1 + var_2) ** 2

    def predicting(self, input_list):
        """
        Работа самой нейросети (по входным данным получает выходное значение)
        """
        previous_moves = np.array([[i] for i in input_list])

        self.input_h = np.dot(self.weights_1, previous_moves) + self.b1
        self.h = self.activation(self.input_h)
        self.s = np.dot(self.weights_2, self.h) + self.b2
        self.prediction = self.activation(self.s)

    def learning(self):
        """
        Обучение нейросети методом обратного распространения
        """
        x1 = []
        x2 = []
        y1 = []
        y2 = []
        y3 = []
        y4 = []
        y21 = []
        error = np.array([[0]])

        file = open("data/education_set.txt", "r")
        education_set = file.readlines()
        file.close()

        self.weights_1 = np.random.uniform(-5, 5, (3, 5))
        self.weights_2 = np.random.uniform(-5, 5, (1, 3))
        self.b1 = np.random.uniform(-5, 5, (3, 1))
        self.b2 = np.random.uniform(-5, 5, (1, 1))

        pre_delta_w1 = np.zeros((3, 5))
        pre_delta_w2 = np.zeros((1, 3))
        pre_delta_b1 = np.zeros((3, 1))
        pre_delta_b2 = np.zeros((1, 1))

        for epoch in range(self.epochs):
            for line in education_set:
                training_int = np.array([int(i) for i in line.rstrip()])

                for iteration in range(len(training_int) - 5):
                    input_data = [training_int[iteration + i] for i in range(5)]
                    self.predicting(input_data)

                    input_data = np.asarray(input_data).reshape(-1, 1)

                    if training_int[iteration + 5] == 1:
                        sample = 2
                    elif training_int[iteration + 5] == 2:
                        sample = 3
                    else:
                        sample = 1

                    error[0][0] += ((self.prediction - sample) ** 2) / 2

                    grad_prediction = self.activation_derivative(self.s) * (sample - self.prediction)

                    grad_w2 = (grad_prediction * self.h).T
                    delta_w2 = grad_w2 * self.learning_rate + pre_delta_w2 * self.momentum
                    grad_b2 = grad_prediction
                    delta_b2 = grad_b2 * self.learning_rate + pre_delta_b2 * self.momentum

                    grad_h = self.activation_derivative(self.input_h)
                    grad_w1 = grad_prediction * (np.dot(input_data, (self.weights_2 * grad_h.T))).T
                    delta_w1 = grad_w1 * self.learning_rate + pre_delta_w1 * self.momentum
                    grad_b1 = grad_prediction * (self.weights_2.reshape((-1, 1)) * grad_h)
                    delta_b1 = grad_b1 * self.learning_rate + pre_delta_b1 * self.momentum

                    self.weights_1 += delta_w1
                    self.weights_2 += delta_w2
                    self.b1 += delta_b1
                    self.b2 += delta_b2

                    pre_delta_w1 = delta_w1
                    pre_delta_w2 = delta_w2
                    pre_delta_b1 = delta_b1
                    pre_delta_b2 = delta_b2
            x1.append(epoch)
            y1.append(self.weights_1[0][0])
            y2.append(self.weights_2[0][0])
            y3.append(self.b1[0][0])
            y4.append(self.b2[0][0])
            x2.append(epoch)
            y21.append(error[0][0])
            error = np.array([[0]])

            if epoch % 1000 == 0:
                print("Эпоха №" + str(epoch))

        with open("data/weights.json", "w") as file:
            json.dump({'weights_1': self.weights_1, 'weights_2': self.weights_2, 'b1': self.b1, 'b2': self.b2},
                      file, cls=NumpyEncoder, indent=4)

        plt.plot(x1, y1)
        plt.plot(x1, y2)
        plt.plot(x1, y3)
        plt.plot(x1, y4)
        plt.show()
        plt.plot(x2, y21)
        plt.show()


if __name__ == "__main__":
    neuron = NeuralNetwork()
    neuron.learning()
    print("Этот модуль не запускается отдельно.")
