import pygame

pygame.init()
size = width, height = 300, 300
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Worlds hardest game!!!!!!!')


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color("white"))
    pygame.display.flip()

pygame.quit()
