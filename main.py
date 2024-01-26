#importações iniciais
import pygame
import random

pygame.init() #iniciar a biblioteca
pygame.display.set_caption('Jogo da Cobrinha') #nome que vai aparecer na janela
largura = 900
altura = 700
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

#cores (formato RGB)
preto = (0,0,0)
branca = (255,255,255)
red = (255,0,0)
verde = (0,255,0)

#parametros da cobrinha
tamanho_quadrado = 20 #cobra e comida vai ser 10x10
velocidade_jogo = 15


def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado)/float(tamanho_quadrado)) * float(tamanho_quadrado) #se for a lagura toda, vai para fora da tela
    comida_y = round(random.randrange(0, altura - tamanho_quadrado)/float(tamanho_quadrado)) * float(tamanho_quadrado)
    return comida_x, comida_y


def desenhar_comida(tamanho, comida_x,comida_y):
    pygame.draw.rect(tela, red, [comida_x, comida_y, tamanho, tamanho]) #desenhar comida na tela

def desenhar_cobra(tamanho, pixels):
    for pixel in pixels:
        pygame.draw.rect(tela, branca, [pixel[0], pixel[1], tamanho, tamanho])


def selecionar_velocidade(tecla):
    if tecla == pygame.K_DOWN: # se for pra baixo
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    elif tecla == pygame.K_UP: # se for pra cima
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
    elif tecla == pygame.K_RIGHT:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0
    elif tecla == pygame.K_LEFT:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0
    return velocidade_x, velocidade_y

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont('Helvetica', 25)
    texto = fonte.render(f'Pontos: {pontuacao}', True, verde) #True: sem pixels, redondo
    tela.blit(texto, [4,4])

def rodar_jogo():
    fim_jogo = False
    x = largura/2
    y = altura/2

    velocidade_x = 0
    velocidade_y = 0

    tamanho_cobra = 1
    pixels = []
    #primeira comida
    comida_x, comida_y = gerar_comida()

#looping infinito
    while not fim_jogo:
        tela.fill(preto)
        for evento in pygame.event.get(): #cada vez que o user colocar alguma coisa, vai add nessa lista
            if evento.type == pygame.QUIT: #evento type é o usuário
                fim_jogo = True
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        #se bater na parede
        if x < 0 or x >= largura or y < 0 or y >= altura:
            fim_jogo = True
        #atualizar a pos da cobra
        x += velocidade_x
        y += velocidade_y
        # desenhar os objetos:
        # -comida
        desenhar_comida(tamanho_quadrado, comida_x,comida_y)
        # -pontuação;
        desenhar_pontuacao(tamanho_cobra - 1)
        # -cobrinha;
        pixels.append([x,y]) #cabeça da cobrinha
        if len(pixels) > tamanho_cobra: #a cobra vai andar quando a gente add o pixel na ultima pos e deletar o 1
            del pixels[0]
        #se a cobrinha bateu no próprio corpo
        for pixel in pixels[:-1]: #cabeça é o último item
            if pixel == [x,y]:
                fim_jogo = True
        desenhar_cobra(tamanho_quadrado, pixels)

        #atualização tela
        pygame.display.update()
        #criar uma nova comida
        if x == comida_x and y == comida_y: #cobra comeu
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()
        relogio.tick(velocidade_jogo)
rodar_jogo()