##################################
# GameOfLife: v1.0
# By: @Tinchoram
# CodeSource: 
# Source: @dotcsv https://www.youtube.com/watch?v=qPtKv9fSHZY  
# Date: 2020-04-22
##################################


#################
# Se deben instalar librerias con Pip
# Instalar ambiente virtual
# pip install numpy
# pip install pygame
#####IMPORTs#####
import pygame
import numpy as np
import time 



#####SET GAME#####

##Start pygme
pygame.init()

#Titulo de la ventana
pygame.display.set_caption('Game of Life')

#configuro tamaño de pantalla
width, height = 500, 500
screen = pygame.display.set_mode((width,height))

#Color de pantalla
bg = 25,25,25
screen.fill(bg)

#Numero de celdas
#nxC,nyC = 25,25
nxC,nyC = 50,50
#Tamaño de la celdas
dimCW = width / nxC
dimCH = height /nyC

# Establecemos la celda: vivas = 1 - Muertas = 0
gameState = np.zeros((nxC, nyC))


#####AUTOMATAS DEMO#####
###Automatas Predefinidos al iniciar: 
# PALO
gameState[5,3] = 1
gameState[5,4] = 1
gameState[5,5] = 1

###Automata que se mueve
gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1

##Variable para controlar RUN del juego
pueseExect = False
running = True

#####DASHBOARD#####
white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128)

#Ubicacion
Xd = 380
Yd = 480
generation = 0
font = pygame.font.Font('freesansbold.ttf', 17)
text = font.render('Generacion: ' + str(generation), True, green, blue) 
textRect = text.get_rect()  
textRect.center = (Xd , Yd ) 

#####START GAME#####
#Bucle infinito para mantener abierta la ventana
while running:

    #Creo una copia del estado del juego
    newGameState = np.copy(gameState) 
    #Refresco pantalla
    screen.fill(bg) 
    screen.blit(text, textRect) 

    ####################INTERACCION_LEO_EVENTOS######################
    #Registramos eventos en de teclado y mouse
    # retorna un solo evento de la cola de eventos
    #event = pygame.event.poll()
    #pygame.event.wait()    
    
    ###get lista de eventos
    event = pygame.event.get()
    ### Leo la lista
    for ev in event:

        ##Si presiona alguna tecla pauso
        if ev.type == pygame.KEYDOWN:
            pueseExect = not pueseExect
            

        #Detectamos si se presiona el mouse
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            #Get ubicacion
            posX, posY = pygame.mouse.get_pos()
            celX, CelY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            #set Celda
            newGameState[celX,CelY] = not mouseClick[2]


        # si se presiona el botón 'cerrar' de la ventana
        if ev.type == pygame.QUIT:
            # detiene el bucle
            running = False

    ######START Update Generacion######
    if not pueseExect:
        generation += 1

    for y in range(0,nxC):
        for x in range(0,nyC):
            
            ##controlo si el juego esta pausado o no
            if not pueseExect:
                #Verifico vecinos cercanos
                n_neigh = gameState [(x-1) % nxC, (y-1) % nyC] + \
                        gameState [(x)   % nxC, (y-1) % nyC] + \
                        gameState [(x+1) % nxC, (y-1) % nyC] + \
                        gameState [(x-1) % nxC, (y)   % nyC] + \
                        gameState [(x+1) % nxC, (y)   % nyC] + \
                        gameState [(x-1) % nxC, (y+1) % nyC] + \
                        gameState [(x)   % nxC, (y+1) % nyC] + \
                        gameState [(x+1) % nxC, (y+1) % nyC]

                #Rule 1: Una celula muerta con 3 vecinas vivas "revive"
                if gameState[x,y] == 0 and n_neigh == 3:
                    newGameState[x,y] = 1
                
                #Rule 2: Una celula viva con menos de 2 o mas de 3 vecinas vivas "Muere"
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x,y] = 0

            #Dibujamos la celda para cada par de x e y
            poly = [((x) * dimCW, y * dimCH), 
                    ((x+1) * dimCW, y * dimCH), 
                    ((x+1) * dimCW, (y+1) * dimCH), 
                    ((x) * dimCW, (y+1) * dimCH) ]

            if newGameState[x,y] == 0:
                pygame.draw.polygon(screen,(128,128,128),poly,1)
            else:
                pygame.draw.polygon(screen,(255,255,255),poly,0)
    
    #Actualizamos el estado del juego
    
    text = font.render('Generacion: ' + str(generation), True, green, blue) 
    gameState = np.copy(newGameState)
    time.sleep(0.03)
    pygame.display.flip()


#finaliza Pygame
pygame.quit()
