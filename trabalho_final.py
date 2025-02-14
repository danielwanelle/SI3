import numpy as np
import pygame
import sys
import math

import Jogo     # seu arquivo Jogo.py
import Piloto   # seu arquivo Piloto.py

def play_best_pilot(model_file="best_pilot.npy"):
    # Carrega o melhor piloto
    loaded_obj = np.load(model_file, allow_pickle=True)
    best_pilot = loaded_obj[0]  # pois salvamos em formato [best_pilot]

    # Desempacota a tupla
    w1, w2, b1, b2 = best_pilot

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    game_map = pygame.image.load('map.png').convert()

    car = Jogo.Car()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        # Coleta dados dos sensores
        state = car.get_data()  # [s1, s2, s3, s4, s5]
        input_data = np.array(state).reshape(1, -1)

        # Faz forward pass na rede usando o best_pilot
        output, _, _ = Piloto.foward(input_data, w1, w2, b1, b2)

        # Interpreta as saídas (angle_factor, speed_factor)
        angle_factor = output[0, 0]  # valor entre ~0..1
        speed_factor = output[0, 1]  # valor entre ~0..1

        # Ajusta o carro (exemplo de escala)
        car.angle += (angle_factor * 30) - 15
        car.speed = speed_factor * 20

        # Atualiza a posição do carro
        if car.is_alive():
            car.update(game_map)
        else:
            # Bateu ou saiu da pista -> encerra
            running = False

        # Desenha no pygame
        screen.blit(game_map, (0, 0))
        car.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    print("Fim de jogo!")
    print("Recompensa obtida:", car.get_reward())
    pygame.quit()

if __name__ == "__main__":
    play_best_pilot("best_pilot.npy")