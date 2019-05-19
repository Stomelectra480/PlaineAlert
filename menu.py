import pygame
import sys
import time
from pygame.locals import *
import subprocess
import os
 


pygame.init()

#Paramètre
mainClock = pygame.time.Clock()
W = 640
H = 480


#création de la fenêtre
Surface = pygame.display.set_mode((W,H), 0, 32)
pygame.display.set_caption('Menu Principale')
son = pygame.mixer.Sound("menu.wav")


#Définie les couleur
NOIR = (0, 0, 0)
VERT = (0, 255, 0)
BLANC = (255, 255, 255)
BLUE = (0, 0, 255)
ROUGE = (255, 0, 0)
JAUNE = (255, 255, 0)
GRIS = (128,128,128)



continuer = 1
mouse_pos = (0,0)
mouse_click = (0,0)
text1_bool = False
text2_bool = False
text3_bool = False
output = '?'



while continuer == 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit(0)
        if event.type == MOUSEMOTION:
            mouse_pos = event.pos
        if event.type == MOUSEBUTTONUP:
            mouse_click = event.pos




    
    son.play()
    Surface.fill(GRIS)
    color = BLANC
    Font = pygame.font.SysFont('arial', 40)
    #Quand la souris vas passer sur le rectangle elle changera de couleur avec la fonction "Bool"
    if text1_bool:
        color = ROUGE
    text = Font.render('Play',True,color)
    text_rect = text.get_rect()
    text_rect.center = (W / 2,H / 5)
    if text_rect.collidepoint(mouse_click):
        son.stop()
        os.system('main.py')
        pygame.quit()
        sys.exit(0)
    if text_rect.collidepoint(mouse_pos):
        text1_bool = True
    else:
        text1_bool = False
    Surface.blit(text, text_rect)

    color = BLANC
    if text2_bool:
        color = ROUGE
    
    Font = pygame.font.SysFont('arial', 40)
    text = Font.render('Soon',True,color)
    text_rect = text.get_rect()
    text_rect.center = (W / 2,H * 2 / 5)
    if text_rect.collidepoint(mouse_click):
        output = 'Soon'
    if text_rect.collidepoint(mouse_pos):
        text2_bool = True
    else:
        text2_bool = False
    Surface.blit(text, text_rect)

    color = BLANC
    if text3_bool:
        color = ROUGE
    
    Font = pygame.font.SysFont('arial', 40)
    text = Font.render('Quitter',True,color)
    text_rect = text.get_rect()
    text_rect.center = (W / 2,H * 3 / 5)
    if text_rect.collidepoint(mouse_click):
            pygame.quit()
            sys.exit(0)
    if text_rect.collidepoint(mouse_pos):
        text3_bool = True
    else:
        text3_bool = False
    Surface.blit(text, text_rect)


    Font = pygame.font.SysFont('arial', 40)
    text = Font.render(output,True,BLUE)
    text_rect = text.get_rect()
    text_rect.center = (W / 2,H * 4 / 5)
    Surface.blit(text, text_rect)


    pygame.display.flip()
    mainClock.tick(100000)
