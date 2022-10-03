import pygame
from pygame.locals import *  # asterisco significa todos as bibliotecas
import random # para sortear

class Pacman(object):  # classe do pacman
    LEFT = 0  # para movimentação do pac, cada direção é indicada por um número
    UP = 1
    RIGHT = 2
    DOWN = 3
    COLOR = (255, 204, 0)  # cores do pac

    def __init__(self, x, y, tiles): # inicializador da classe
        self.x = x  # x e y indicam localização e movimentação do pacman no maze
        self.y = y
        self.tiles = tiles  # cada azulejo do maze, como de fossem "casas" em um tabuleiro
        self.comida = [line[:] for line in tiles]  # 1 comidinha para cada azulejo
        self.pontos = 0  # soma 10 pontos a cada pastilha comida
        self.pastilhas = 204  # total de pastilhas do maze inicial, vai diminuindo quando come
        self.direction = None # a direção é indefinida
        self.pos_antiga = None # guarda a antiga posição para verificar colisão com fantasma
        self.rect = None # indefinida
        self.__comer()  # posteriormente utilizada para comer as pastilhas

    def __can_move(self, direction):  # verifica se pode mover-se (caminho ou parede)
        width = len(self.tiles[0]) - 1
        # verifica qual é a direção que pretende mover-se (Left ou up..., e verifica se
        # é maior que 0, logo é caminho e não parede )
        if direction == Pacman.LEFT and self.y > 0 and tiles[self.x][self.y - 1]: return True
        if direction == Pacman.UP and self.x > 0 and tiles[self.x - 1][self.y]: return True
        if direction == Pacman.RIGHT and self.y < width and tiles[self.x][self.y + 1]: return True
        if direction == Pacman.DOWN and self.x < width and tiles[self.x + 1][self.y]: return True
        return False

    def move(self, direction): # para movimentação do pacman
        self.pos_antiga = (self.x, self.y)  # para guardar a posição antiga e posteriormente verificar colisão
        self.direction = direction
        if self.__can_move(direction):  # indica como mover
            if direction == Pacman.LEFT:
                self.y -= 1  # se for = 0, y recebe -1 para movimentar para esquerda, o mesmo ocorre com as outras direções
            elif direction == Pacman.UP:
                self.x -= 1
            elif direction == Pacman.RIGHT:
                self.y += 1
            elif direction == Pacman.DOWN:
                self.x += 1
            self.__comer()  # função comer pastilhas para quando o pacman mover-se

    def __comer(self): # para comer pastilhas
        if self.comida[self.x][self.y]: # verifica se com a posição no eixo x e y o pacman passa por cima de uma comida
            self.comida[self.x][self.y] = 0 # substitui 0 por 1 para comer as pastilhas
            self.pontos += 10  # soma 10 pontos cada pastilha que come
            self.pastilhas -= 1 # diminui do 204 uma pastilha, cada vez q come, qnd chegar a 0 ganha o jogo
            self.musica = pygame.mixer.music.load("waka.wav") # cada vez que come, toca a musiquinha
            pygame.mixer.music.play() # comando o pygame para tocar músicas

