import pygame

pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color("black"))
    pygame.display.flip()

pygame.quit()
