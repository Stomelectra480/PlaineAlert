import pygame
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

#On met en place notre Fenetre
W, H = 1280, 720
fenetre = pygame.display.set_mode((W,H))
pygame.display.set_caption('PlaineAlert')

#Collage du Fond
fond = pygame.image.load('images/bg.png').convert()
fondX = 0
fondX2 = fond.get_width()

clock = pygame.time.Clock()



class Joueur(object):
    """Il nous permetra de configurer les caractéristique et animations du joueur et tout les paramètres pour jouer"""
    
    courir = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,16)]
    Saut = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1,8)]
    glisser = [pygame.image.load(os.path.join('images', 'S1.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    Tombe = pygame.image.load(os.path.join('images','0.png'))
    ListSaut = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]

    def __init__(self, x, y, Largeur, Hauteur):
        """Paramétre du personnage et cet coordonnées """
        
        self.x = x
        self.y = y
        self.Largeur = Largeur
        self.Hauteur = Hauteur
        self.Sauter = False
        self.SeGlisser = False
        self.tomber = False
        self.Tempsol = 0
        self.Tempsaut = 0
        self.tempCourse = 0
        self.Glisserhaut = False

    def dessine(self, fenetre):
        """Cet fonctions permet de coller Tout les images du personnage pour chaque actions différents"""

        #Positions du personnage
        if self.tomber:
            fenetre.blit(self.Tombe, (self.x, self.y + 30))

        #Colle les image en rapport avec l'action effectuer Sauter
        elif self.Sauter:
            self.y -= self.ListSaut[self.Tempsaut] * 1.3
            fenetre.blit(self.Saut[self.Tempsaut//18], (self.x,self.y))
            self.Tempsaut += 1
            if self.Tempsaut > 108:
                self.Tempsaut = 0
                self.Sauter = False
                self.tempCourse = 0
            self.hitbox = (self.x+ 4,self.y,self.Largeur-24,self.Hauteur-10)
            
        #Colle les image en rapport avec l'action effectuer Glisser
        elif self.SeGlisser or self.Glisserhaut:
            if self.Tempsol < 20:
                self.y += 1
                self.hitbox = (self.x+ 4,self.y,self.Largeur-24,self.Hauteur-10)
            elif self.Tempsol == 80:
                self.y -= 19
                self.SeGlisser = False
                self.Glisserhaut = True
            elif self.Tempsol > 20 and self.Tempsol < 80:
                self.hitbox = (self.x,self.y+3,self.Largeur-8,self.Hauteur-35)
                
            if self.Tempsol >= 110:
                self.Tempsol = 0
                self.tempCourse = 0
                self.Glisserhaut = False
                self.hitbox = (self.x+ 4,self.y,self.Largeur-24,self.Hauteur-10)
            fenetre.blit(self.glisser[self.Tempsol//10], (self.x,self.y))
            self.Tempsol += 1

        else:
            #Position de base ou le personnage Coure
            if self.tempCourse > 42:
                self.tempCourse = 0
            fenetre.blit(self.courir[self.tempCourse//6], (self.x,self.y))
            self.tempCourse += 1
            self.hitbox = (self.x+ 4,self.y,self.Largeur-24,self.Hauteur-13)
 




class Piege(object):
    """Cet fonction va gérer les pieges pour que tout les pièges soit pareil"""

    #Recolte les photos pour l'animations du saut
    rotation = [pygame.image.load(os.path.join('images', 'SAW0.PNG')),pygame.image.load(os.path.join('images', 'SAW1.PNG')),pygame.image.load(os.path.join('images', 'SAW2.PNG')),pygame.image.load(os.path.join('images', 'SAW3.PNG'))]

    def __init__(self, x, y, Largeur, Hauteur):
        """Paramètre de base du pièges"""
        self.x = x
        self.y = y
        self.Largeur = Largeur
        self.Hauteur = Hauteur
        self.rotateCount = 0
        self.vel = 1.4

    #on place une HitBox et on ajoute l'animations pour le pièges
    def dessine(self,fenetre):
        self.hitbox = (self.x + 10, self.y + 5, self.Largeur - 20, self.Hauteur - 5)
        if self.rotateCount >= 8:
            self.rotateCount = 0
        fenetre.blit(pygame.transform.scale(self.rotation[self.rotateCount//2], (64,64)), (self.x,self.y))
        self.rotateCount += 1

    #On vérifie les collision entre le joueur et la hitbox
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False




#cet fonction vas mettre a jour le fichier Score si le joueur effectue un score plus élevé
def MiseAjour():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0]) #Lit le score dans le Fichier

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

        return score
               
    return last



#Cet fonction vas mettre en place le scores, et l'interface pour savoir si on a dépasse oui ou non le score
def Score():
    global pause, score, Vitesse, obstacles
    pause = 0
    Vitesse = 200
    obstacles = []
                   
    coure = True
    while coure:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                coure = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                coure = False
                EnCourse.tomber = False
                EnCourse.SeGlisser = False
                EnCourse.Sauter = False
                
        fenetre.blit(fond, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        AncienScore = largeFont.render('Meilleur Score: ' + str(MiseAjour()),1,(0,0,255))
        ScoreActuel = largeFont.render('Score atteint: '+ str(score),1,(0,0,0))
        fenetre.blit(AncienScore, (W/2 - AncienScore.get_width()/2,150))
        fenetre.blit(ScoreActuel, (W/2 - ScoreActuel.get_width()/2, 240))
        pygame.display.update()
    score = 0

        

#Cet fonction vas positionner le score sur l'ecran
def initialisation():
    largeFont = pygame.font.SysFont('comicsans', 30)
    fenetre.blit(fond, (fondX, 0))
    fenetre.blit(fond, (fondX2,0))
    text = largeFont.render('Score: ' + str(score), 1, (0,0,255))
    EnCourse.dessine(fenetre)
    for obstacle in obstacles:
        obstacle.dessine(fenetre)

    fenetre.blit(text, (700, 10))
    pygame.display.update()

#définie les point pour second et la vitesse du jeux
pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, 3000)
Vitesse = 200

score = 0

coure = True

#Le joueur vas courir
EnCourse = Joueur(100, 527, 64, 64)

obstacles = []
pause = 0
vitessTomber = 0

#Initialisations du score et de la vitesse quand le personnage retombe
while coure:
    if pause > 0:
        pause += 1
        if pause > vitessTomber * 2:
            Score()
        
    score = Vitesse//10 - 20

    #On met en place les piéges et leur positions sur l'ecran
    for obstacle in obstacles:
        if obstacle.collide(EnCourse.hitbox):
            EnCourse.tomber = True
            
            if pause == 0:
                pause = 1
                vitessTomber = Vitesse
        if obstacle.x < -64:
            obstacles.pop(obstacles.index(obstacle))
        else:
            obstacle.x -= 1.4
    
    fondX -= 1.4
    fondX2 -= 1.4

    if fondX < fond.get_width() * -1:
        fondX = fond.get_width()
    if fondX2 < fond.get_width() * -1:
        fondX2 = fond.get_width() 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            coure = False
            
        #La vitesse du jeux accéler progressivement
        if event.type == USEREVENT+1:
            Vitesse += 1

        #Fréquence d'apparition en cours du jeux
        if event.type == USEREVENT+2:
            r = random.randrange(0,1)
            if r == 0:
                obstacles.append(Piege(810, 527, 64, 64))

                
    if EnCourse.tomber == False:
        k = pygame.key.get_pressed()

        #Configure la touche ESPACE et la touche HAUT  pour sauter
        if k[pygame.K_SPACE] or k[pygame.K_UP]:
            if not(EnCourse.Sauter):
                EnCourse.Sauter = True

        #Configure la touche BAS pour glisser
        if k[pygame.K_DOWN]:
            if not(EnCourse.SeGlisser):
                EnCourse.SeGlisser = True
    
    clock.tick(Vitesse)
    initialisation()
