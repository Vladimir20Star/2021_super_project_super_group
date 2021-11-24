from numpy import exp, array, dot, zeros, random
import matplotlib.pyplot as plt


def sigmoid(x):
    return 1 / (1 + exp(-x))


def learning():
    x = []
    y1 = []
    y2 = []

    bias = 1
    e = 0.7
    a = 0.3

    education_string = "1010100001010101001101001010010111101001011101000100101010010010101000100000101010101000010101101111110101010110100101010100101001001010010101010101010101001011001010110010101001010101010110100010101001010110101010101101010101010101010101001101"
    training_int = array([int(i) for i in education_string])
    weights_1 = random.uniform(-3, 3, (3, 6))
    weights_2 = random.uniform(-3, 3, 4)

    grad_w1 = zeros((3, 6))

    pre_delta_w1 = zeros((3, 6))
    pre_delta_w2 = zeros(4)

    h = array([0, 0, 0, bias], dtype=float)

    for j in range(10000):
        for i in range(len(training_int) - 5):
            input_data = array([training_int[i], training_int[i + 1], training_int[i + 2],
                                training_int[i + 3], training_int[i + 4], bias])
            for k in range(3):
                h[k] = sigmoid(dot(weights_1[k], input_data))
            output = sigmoid(dot(h, weights_2))

            delta_out = output * (1 - output) * (training_int[i + 5] - output)
            delta_h = h * (1 - h) * (weights_2 * delta_out)
            grad_w2 = h * delta_out
            delta_w2 = e * grad_w2 + a * pre_delta_w2
            weights_2 += delta_w2
            pre_delta_w2 = delta_w2

            for k in range(3):
                grad_w1[k] = input_data * delta_h[k]
            delta_w1 = e * grad_w1 + pre_delta_w1 * a
            weights_1 += delta_w1
            pre_delta_w1 = delta_w1
        x.append(j)
        y1.append(weights_2[0])
        y2.append(weights_2[3])

    print(weights_1, weights_2)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.show()


def main():
    input_string = "10010101011111111001110000001011101000111100111110100000111111111111110000000000110101010101100110"
    input_int = array([int(i) for i in input_string])
    bias = 1
    true = false = 0
    weights_1 = array([[4.41939358, -10.2474862, 15.19866336, 2.19545558, -13.71447213, 2.68323302],
                       [9.83581491, 12.48304071, 15.54548119, -5.25297232, 14.44165296, -12.16899895],
                       [-5.03273995, -7.17027329, -6.411262, -15.12923394, 27.13865129, -4.47243248]])
    weights_2 = array([1.44701983, -1.18916571, -2.77864101, 1.51096182])
    h = array([0, 0, 0, bias], dtype=float)
    for i in range(len(input_int) - 5):
        input_data = array([input_int[i], input_int[i + 1], input_int[i + 2],
                            input_int[i + 3], input_int[i + 4], bias])
        for k in range(3):
            h[k] = sigmoid(dot(weights_1[k], input_data))
        output = sigmoid(dot(h, weights_2))
        if int(2 * output) == input_int[i + 5]:
            true += 1
        else:
            false += 1
    print(true, false)


if __name__ == "__main__":
    main()
