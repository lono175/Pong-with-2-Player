import sys,pygame
pygame.init()
size = width,height=200, 400
speed = [2,2]
barSpeed = [10, 0]
white = 255,255,255
black = 0, 0, 0
clock=pygame.time.Clock()

#set key repeat interval
delay = 300
interval = 50
pygame.key.set_repeat(delay, interval)
screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.bmp")
bar = pygame.image.load("bar.bmp")
ballRect = ball.get_rect()
barRect = bar.get_rect()
barRect.top = 200

while 1:

    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                sys.exit(0)

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
               barRect = barRect.move([-barSpeed[0], -barSpeed[1]]) 
            if event.key==pygame.K_RIGHT:
               barRect = barRect.move(barSpeed) 

    if ballRect.colliderect(barRect):
        speed[1] = -speed[1]
    ballRect = ballRect.move(speed)
    if ballRect.left < 0 or ballRect.right > width:
        speed[0] = -speed[0]
    if ballRect.top < 0 or ballRect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball,ballRect)
    screen.blit(bar,barRect)
    pygame.display.flip()