class Maze(object):  # classe do labirinto
    SQUARE_SIZE = 30  # tamanho do lab
    BLUE = (0, 140, 255)  # padrão rgb das cores utilizadas
    BLACK = (0, 0, 0)
    ORANGE = (170, 132, 58)
    WHITE = (255, 255, 255)

    def __init__(self, screen, pacman, tiles, fantasmas): # inicializa a classe
        self.pacman = pacman # pacman
        self.tiles = tiles # azulejos
        self.fantasmas = fantasmas # fantasmas
        self.size = len(tiles[0])  # tamanho do maze é determinado pelo número de azulejos
        self.screen = screen # tela de jogo

        self.drawer = pygame.draw  # para desenhar
        self.screen.fill(Maze.BLACK)  # printa fundo preto

    def draw(self):  # desenha o labirinto e as comidinhas
        self.screen.fill(Maze.BLACK)  # fundo preto
        mid_square = int(Maze.SQUARE_SIZE / 2)  # para que as comidinhas pacman e fantasma fique centralizado
        for l in range(self.size):  # para desenhar linhas de acordo com o tamanho do maze
            for c in range(self.size): # para desenhar colunas de acordo com o tamanho do maze
                tile = self.tiles[l][c]  # azulejos estão nas linhas e colunas
                comida = self.pacman.comida[l][c]  # comidas nas linhas e colunas
                if tile > 0: # verifica se na matriz existem elementos maiores que 0, então desenha linhas e colunas
                    x = l * Maze.SQUARE_SIZE # x = linhas de acordo com o tamanho do maze
                    y = c * Maze.SQUARE_SIZE # y = colunas de acordo com o tamanho do maze
                    self.drawer.rect(self.screen, Maze.BLUE, [y, x, Maze.SQUARE_SIZE, Maze.SQUARE_SIZE],
                                     0)  # desenha caminhos nos tiles maiores que 0

                    if comida == 1:  # para desenhar as comidinhas em cada azulejo
                        c = self.drawer.circle(self.screen, Maze.BLACK, (y + mid_square, x + mid_square), 4,
                                                0)  # desenha e posiciona, raio das comidinhas

        x = self.pacman.x * Maze.SQUARE_SIZE  # localização do pacman no maze no eixo x
        y = self.pacman.y * Maze.SQUARE_SIZE # localização do pacman no maze no eixo y
        pc = self.drawer.circle(self.screen, Pacman.COLOR, (y + mid_square, x + mid_square), 15, 0)  # desenha o pacman

        for fantasma in fantasmas: # para cada fantasma, desenhar
            x = fantasma.x * Maze.SQUARE_SIZE # localização dos fantasmas no eixo x
            y = fantasma.y * Maze.SQUARE_SIZE # localização dos fantasmas  no eixo y
            fantasma.rect = self.screen.blit(fantasma.sprite, [y, x, 1, 1])  # printar sprite

        # informações no maze
        # para printar rules
        comandos = pygame.key.get_pressed()  # verifica se teclas foram pressionadas
        if comandos[K_h]: # verifica se o h foi pressionado
            regras = pygame.image.load("rules.jpg")  # sprite das regras
            self.screen.blit(regras, [85, 100, 20, 20])  # printar regras na tela

        # textos
        font2 = pygame.font.SysFont("arial black", 20)
        self.screen.blit(font2.render('H PARA VER REGRAS', True, Maze.WHITE), (310, 607))  # printar na borda inferior da tela
        self.screen.blit(font2.render('PONTOS: ' + str(pacman.pontos), True, Maze.WHITE),
                         (120, 10))  # printar score na tela
        self.screen.blit(font2.render('PASTILHAS: ' + str(pacman.pastilhas), True, Maze.WHITE), # + str para ir mudando o número de pastilhas
                         (350, 10))  # printar na borda superior da tela

