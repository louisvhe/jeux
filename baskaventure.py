import pygame
import random


pygame.init()

pygame.display.set_caption('basketball adventure')
icon = pygame.image.load('watermelon.png')
pygame.display.set_icon(icon)
screen_width = 800
screen_height = 800
clock = pygame.time.Clock()
background = pygame.image.load("image.png")
background1 = pygame.transform.scale(background, (800,800))
WHITE = (255, 255, 255)
BLACK = ( 0, 0, 0)
purpule = (212, 25, 209)
RED = (212, 25, 34)
# x et y position 
x_position = 150
y_position = 780
# load the image
hero = pygame.image.load("ballon-de-basket.png")
hero1 = pygame.transform.scale(hero, (150, 150))
# get rect surrounding the image
hero_rect = hero1.get_rect()
# position the image
hero_rect.bottomright = (x_position, y_position)


gravity = 1
y_height = 25
y_vel = y_height
jumping = False

###########################################################################
boss = pygame.image.load("boss-final.png")
boss1 = pygame.transform.scale(boss, (140, 140))
boss_rect = boss1.get_rect()
boss_rect.bottomleft = (750, 790)

lose = False
active = True
x_vel = 10
i = 0
score = 0


screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
font = pygame.font.Font('freesansbold.ttf', 32)

###############################################################################""
#game loop 
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #screen.fill((0,255,255))
    screen.blit(background1, (0,0))
    score_text = font.render(f'score: {score}', True, WHITE, purpule)
    screen.blit(score_text, (330,100))
    if lose:
        text = font.render(f'Game Over ', RED, RED)
        screen.blit(text, (300,200))
    screen.blit(hero1, hero_rect)
    screen.blit(boss1, boss_rect)
    


    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_SPACE]:
        jumping = True
        
        
        
    if jumping:
        hero_rect.y -= y_vel
        y_vel -= gravity
        if y_vel < -y_height:
            jumping = False
            y_vel = y_height
    
    if active:
        boss_rect.x -= x_vel
        
        if boss_rect.x < -5:
            boss_rect.x = random.randint(800, 800)
            score += 1
        if hero_rect.colliderect(boss_rect):
            active = False
            lose =True


    if key_pressed[pygame.K_d]:
        hero_rect.x += 5
    if key_pressed[pygame.K_q]:
        hero_rect.x -= 5
    

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
