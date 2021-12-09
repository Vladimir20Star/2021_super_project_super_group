from neural_network import NeuralNetwork, round_to

neyro = NeuralNetwork()

uno = 0
dos = 0
tres = 0
for i_1 in range(1, 4):
    for i_2 in range(1, 4):
        for i_3 in range(1, 4):
            for i_4 in range(1, 4):
                for i_5 in range(1, 4):
                    neyro.predicting([i_1, i_2, i_3, i_4, i_5])
                    neyro.prediction = round_to(neyro.prediction)
                    if neyro.prediction == 1:
                        uno += 1
                    elif neyro.prediction == 2:
                        dos += 1
                    elif neyro.prediction == 3:
                        tres += 1
print("камень:", uno, "раз")
print("бумага:", dos, "раз")
print("ножницы:", tres, "раз")
