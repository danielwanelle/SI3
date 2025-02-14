import pygame 
import sys
import math
import numpy as np
class Car:

    def __init__(self):
        # Carregar o sprite do carro e rotacioná-lo
        self.sprite = pygame.image.load('car.png').convert() # Convert acelera muito o processamento
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite 

        # self.position = [690, 740] # Posição inicial
        self.position = [830, 920] # Posição inicial
        self.angle = 0
        self.speed = 0
        self.oldPosition = [820, 910]

        self.speed_set = False # Flag para velocidade padrão posteriormente

        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2] # Calcular o centro

        self.radars = [] # Lista para sensores / radares
        self.drawing_radars = [] # Radares a serem desenhados

        self.alive = True # Booleano para verificar se o carro colidiu

        self.distance = 0 # Distância percorrida
        self.time = 0 # Tempo decorrido

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position) # Desenhar sprite
        self.draw_radar(screen) # OPCIONAL PARA SENSORES
        

    def draw_radar(self, screen):
        # Opcionalmente desenhar todos os sensores / radares
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            # Se qualquer canto tocar a cor da borda -> Colisão
            # Assume um formato retangular
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Enquanto não atingir a cor da borda e o comprimento < 300 (máximo) -> continuar avançando
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calcular distância até a borda e adicionar à lista de radares
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])
    
    def update(self, game_map):
        # Definir a velocidade para 20 na primeira vez
        # Apenas quando houver 4 nós de saída com velocidade para cima e para baixo
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        # Obter sprite rotacionado e mover na direção X correta
        # Não permitir que o carro se aproxime menos de 20px da borda
        self.oldPosition[0]=self.position[0]
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        # Aumentar a distância e o tempo
        self.distance += self.speed
        self.time += 1
        
        # Mesmo para a posição Y
        self.oldPosition[1]=self.position[1]
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)
        
        # Calcular novo centro
        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        # Calcular os quatro cantos
        # O comprimento é metade do lado
        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Verificar colisões e limpar radares
        self.check_collision(game_map)
        self.radars.clear()

        # De -90 a 120 com passo de 45 verificar radar
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def get_data(self):
        # Obter distâncias até a borda
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def is_alive(self):
        # Função básica de verificação de vida
        return self.alive

    def get_reward(self):
        # Calcular recompensa (talvez mudar?)
        return self.distance / (CAR_SIZE_X / 2)

    def rotate_center(self, image, angle):
        # Rotacionar o retângulo
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image



pygame.init()
WIDTH = 1920
HEIGHT = 1080

CAR_SIZE_X = 60    
CAR_SIZE_Y = 60

BORDER_COLOR = (255, 255, 255, 255) # Cor que causa colisão ao tocar
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Configurações do relógio
# Configurações de fonte e carregamento do mapa
clock = pygame.time.Clock()
generation_font = pygame.font.SysFont("Arial", 30)
alive_font = pygame.font.SysFont("Arial", 20)
game_map = pygame.image.load('map.png').convert() # A conversão acelera muito o processamento
map_array = pygame.surfarray.array3d(game_map)

# Criar uma máscara para identificar a pista preta
track_mask = np.all(map_array == [0, 0, 0], axis=-1)
# Configurações da tela
pygame.display.set_caption("Jogo de Corrida com Curvas")
gen=0 # Atual geração
genmax=2 # Número de gerações maxima
while gen<genmax:
    gen+=1
    car = Car() # aqui foi criado somente 1 carro. Mas para uma população por exemplo de 10 indivíduos então faça um vetor de cars = [car(), ..., car()]
    while True: # Esse while define o tempo da geração.


        # Essa parte é a principal para criar a rede que irá aprender
        # A variável car.get_data() é a distâncias dos sensores -> entrada da rede
        # Variáveis car.angle e car.speed são saída da rede, ações que o carro irá fazer
        # car.get_reward() é a recompença para a rede

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
        # Movimentação do carro
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     car.angle += 15 # Left
        # if keys[pygame.K_RIGHT]:
        #     car.angle -= 5 # Right
        # if keys[pygame.K_UP]:
        #     car.speed += 2 # Speed Up
        # else:
        #     car.speed=0
        still_alive = 0
        if car.is_alive():
            still_alive += 1
            car.update(game_map)
        if still_alive == 0:
            print(str(car.get_reward())) # irá imprimir a pontuação do carro quanto ele bater
            break # Esse break irá terminar com a geração, se tiver


        screen.blit(game_map, (0, 0))
        car.draw(screen)
        
        text = alive_font.render(str(car.get_data())+" "+str(car.get_reward()),True, (0, 0, 0)) # Essa a string que imprime no meio da tela
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)
        # Atualizar a tela
        pygame.display.flip()
        clock.tick(60)