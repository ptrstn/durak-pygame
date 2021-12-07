import sys

import pygame

from durakui.card import Card
from durakui.settings import SCREEN_WIDTH, SCREEN_HEIGHT, CARD_ANGLE


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Durak")
    clock = pygame.time.Clock()

    background_surface = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
    background_surface.fill("lightgreen")

    card1 = Card("2", "♠").surface
    card2 = Card("7", "♠").surface
    card2 = pygame.transform.rotate(card2, angle=CARD_ANGLE)

    card3 = Card("8", "♥").surface
    card4 = Card("K", "♥").surface
    card4 = pygame.transform.rotate(card4, angle=CARD_ANGLE)

    card5 = Card("10", "♣").surface
    card6 = Card("Q", "♣").surface
    card6 = pygame.transform.rotate(card6, angle=CARD_ANGLE)

    card7 = Card("A", "♦").surface

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background_surface, (0, 0))
        screen.blit(card1, (10, 10))
        screen.blit(card2, (10, 10))
        screen.blit(card3, (200, 10))
        screen.blit(card4, (200, 10))
        screen.blit(card5, (400, 10))
        screen.blit(card6, (400, 10))
        screen.blit(card7, (600, 10))

        pygame.display.update()
        clock.tick(60)  # max 60 loops per second


if __name__ == "__main__":
    main()
