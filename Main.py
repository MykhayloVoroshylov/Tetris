import pygame
from random import randint

pygame.init()
fps = pygame.time.Clock()
screen = pygame.display.set_mode((500,600)) 
icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(icon)

bg = pygame.image.load('assets/images/background.png')
bg = pygame.transform.scale(bg,(300,600))

bg_sound = pygame.mixer.Sound('assets/sounds/Yihav_kozak_za_dunai.mp3')
bg_sound.play(-1)


Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    screen.blit(bg, (0,0))
    



    pygame.display.update()

pygame.quit()
