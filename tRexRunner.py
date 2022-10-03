import pygame, time
from pygame.locals import *  # asterisco significa todos os módulos do pygame

pygame.init()  # inicializar todos os módulos do pygame

clock = pygame.time.Clock()  # para atualizar a tela

# tela
largura = 1000  # dimensão da tela
altura = 480  # dimensão da tela
screen = pygame.display.set_mode([largura, altura])  # para printar a tela com as dimensões

# imagem de fundo
pygame.display.set_caption("Crazy Chicken")  #legenda da janela
background = pygame.Surface([largura, altura])  # superfície do fundo
fundo = pygame.image.load("fundo.png")  # para projetar imagem de fundo
background.blit(fundo, (0, 0))  # projetar durante o game
screen.blit(fundo, (0, 0))  # projetar na tela de espera

# para estabelecer o time e a altura do jump
time_down = 0.0 # marca temporária para descida do jump
time_elapsed = 0.0  # marca "temporária" de quanto durou o jump

score = 0  # variável que armazena pontução

class Galinha():  # classe principal que representa o dino

   def __init__(self, x, y):  # inicializar a classe
       self.x = 60  # posição da galinha no eixo x
       self.y = 350  # posição da galinha no eixo y

       # pulo
       self.isJump = False  # torna-se true ao pressionar space oua seta up
       self.jumpCount = 10  # referencial para os pulos
       self.isJump2 = False # para voltar mais rápido ao solo
       self.jumpCount2 = 10 # para voltar mais rápido ao solo

       # raposas
       self.px = 800  # posicionamento inicial no eixo x da primeira raposa
       self.px2 = 1400  # posicionamento inicial no eixo x da segunda raposa

       self.bx = 18000  # posicionamento do 1º pássaro
       self.bx2 = 20000 # posicionamento do 2º pássaro

   # desenhar galinha
   def drawgalinha(self):
       galinha_img = pygame.image.load("gali.png") #sprite da galinha
       self.galinha = screen.blit(galinha_img, (self.x, self.y)) # para printar galinha na tela e posicionamento

   # para pular
   def jump(self):
       if self.isJump:
           if self.jumpCount >= -10:  # altura do pulo
               neg = 1
               if self.jumpCount < 0:
                   neg = -1
               self.y -= self.jumpCount ** 2 * time_elapsed * neg
               self.jumpCount -= 1
           else:
               self.isJump = False
               self.jumpCount = 10  # para voltar ao solo
   # para voltar mais rápido ao solo
   def jump2(self):
       if self.isJump2:
           if self.jumpCount2 >= -10:  # altura do pulo
               neg = 1
               if self.jumpCount2 < 2: # 2 ao invés de 0 para voltar mais rápido ao solo
                   neg = -1
               self.y -= self.jumpCount2 ** 2 * time_elapsed * neg
               self.jumpCount2 -= 10
           else:
               self.isJump2 = False
               self.jumpCount2 = 5  # para voltar ao solo

   # desenhar raposa
   def drawraposa(self):
       self.px += (-10)  # velocidade da primeira raposa
       self.px2 += (-10)  # velocidade da segunda raposa
       fox = pygame.image.load("raposa.png") # sprite da raposa
       self.raposa = screen.blit(fox, [self.px, 350, 150, 30]) #printar raposas na tela
       self.raposa2 = screen.blit(fox, [self.px2, 350, 150, 60])
       # movimentação da primeria raposa:
       if self.px:
           if self.px >= largura:  # para que a raposa volte à tela
               self.px += (-10)
           if self.px <= 0:
               self.px = largura

       # movimentação da segunda raposa:
       if self.px2:
           if self.px2 >= largura:
               self.px2 += (-2)
           if self.px2 <= 0:
               self.px2 = largura

   # desenhar passaros
   def drawbirds(self):
       self.bx += (-5)  # velocidade de movimentação dos pássaros
       self.bx2 += (-5)
       eagle = pygame.image.load("águia.png") # para sprite
       self.bird = screen.blit(eagle, [self.bx, 270, 150, 30]) # printar águia
       self.bird2 = screen.blit(eagle, [self.bx2, 190, 150, 30])

       # movimentação do primeiro pássaro
       if self.bx:
           if self.bx >= largura:
               self.bx += (-2)
           if self.bx <= 0:
               self.bx = largura

       # movimentação do segundo pássaro
       if self.bx2:
           if self.bx2 >= largura:
               self.bx2 += (-2)
           if self.bx2 <= 0:
               self.bx2 = largura

   # mensagens impressas na tela
   def msg(self):
       WHITE = (255, 255, 255)  # código RGB
       pygame.font.init()  # inicializador de fonte do pygame
       self.fonte_padrao = pygame.font.get_default_font()  # fonte padrão do pygame
       self.fonte_perdeu = pygame.font.SysFont(self.fonte_padrao, 80)  # aparece qnd há colisão
       self.fonte_retry = pygame.font.SysFont(self.fonte_padrao, 35)  # opção para dar reset após game over
       self.font = pygame.font.SysFont(pygame.font.get_default_font(), 45)  # para score
       screen.blit(font.render('SCORE: ' + str(score), True, WHITE), (830, 15))  # printar score na tela

   # colisões e game over
   def colidir(self):
       if self.galinha.colliderect(self.raposa):  # colisão da galinha com a raposa
           return True

       if self.galinha.colliderect(self.raposa2):  # colisão da galinha com a raposa 2
           return True

       if self.galinha.colliderect(self.bird):  # colisão com o águia 1
           return True
       if self.galinha.colliderect(self.bird2):  # colisão com  a águia 2
           return True

       return False

