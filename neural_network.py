import numpy as np
import matplotlib.pyplot as plt
import json

"""
1 -- камень
2 -- бумага
3 -- ножницы
"""


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def round_to(x):
    if 0.5 <= x <= 1.5:
        return 1
    elif x >= 2.5:
        return 3
    else:
        return 2


class NeuralNetwork:
    def __init__(self):
        with open("weights.json", "r") as file:
            json_loads = json.load(file)

        self.weights_1 = np.asarray(json_loads["weights_1"])
        self.weights_2 = np.asarray(json_loads["weights_2"])
        self.b1 = np.asarray(json_loads["b1"])
        self.b2 = np.asarray(json_loads["b2"])

        self.input_h = self.h = np.zeros((3, 1))
        self.s = self.prediction = np.zeros((1, 1))

        self.learning_rate = 0.5
        self.momentum = 0.5
        self.epochs = 20000

    @staticmethod
    def activation(x):
        return 0.5 + 1.5 / (1 + np.exp(-x - 3)) + 1.5 / (1 + np.exp(-x + 3))

    @staticmethod
    def activation_derivative(x):
        var_1 = np.exp(-x - 3)
        var_2 = np.exp(-x + 3)
        return 1.5 * var_1 / (1 + var_1) ** 2 + 1.5 * var_2 / (1 + var_2) ** 2

    def predicting(self, input_list):
        previous_moves = np.array([[i] for i in input_list])

        self.input_h = np.dot(self.weights_1, previous_moves) + self.b1
        self.h = self.activation(self.input_h)
        self.s = np.dot(self.weights_2, self.h) + self.b2
        self.prediction = round_to(self.activation(self.s))

    def learning(self):
        x = []
        y1 = []
        y2 = []
        y3 = []
        y4 = []

        education_set = [
            "313133211132112223312313122333213213231323131331231131232"
            "133322113131313221133213333123313123213331331331332223321",
            "322312213211133311322113232132213223222331123312231333332"
            "3321121332223311332312333311331132231131123322133211332311"]

        self.weights_1 = np.random.uniform(-1, 1, (3, 5))
        self.weights_2 = np.random.uniform(-1, 1, (1, 3))
        self.b1 = np.random.uniform(-1, 1, (3, 1))
        self.b2 = np.random.uniform(-1, 1, (1, 1))

        pre_delta_w1 = np.zeros((3, 5))
        pre_delta_w2 = np.zeros((1, 3))
        pre_delta_b1 = np.zeros((3, 1))
        pre_delta_b2 = np.zeros((1, 1))

        for epoch in range(self.epochs):
            for training_str in education_set:
                training_int = np.array([int(i) for i in training_str])
                for iteration in range(len(training_int) - 5):
                    input_data = [training_int[iteration + i]for i in range(5)]
                    self.predicting(input_data)
                    input_data = np.asarray(input_data).reshape(-1, 1)

                    grad_prediction = self.activation_derivative(self.s) * (training_int[iteration + 5]
                                                                            - self.prediction)
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
            x.append(epoch)
            y1.append(self.weights_1[0][0])
            y2.append(self.weights_2[0][0])
            y3.append(self.b1[0][0])
            y4.append(self.b2[0][0])
            if epoch % 1000 == 0:
                print("Эпоха №" + str(epoch))

        with open("weights.json", "w") as file:
            json.dump({'weights_1': self.weights_1, 'weights_2': self.weights_2, 'b1': self.b1, 'b2': self.b2},
                      file, cls=NumpyEncoder, indent=4)

        plt.plot(x, y1)
        plt.plot(x, y2)
        plt.plot(x, y3)
        plt.plot(x, y4)
        plt.show()


if __name__ == "__main__":
    neuron = NeuralNetwork()
    neuron.learning()
    print("Этот модуль не запускается отдельно.")