class Fantasma(object): # classe dos fantasmas
    # direções para movimentação dos fantasmas, cada direção vale um número
    DIRECTIONS = [
        0,  # left
        1,  # up
        2,  # right
        3  # down
    ]
    def __init__(self, tiles, pos, sprite):
        self.tiles = tiles
        self.sprite = pygame.image.load(sprite)  # para printar sprites dos fantasmas
        self.y = pos[0]
        self.x = pos[1]
        self.rect = None
        self.direction = None
        self.posantiga = None # para guardar a posição e depois verificar colisões

    def __can_move(self):  # verifica se os fantasmas podem mover-se (caminho ou parede)
        width = len(self.tiles[0]) - 1
        if self.direction == Fantasma.DIRECTIONS[0] and self.y > 0 and tiles[self.x][self.y - 1]: return True
        if self.direction == Fantasma.DIRECTIONS[1] and self.x > 0 and tiles[self.x - 1][self.y]: return True
        if self.direction == Fantasma.DIRECTIONS[2] and self.y < width and tiles[self.x][self.y + 1]: return True
        if self.direction == Fantasma.DIRECTIONS[3] and self.x < width and tiles[self.x + 1][self.y]: return True
        return False

    def move(self):  # mover fantasmas
        while self.direction is None or not self.__can_move():
            self.direction = random.choice(Fantasma.DIRECTIONS)  # sotear direções para o fantasma mover-se
        if self.direction == Fantasma.DIRECTIONS[0]:  # se por exemplo, sortear == 0, vai para a esquerda
            self.y -= 1
        elif self.direction == Fantasma.DIRECTIONS[1]: # mover para cima
            self.x -= 1
        elif self.direction == Fantasma.DIRECTIONS[2]: # mover para direita
            self.y += 1
        elif self.direction == Fantasma.DIRECTIONS[3]: # mover para baixo
            self.x += 1

    def colidiu(self, direction, pos, pos_antiga):
        if self.x == pos[0] and self.y == pos[1]: # verifica posição dos fantasmas para analisar colisão
            return True
        # compara se a posiçao do pacman foi igual posição dos fantasmas, se for, houve colisão
        elif direction and pos_antiga and self.x == pos_antiga[0] and self.y == pos_antiga[1]:
            if (self.direction == Fantasma.DIRECTIONS[0] and direction == Pacman.RIGHT) or \
                    (self.direction == Fantasma.DIRECTIONS[1] and direction == Pacman.DOWN) or \
                    (self.direction == Fantasma.DIRECTIONS[2] and direction == Pacman.LEFT) or \
                    (self.direction == Fantasma.DIRECTIONS[3] and direction == Pacman.UP):
                return True
        return False

# 0 parede e 1 indica caminho
tiles = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
pygame.init()  # inicializa as funções do pygame
WINDOW_X_SIZE = 600 # dimensões da tela
WINDOW_Y_SIZE = 650
screen = pygame.display.set_mode((WINDOW_X_SIZE, WINDOW_Y_SIZE))  # janela do game
legenda = pygame.display.set_caption("Pacman")  # legenda da janela
MOVE = pygame.USEREVENT + 1  # para movimentar fantasmas, cria um novo evento a cada 400ms
pygame.time.set_timer(MOVE, 400) # os fantasmas se movem a cada 400ms
# posiciona sprites dos fantasmas
fantasmas = [Fantasma(tiles, (1, 2), 'f4.png'), Fantasma(tiles, (18, 19), 'f4.png'), Fantasma(tiles, (10,15), "f4.png"), Fantasma(tiles, (10,6), "f4.png")]
pacman = Pacman(9, 10, tiles) # classe do pacman
maze = Maze(screen, pacman, tiles, fantasmas) # classe do labirinto
clock = pygame.time.Clock()  # tempo de atualização da tela

# para só iniciar o game após teclar key (espaço)
def wait(texts, fonts, keys, screen, color=(170, 132, 58)):
    for i, text in enumerate(texts): # enumerate retorna um interável
        text_width, text_height = fonts[i].size(text)
        pos = (WINDOW_X_SIZE - text_width) // 2, (WINDOW_Y_SIZE - text_height) // 2 + 50 * i  # para centralizar o texto
        screen.blit(fonts[i].render(text, True, color), pos) # para printar fontes na screen
    pygame.display.update() # atualizar tela
    return_key = None
    while return_key is None: # enquanto nenhuma tecla for pressionada
        for event in pygame.event.get(): # captura eventos
            if event.type == pygame.KEYDOWN:  # verifica se o espaço foi pressionado
                if event.key in keys:
                    return_key = event.key
    return return_key # para posteriormente reiniciar o jogo


font = pygame.font.SysFont(pygame.font.get_default_font(), 30) # fonte do wait
wait(['PRESS SPACE TO START'], [font], [pygame.K_SPACE], screen)  # qnd clicar space o jogo começa
vidas = 3 # vidas iniciais

