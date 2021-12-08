import sys

import pygame

from durakui.cards import TableCardGroup
from durakui.settings import SCREEN_WIDTH, SCREEN_HEIGHT


def main():

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Durak")
    clock = pygame.time.Clock()

    background_surface = pygame.Surface(screen.get_size())
    background_surface.fill("lightgreen")

    table = TableCardGroup()

    table.attack("♠", "2")
    table.attack("♠", "8")
    table.defend("♠", "2", "♠", "10")
    table.attack("♦", "A")
    table.defend("♦", "A", "♣", "2")
    table.attack("♥", "K")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                table.attack("♠", "2")
            if event.type == pygame.MOUSEWHEEL:
                table.empty()

        screen.blit(background_surface, (0, 0))
        table.draw(screen)
        table.update()
        pygame.display.update()
        clock.tick(60)  # max 60 loops per second


if __name__ == "__main__":
    main()
