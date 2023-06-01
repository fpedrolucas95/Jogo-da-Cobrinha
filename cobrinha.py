import pygame
import random
import sys

# Função para iniciar uma nova partida
def iniciar_nova_partida():
    # Inicializa o Pygame
    pygame.init()

    largura_tela = 800
    altura_tela = 600
    tamanho_cobra = 20
    raio_comida = 10
    velocidade = 10

    # Cria a tela do jogo
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Jogo da Cobrinha")

    # Define as cores
    cor_fundo = (255, 255, 255)  # Branco
    cor_cobra = (0, 0, 0)  # Preto
    cor_comida = (255, 0, 0)  # Vermelho
    cor_botao = (0, 0, 255)  # Azul

    # Define a posição inicial da cobra
    posicao_cobra = [(largura_tela // 2, altura_tela // 2)]
    tamanho_inicial_cobra = 5

    # Gera a posição inicial da comida
    posicao_comida = (random.randint(0, largura_tela - raio_comida * 2) // 10 * 10 + raio_comida,
                      random.randint(0, altura_tela - raio_comida * 2) // 10 * 10 + raio_comida)

    # Define a direção inicial da cobra
    direcao = "cima"

    # Define o timer, pontuação inicial e maior pontuação
    timer = 0
    pontuacao = 0
    # Use uma variável global para a maior pontuação
    global maior_pontuacao 
    if not 'maior_pontuacao' in globals():
        maior_pontuacao = 0

    # Define os botões
    botao_novo_jogo = pygame.Rect(largura_tela // 2 - 70, altura_tela // 2 + 100, 140, 50)
    botao_sair = pygame.Rect(largura_tela // 2 - 70, altura_tela // 2 + 160, 140, 50)

    # Função para desenhar a cobra na tela
    def desenhar_cobra():
        for posicao in posicao_cobra:
            pygame.draw.rect(tela, cor_cobra, (posicao[0], posicao[1], tamanho_cobra, tamanho_cobra))

    # Função para desenhar um botão na tela
    def desenhar_botao(rect, texto):
        pygame.draw.rect(tela, cor_botao, rect)
        fonte = pygame.font.SysFont(None, 24)
        texto_botao = fonte.render(texto, True, cor_fundo)
        tela.blit(texto_botao, (rect.x + rect.width // 2 - texto_botao.get_width() // 2,
                                rect.y + rect.height // 2 - texto_botao.get_height() // 2))

    # Função para mover a cobra
    def mover_cobra():
        nonlocal posicao_comida, pontuacao, tamanho_inicial_cobra

        if direcao == "cima":
            nova_posicao = (posicao_cobra[0][0], posicao_cobra[0][1] - velocidade)
        elif direcao == "baixo":
            nova_posicao = (posicao_cobra[0][0], posicao_cobra[0][1] + velocidade)
        elif direcao == "esquerda":
            nova_posicao = (posicao_cobra[0][0] - velocidade, posicao_cobra[0][1])
        elif direcao == "direita":
            nova_posicao = (posicao_cobra[0][0] + velocidade, posicao_cobra[0][1])

        posicao_cobra.insert(0, nova_posicao)
        if len(posicao_cobra) > tamanho_inicial_cobra:
            posicao_cobra.pop()

        if posicao_cobra[0][0] - raio_comida < posicao_comida[0] < posicao_cobra[0][0] + tamanho_cobra + raio_comida and \
           posicao_cobra[0][1] - raio_comida < posicao_comida[1] < posicao_cobra[0][1] + tamanho_cobra + raio_comida:
            posicao_comida = (random.randint(0, largura_tela - raio_comida * 2) // 10 * 10 + raio_comida,
                              random.randint(0, altura_tela - raio_comida * 2) // 10 * 10 + raio_comida)
            pontuacao += 1
            tamanho_inicial_cobra += 1

    # Função para verificar colisões
    def verificar_colisoes():
        if posicao_cobra[0][0] < 0 or posicao_cobra[0][0] >= largura_tela or \
                posicao_cobra[0][1] < 0 or posicao_cobra[0][1] >= altura_tela:
            return True

        for posicao in posicao_cobra[1:]:
            if posicao == posicao_cobra[0]:
                return True

        return False

    # Loop principal do jogo
    jogo_ativo = True
    clock = pygame.time.Clock()

    while jogo_ativo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jogo_ativo = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direcao != "baixo":
                    direcao = "cima"
                elif event.key == pygame.K_DOWN and direcao != "cima":
                    direcao = "baixo"
                elif event.key == pygame.K_LEFT and direcao != "direita":
                    direcao = "esquerda"
                elif event.key == pygame.K_RIGHT and direcao != "esquerda":
                    direcao = "direita"

        tela.fill(cor_fundo)
        desenhar_cobra()
        pygame.draw.circle(tela, cor_comida, posicao_comida, raio_comida)
        mover_cobra()
        fonte = pygame.font.SysFont(None, 24)
        texto_pontuacao = fonte.render(f"Pontuação: {pontuacao}", True, cor_cobra)
        tela.blit(texto_pontuacao, (10, 10))

        if verificar_colisoes():
            if pontuacao > maior_pontuacao:
                maior_pontuacao = pontuacao
            jogo_ativo = False

        pygame.display.update()
        clock.tick(15)

    # Janela de Game Over
    gameover = True
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos_mouse = pygame.mouse.get_pos()
                if botao_novo_jogo.collidepoint(pos_mouse):
                    iniciar_nova_partida()
                elif botao_sair.collidepoint(pos_mouse):
                    pygame.quit()
                    sys.exit()

        tela.fill(cor_fundo)
        fonte = pygame.font.SysFont(None, 30)
        texto_gameover = fonte.render("Fim de Jogo", True, cor_cobra)
        texto_pontuacao_final = fonte.render(f"Pontuação Final: {pontuacao}", True, cor_cobra)
        texto_maior_pontuacao = fonte.render(f"Maior Pontuação: {maior_pontuacao}", True, cor_cobra)
        tela.blit(texto_gameover, (largura_tela // 2 - 60, altura_tela // 2 - 50))
        tela.blit(texto_pontuacao_final, (largura_tela // 2 - 90, altura_tela // 2))
        tela.blit(texto_maior_pontuacao, (largura_tela // 2 - 95, altura_tela // 2 + 50))

        botao_novo_jogo = pygame.draw.rect(tela, (0, 255, 0), (largura_tela // 2 - 60, altura_tela // 2 + 100, 120, 50))
        botao_sair = pygame.draw.rect(tela, (255, 0, 0), (largura_tela // 2 - 60, altura_tela // 2 + 160, 120, 50))
        fonte_botao = pygame.font.SysFont(None, 24)
        texto_botao_novo_jogo = fonte_botao.render("Novo Jogo", True, (0, 0, 0))
        texto_botao_sair = fonte_botao.render("Sair", True, (0, 0, 0))
        tela.blit(texto_botao_novo_jogo, (largura_tela // 2 - 40, altura_tela // 2 + 115))
        tela.blit(texto_botao_sair, (largura_tela // 2 - 20, altura_tela // 2 + 175))

        texto_desenvolvedor = fonte.render("Desenvolvido por Pedro Lucas França", True, cor_cobra)
        tela.blit(texto_desenvolvedor, (largura_tela // 2 - 190, altura_tela - 40))

        pygame.display.update()

    pygame.quit()

iniciar_nova_partida()