while True: # pricipal while do game
    maze.draw() # desenha o labirinto
    for event in pygame.event.get():  # verifica eventos
        if event.type == pygame.QUIT:  # verifica se quer sair
            exit()  # fecha a janela do jogo
            pygame.display.update() # atualização de telas
        if event.type == MOVE: # para movimentar fantasmas, evento que atualiza a cada 1 seg
            for fantasma in maze.fantasmas:
                fantasma.move()
        if event.type == pygame.KEYDOWN:  # verifica teclas pressionadas
            keys = pygame.key.get_pressed()
            if keys[pygame.K_BACKSPACE]: # se o backspace for pressionado fecha a janela do game
                pygame.quit()
                exit()  # para sair do jogo
            if keys[K_UP]: pacman.move(Pacman.UP) # se teclar a setinha, o pacman move-se
            if keys[K_DOWN]: pacman.move(Pacman.DOWN)
            if keys[K_LEFT]: pacman.move(Pacman.LEFT)
            if keys[K_RIGHT]: pacman.move(Pacman.RIGHT)
            for fantasma in maze.fantasmas: # para cada fantasma dentre os fantasmas:
                if fantasma.colidiu(pacman.direction, (pacman.x, pacman.y), pacman.pos_antiga): # se ocuparam a mesma posição
                    vidas -= 1 # diminui uma vida
                    musica2 = pygame.mixer.music.load("colide.wav") # musica para quando colide
                    pygame.mixer.music.play() # método do pygame para tocar música
                    if vidas == 0: # se as vidas forem igual a 0
                        screen.fill(Maze.BLACK) # printa fundo preto
                        font2 = pygame.font.SysFont(pygame.font.get_default_font(), 35)  # fonte
                        font3 = pygame.font.SysFont("arial black", 30)
                        screen.blit(font3.render('GAME OVER', True, Maze.ORANGE), (195, 230)) # printa game over na tela
                        key = wait(['TECLE R PARA JOGAR NOVAMENTE', # informações durante o wait
                                    'TECLE BACKSPACE PARA SAIR'],
                                   [font2, font2], [pygame.K_r, pygame.K_BACKSPACE], screen, color=Maze.ORANGE)
                        if key == pygame.K_BACKSPACE: # se clicar o backspace fecha a janela do jogo
                            exit()
                        elif key == pygame.K_r:  # para restart game
                            vidas = 3
                            # pacman em posição inicial
                            pacman = Pacman(9, 10, tiles)
                            # fantasmas em posição inicial
                            fantasmas = [Fantasma(tiles, (1, 2), 'f4.png'), Fantasma(tiles, (18, 19), 'f4.png'),
                                         Fantasma(tiles, (10, 15), "f4.png"), Fantasma(tiles, (10, 6), "f4.png")]
                            maze = Maze(screen, pacman, tiles, fantasmas) # novas comidinhas, maze restart

    if maze.pacman.pastilhas == 0:  # quando pastilhas forem = 0,ganha o jogo
        screen.fill(Maze.BLACK) # fundo preto
        font2 = pygame.font.SysFont(pygame.font.get_default_font(), 35)  # fonte
        font3 = pygame.font.SysFont("arial black", 30)
        screen.blit(font3.render('PARABÉNS, VOCÊ GANHOU!', True, Maze.ORANGE), (70, 230))
        key = wait(['TECLE R PARA JOGAR NOVAMENTE', # informações para o wait winner
                    'TECLE BACKSPACE PARA SAIR'],
                   [font2, font2], [pygame.K_r, pygame.K_BACKSPACE], screen, color=Maze.ORANGE)
        if key == pygame.K_BACKSPACE: # fecha a janela do jogo
            pygame.quit()
            exit()
        elif key == pygame.K_r:  # para restart game
            pacman = Pacman(9, 10, tiles)
            fantasmas = [Fantasma(tiles, (1, 2), 'f4.png'), Fantasma(tiles, (18, 19), 'f4.png'), Fantasma(tiles, (10,15), "f4.png"), Fantasma(tiles, (10,6), "f4.png")]
            maze = Maze(screen, pacman, tiles, fantasmas)
    WHITE = (255, 255, 255) # padrão rgb
    font2 = pygame.font.SysFont("arial black", 20)
    screen.blit(font2.render('VIDAS: ' + str(vidas), True, WHITE), (110, 610))  # printar vidas na tela
    pygame.display.update()  # atualizações na tela
    clock.tick(60)  # Frames atualizados por segundo
