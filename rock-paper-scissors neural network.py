from numpy import exp, array, dot, zeros, random
import matplotlib.pyplot as plt

"""
1 -- камень
2 -- бумага
3 -- ножницы
"""


def activation(x):
    return 0.5 + 3 / (1 + exp(-x))


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

    bias = 1
    e = 0.5
    a = 0.5

    education_string = [
        "313133211132112223312313122333213213231323131331231131232133322113131313221133213333123313123213331331331332223321",
        "3223122132111333113221132321322132232223311233122313333323321121332223311332312333311331132231131123322133211332311"]
    training_int1 = array([int(i) for i in education_string[0]])  # Костыль, надо исправить
    training_int2 = array([int(i) for i in education_string[1]])  # Костыль, надо исправить
    weights_1 = random.uniform(-3, 3, (3, 6))
    weights_2 = random.uniform(-3, 3, 4)

    grad_w1 = zeros((3, 6))

    pre_delta_w1 = zeros((3, 6))
    pre_delta_w2 = zeros(4)

    h = array([0, 0, 0, bias], dtype=float)

    for j in range(20000):
        for i in range(len(training_int1) - 5):
            input_data = array([training_int1[i], training_int1[i + 1], training_int1[i + 2],
                                training_int1[i + 3], training_int1[i + 4], bias])
            for k in range(3):
                h[k] = activation(dot(weights_1[k], input_data))
            output = activation(dot(h, weights_2))

            delta_out = (output - 0.5) * (7 / 6 - output / 3) * (training_int1[i + 5] - output)
            delta_h = (h - 0.5) * (7 / 6 - h / 3) * (weights_2 * delta_out)
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
        for i in range(len(training_int2) - 5):
            input_data = array([training_int2[i], training_int2[i + 1], training_int2[i + 2],
                                training_int2[i + 3], training_int2[i + 4], bias])
            for k in range(3):
                h[k] = activation(dot(weights_1[k], input_data))
            output = activation(dot(h, weights_2))

            delta_out = (output - 0.5) * (7 / 6 - output / 3) * (training_int2[i + 5] - output)
            delta_h = (h - 0.5) * (7 / 6 - h / 3) * (weights_2 * delta_out)
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
        if j > 19700:
            print(weights_2[0], weights_2[3])

    print(weights_1, weights_2)
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.show()


def test():
    #input_string = "10010101011111111001110000001011101000111100111110100000111111111111110000000000110101010101100110"
    #input_int = array([int(i) for i in input_string])
    bias = 1
    player = bot = draw = 0
    weights_1 = array([[-0.65324095, 0.08473624, -2.75593248, -2.94977803, -4.19452158, -3.96927836],
                       [-4.97214371, 0.76401118, -6.67989925, 0.61377894, -8.08062782, -0.3201619],
                       [-2.28546697, -3.94500862, 6.88317406, -12.64563122, -11.80378841, 1.59190351]])
    weights_2 = array([-2.46409999, 0.81389463, 1.76516013, -0.63625594])
    h = array([0, 0, 0, bias], dtype=float)
    input_data = []

    for i in range(5):
        a = input()
        if a == "k":
            player_move = 1
        elif a == "b":
            player_move = 2
        else:
            player_move = 3
        input_data.append(player_move)
        output = random.randint(1, 3)
        if output == 1:
            bot_move = "k"
        elif output == 2:
            bot_move = "b"
        else:
            bot_move = "n"

        if player_move == output:
            print(bot_move, "Ничья!")
        elif player_move == 2:
            if output > player_move:
                print(bot_move, "Победил бот")
            else:
                print(bot_move, "Победил игрок")
        elif player_move == 1:
            if output == 2:
                print(bot_move, "Победил бот")
            else:
                print(bot_move, "Победил игрок")
        else:
            if output == 1:
                print(bot_move, "Победил бот")
            else:
                print(bot_move, "Победил игрок")

    input_data.append(bias)
    for i in range(50):
        player_data = input()
        if player_data == "k":
            player_move = 1
        elif player_data == "b":
            player_move = 2
        else:
            player_move = 3

        for k in range(3):
            h[k] = activation(dot(weights_1[k], input_data))
        output = activation(dot(h, weights_2))
        output = round_to(output)

        if output == 1:
            bot_move = "k"
        elif output == 2:
            bot_move = "b"
        else:
            bot_move = "n"

        if player_move == output:
            draw += 1
            print(bot_move, "Ничья!")
        elif player_move == 2:
            if output > player_move:
                bot += 1
                print(bot_move, "Победил бот")
            else:
                player += 1
                print(bot_move, "Победил игрок")
        elif player_move == 1:
            if output == 2:
                bot += 1
                print(bot_move, "Победил бот")
            else:
                player += 1
                print(bot_move, "Победил игрок")
        else:
            if output == 1:
                bot += 1
                print(bot_move, "Победил бот")
            else:
                player += 1
                print(bot_move, "Победил игрок")
        for j in range(4):
            print(input_data)
            input_data[j] = input_data[j + 1]
        input_data[4] = player_move
    print(bot / 50, player / 50, draw / 50)


if __name__ == "__main__":
    test()
