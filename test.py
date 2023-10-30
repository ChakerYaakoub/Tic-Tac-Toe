import pygame

from classes.button import *


def my_callback():
    print("Button clicked!")


pygame.init()
screen = pygame.display.set_mode((400, 300))
button = Button(100, 100, 200, 50, "Click Me",
                (0, 128, 255), (255, 255, 255), my_callback)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        button.handle_event(event)

    screen.fill((255, 255, 255))
    button.draw(screen)
    pygame.display.flip()

pygame.quit()
