import numpy as np
import random
import pygame
import sys
import Jogo  
import Piloto 

POPULATION_SIZE = 10
GENERATIONS = 20

def create_individual():
    # pesos e biases aleatórios
    w1 = np.random.randn(5, 8)  # 5 sensores, 8 neurônios na camada oculta
    w2 = np.random.randn(8, 2)  # 2 saídas  
    b1 = np.zeros((1, 8))
    b2 = np.zeros((1, 2))
    return (w1, w2, b1, b2)

def evaluate_individual(ind, max_steps=1000):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080))
    clock = pygame.time.Clock()

    game_map = pygame.image.load('map.png').convert()

    car = Jogo.Car()

    running = True
    steps = 0  # Contador de passos
    while running:
        steps += 1
        if steps > max_steps:
            # Se atingiu o número máximo de passos, paramos
            running = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

        # Obtém dados dos sensores
        state = car.get_data()
        input_data = np.array(state).reshape(1, -1)

        # Forward na rede do indivíduo
        (w1, w2, b1, b2) = ind
        output, _, _ = Piloto.foward(input_data, w1, w2, b1, b2)

        # Interpreta saídas
        angle_factor = output[0, 0]  # 0..1
        speed_factor = output[0, 1]  # 0..1
        # atualiza o valor do angulo e velocidade
        car.angle += (angle_factor * 30) - 15
        car.speed = speed_factor * 20

        # Verifica vida
        if car.is_alive():
            car.update(game_map)
        else:
            running = False

        screen.blit(game_map, (0, 0))
        car.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    reward = car.get_reward()
    pygame.quit()
    return reward

def crossover(parent1, parent2):
    """
    Faz crossover simples entre dois indivíduos (w1, w2, b1, b2)
    Retorna um filho (w1, w2, b1, b2)
    """
    w1a, w2a, b1a, b2a = parent1
    w1b, w2b, b1b, b2b = parent2
    
    child_w1 = np.where(np.random.rand(*w1a.shape) < 0.5, w1a, w1b)
    child_w2 = np.where(np.random.rand(*w2a.shape) < 0.5, w2a, w2b)
    child_b1 = np.where(np.random.rand(*b1a.shape) < 0.5, b1a, b1b)
    child_b2 = np.where(np.random.rand(*b2a.shape) < 0.5, b2a, b2b)
    
    return (child_w1, child_w2, child_b1, child_b2)

def mutate(ind, mutation_rate=0.01):
    """
    Aplica mutação gaussiana nos pesos
    """
    (w1, w2, b1, b2) = ind
    # Exemplo de mutação
    w1 += np.random.normal(0, 1, w1.shape) * (np.random.rand(*w1.shape) < mutation_rate)
    w2 += np.random.normal(0, 1, w2.shape) * (np.random.rand(*w2.shape) < mutation_rate)
    b1 += np.random.normal(0, 1, b1.shape) * (np.random.rand(*b1.shape) < mutation_rate)
    b2 += np.random.normal(0, 1, b2.shape) * (np.random.rand(*b2.shape) < mutation_rate)
    return (w1, w2, b1, b2)

def run_ga():
    # Cria população inicial
    population = [create_individual() for _ in range(POPULATION_SIZE)]
    
    for gen in range(GENERATIONS):
        #Avalia cada indivíduo
        fitness_scores = []
        for ind in population:
            fitness = evaluate_individual(ind)
            fitness_scores.append((ind, fitness))
        
        # Ordena do melhor pro pior
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        print(f"Geração {gen} - Melhor fitness: {fitness_scores[0][1]:.2f}")
        
        # Seleciona os melhores
        top_individuals = fitness_scores[:2]  # ex: pega só os 2 melhores
        
        # Cria nova população
        new_population = []
        
        # Mantém os 2 melhores
        new_population.append(top_individuals[0][0])
        new_population.append(top_individuals[1][0])
        
        # Preenche o resto da população via crossover+mutação
        while len(new_population) < POPULATION_SIZE:
            parent1 = random.choice(top_individuals)[0]
            parent2 = random.choice(top_individuals)[0]
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate=0.05)
            new_population.append(child)
        
        population = new_population
    
    fitness_scores = []
    for ind in population:
        fitness_scores.append((ind, evaluate_individual(ind)))
    fitness_scores.sort(key=lambda x: x[1], reverse=True)
    best_ind = fitness_scores[0][0]
    best_score = fitness_scores[0][1]
    
    print("Selecao de Pilotos finalizado!")
    print("Melhor Piloto obteve reward=", best_score)
    return best_ind

if __name__ == "__main__":
    best_pilot = run_ga()
    obj = np.array([best_pilot], dtype=object)
    np.save("best_pilot.npy", obj, allow_pickle=True)
