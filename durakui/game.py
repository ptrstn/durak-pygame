import sys

import pygame
from pygame.sprite import Group

from durakui.areas import (
    BattlefieldArea,
    BackgroundArea,
    DeckArea,
    HandArea,
    OpponentHandArea,
)
from durakui.mocks import (
    mock_battlefield,
    mock_hand,
    mock_deck,
    mock_opponent_hand,
    mock_action,
)
from durakui.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
)


class DurakGame(Group):
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE):
        self.screen = pygame.display.set_mode((width, height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        self.background_area = BackgroundArea()
        self.battlefield_area = BattlefieldArea()
        self.deck_area = DeckArea()
        self.hand_area = HandArea()
        self.opponent_hand_area = OpponentHandArea()

        mock_battlefield(self.battlefield_area.battlefield)
        mock_hand(self.hand_area.hand)
        mock_deck(self.deck_area.deck)
        mock_opponent_hand(self.opponent_hand_area.opponent_hand)

        self.hand_area.rect.centerx = self.background_area.rect.centerx
        self.hand_area.rect.bottom = self.background_area.rect.bottom

        self.opponent_hand_area.rect.centerx = self.background_area.rect.centerx

        self.battlefield_area.rect.center = self.background_area.rect.center
        self.battlefield_area.rect.centerx += 50

        self.deck_area.rect.centery = self.background_area.rect.centery
        self.deck_area.rect.x = 10

    def run(self):
        click_counter = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mock_action(self, click_counter)
                    click_counter += 1
                if event.type == pygame.MOUSEWHEEL:
                    self.battlefield_area.battlefield.empty()
                    self.battlefield_area.battlefield.clear(
                        self.battlefield_area.image, BattlefieldArea().image
                    )
                    click_counter = 0

            self.screen.blit(self.background_area.image, (0, 0))
            self.screen.blit(
                self.opponent_hand_area.image, self.opponent_hand_area.rect
            )
            self.screen.blit(self.battlefield_area.image, self.battlefield_area.rect)
            self.screen.blit(self.deck_area.image, self.deck_area.rect)
            self.screen.blit(self.hand_area.image, self.hand_area.rect)

            self.deck_area.deck.update()
            self.deck_area.deck.draw(self.deck_area.image)

            self.hand_area.hand.update()
            self.hand_area.hand.draw(self.hand_area.image)

            self.battlefield_area.battlefield.update()
            self.battlefield_area.battlefield.draw(self.battlefield_area.image)

            self.opponent_hand_area.opponent_hand.update()
            self.opponent_hand_area.opponent_hand.draw(self.opponent_hand_area.image)

            pygame.display.update()
            self.clock.tick(60)  # max 60 loops per second
