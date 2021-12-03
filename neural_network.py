import numpy as np
import matplotlib.pyplot as plt

"""
1 -- камень
2 -- бумага
3 -- ножницы
"""


def activation(x):
    return 0.5 + 1.5 / (1 + np.exp(-x - 2.5)) + 1.5 / (1 + np.exp(-x + 2.5))


def activation_derivative(x):
    var_1 = np.exp(-x - 2.5)
    var_2 = np.exp(-x + 2.5)
    return 1.5 * var_1 / (1 + var_1) ** 2 + 1.5 * var_2 / (1 + var_2) ** 2


def round_to(x):
    if 0.5 <= x <= 1.5:
        return 1
    elif x >= 2.5:
        return 3
    else:
        return 2


def learning():
    x = []
    y1 = []
    y2 = []

    learning_rate = 0.5
    momentum = 0.5
    epochs = 200000

    education_set = [
        "313133211132112223312313122333213213231323131331231131232"
        "133322113131313221133213333123313123213331331331332223321",
        "322312213211133311322113232132213223222331123312231333332"
        "3321121332223311332312333311331132231131123322133211332311"]

    weights_1 = np.random.uniform(-1, 1, (3, 5))
    weights_2 = np.random.uniform(-1, 1, (1, 3))
    b1 = np.random.uniform(-1, 1, (3, 1))
    b2 = np.random.uniform(-1, 1)

    pre_delta_w1 = np.zeros((3, 5))

    pre_delta_w2 = np.zeros((1, 3))

    pre_delta_b1 = np.zeros((3, 1))

    pre_delta_b2 = 0

    for epoch in range(epochs):
        for training_str in education_set:
            training_int = np.array([int(i) for i in training_str])
            for iteration in range(len(training_int) - 5):
                input_data = np.array([training_int[iteration], training_int[iteration + 1],
                                       training_int[iteration + 2], training_int[iteration + 3],
                                       training_int[iteration + 4]]).reshape((-1, 1)).reshape((-1, 1))
                inp_h = np.dot(weights_1, input_data) + b1
                h = activation(inp_h)
                s = np.dot(weights_2, h) + b2
                prediction = activation(s)
                grad_prediction = activation_derivative(s) * (training_int[iteration + 5] - prediction)

                grad_w2 = (grad_prediction * h).T
                delta_w2 = grad_w2 * learning_rate + pre_delta_w2 * momentum
                grad_b2 = grad_prediction
                delta_b2 = grad_b2 * learning_rate + pre_delta_b2 * momentum

                grad_h = activation_derivative(inp_h)
                grad_w1 = grad_prediction * (np.dot(input_data, (weights_2 * grad_h.T))).T
                delta_w1 = grad_w1 * learning_rate + pre_delta_w1 * momentum
                grad_b1 = grad_prediction * (weights_2.reshape((-1, 1)) * grad_h)
                delta_b1 = grad_b1 * learning_rate + pre_delta_b1 * momentum

                weights_1 += delta_w1
                weights_2 += delta_w2
                b1 += delta_b1
                b2 += delta_b2

                pre_delta_w1 = delta_w1
                pre_delta_w2 = delta_w2
                pre_delta_b1 = delta_b1
                pre_delta_b2 = delta_b2
        x.append(epoch)
        y1.append(weights_2[0][0])
        y2.append(weights_2[0][2])

    print(weights_1, weights_2, b1, b2)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.show()


def predicting(input_list):
    weights_1 = np.array([[-21.13164301, -1.37054036, -16.86976406, 29.30538071, -34.47326956],
                          [48.60277746, -40.69339409, 23.70495276, -50.88796299, -48.15155281],
                          [15.25138701, -14.91345246, -21.40183576, -13.08390208, 10.26623152]])
    weights_2 = np.array([[1.69228692, 1.68394246, 1.9765986]])
    b1 = np.array([[10.03311103],
                   [16.75359252],
                   [-11.22556562]])
    b2 = [[-2.93831495]]
    previous_moves = np.array([[i] for i in input_list])

    h = activation(np.dot(weights_1, previous_moves) + b1)
    prediction = activation(np.dot(weights_2, h) + b2)
    prediction = round_to(prediction)
    return prediction


if __name__ == "__main__":
    learning()
    print("Этот модуль не запускается отдельно.")
