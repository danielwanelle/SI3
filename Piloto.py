import numpy as np
import math


# Inicializar os pesos e bias para 3 camadas ocultas

output_layer_size = 2
w1 = np.random.randn(2, 3)
w2 = np.random.randn(3, 2)
b1 = np.zeros((1, 3))
b2 = np.zeros((1, 2))

# Forward
def foward(input, pw1, pw2, pb1, pb2):
    # Somatório até a camada oculta
    z1 = input.dot(pw1) + pb1
    # Aplicação da função de ativação na camada oculta
    f1 = np.tanh(z1)
    # Somatório até a camada de saída
    z2 = f1.dot(pw2) + pb2
    # Softmax
    e = np.exp(z2)
    output = e / np.sum(e, axis=1, keepdims=True)

    return output, f1, z1


# def genectic_algorithm(input, output, result, f1, z1, pw1, pw2, pb1, pb2):
#     # Crossover
#     # Mutation
#     pass


# def model_fit(epochs, inputs, results, pw1, pw2, pb1, pb2):
#     for epoch in range(epochs):
#         output, f1, z1 = foward(inputs, pw1, pw2, pb1, pb2)
#         # pw1, pw2, pb1, pb2 = backpropagation(inputs, output, results, f1, z1, pw1, pw2, pb1, pb2)
#         genectic_algorithm(inputs, output, results, f1, z1, pw1, pw2, pb1, pb2)

#         #acuracia
#         prediction = np.argmax(output, axis=1)
#         correct = sum(prediction == results)
#         accuracy = correct/results.shape[0]

#         if int((epoch+1) % (epochs/10)) == 0:
#             print(f'Epoch [{epoch+1} / {epochs}] - Accuracy: {accuracy:.3f}')

#     return prediction, pw1, pw2, pb1, pb2