# Aguarda que  determinada tecla seja pressionada e verifica se é igual a key.
# Caso seja igual o jogo é iniciado
def wait(key):
   while True:
       for event in pygame.event.get():
           if event.type == pygame.QUIT: exit(0)
           if event.type == pygame.KEYDOWN:
               if event.key == key: return

WHITE = (255, 255, 255)  # código RGB
font = pygame.font.SysFont(pygame.font.get_default_font(), 45) # fonte do score
screen.blit(font.render('PRESS SPACE TO START', True, WHITE), (310, 180))  # printar score na tela

galinha = Galinha(0, 0)
galinha.drawgalinha()
galinha.drawraposa()
galinha.drawbirds()
pygame.display.update()
wait(pygame.K_SPACE) #funções do jogo

fimdejogo = False # variaveis para loop de jogo e quit
sair = False # variaveis para loop de jogo e quit

t = 0 # variável de tempo

while sair == False:
   if not fimdejogo:
       for event in pygame.event.get():  # enqtn meu evento receber um evento do pygame deve capturá-lo, que é sair da tela
           if event.type == pygame.QUIT:  # verificar se o evento capturado foi o evento fechado
               sair = True # acaba o game e fecha aba de jogo
               break
           if event.type == pygame.KEYDOWN:
               # quando pressionar espaço ou seta pra cima pular
               if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                   t = time.time()  # começa a contar o tempo
           if event.type == pygame.KEYUP:
               if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and t != 0:
                   time_elapsed = time.time() - t  # quando a tecla é solta, calcula o tempo pressionado
                   time_elapsed = max(min(time_elapsed, 0.6), 0.3)  # mínimo de 0.3s e máximo de 0.6s
                   # máximo de 1 segundo
                   galinha.isJump = True  # pula
                   t = 0
                   score += 1  # a cada pulo soma um score
           if event.type == pygame.KEYDOWN: # para galinha voltar mais rápido ao solo
               if event.key == K_DOWN:
                   galinha.isJump2 = True # variável do jump 2
       screen.blit(background, (0, 0))
       galinha.drawgalinha()
       galinha.drawraposa()
       galinha.drawbirds()
       galinha.jump()
       galinha.jump2()
       galinha.msg()
       if galinha.colidir():  # reiniciar
           msg = galinha.fonte_perdeu.render("GAME OVER", True, WHITE)  # imprimir mensagem, com a cor white
           msg1 = galinha.fonte_retry.render("SPACE TO RESTART", True, WHITE)
           msg2 = galinha.fonte_retry.render("BACKSPACE TO QUIT", True, WHITE)
           screen.blit(msg, (350, 100))  # imprime a mensagem de acordo com o posicionamento indicado
           screen.blit(msg1, (410, 160))
           screen.blit(msg2, (400, 197))
           fimdejogo = True
           pygame.mixer.music.load("som.mp3") #som de "cocó" quando a galinha colide
           pygame.mixer.music.play() # comandos para som
           pygame.event.wait()
       pygame.display.update()  # atualizações
   else:  # sair
       for event in pygame.event.get():
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                   score = 0  # reiniciar marca da pontuação
                   fimdejogo = False
                   galinha = Galinha(50, 30)
               if event.key == pygame.K_BACKSPACE:  # sair do jogo caso tecle backsapce
                   sair = True
                   print("Obrigada por utilizar o jogo!")
                   break
   clock.tick(60)  # 60 frames atualizados por segundo
pygame.quit()  # qnd clicar no fechar é chamado pygame.quit, saindo do while


