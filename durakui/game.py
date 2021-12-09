import sys

import pygame

from durakui.areas import (
    TableArea,
    BackgroundArea,
    DeckArea,
    HandArea,
    OpponentHandArea,
)
from durakui.cards import (
    Hand,
    AngledCard,
    CardBack,
    TableCardGroup,
    OpponentHand,
)
from durakui.constants import HEARTS
from durakui.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    CARD_WIDTH,
    CARD_HEIGHT,
    TABLE_CARD_SPACING,
    MAX_NUMBER_OF_TABLE_CARDS,
    HAND_CARD_SPACING,
)


class DurakGame:
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, title=SCREEN_TITLE):
        self.screen = pygame.display.set_mode((width, height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()

        self.table = TableCardGroup()
        self.hand = Hand([])
        self.opponent_hand = OpponentHand(6)

        self.background_area = BackgroundArea()
        self.table_area = TableArea()
        self.deck_area = DeckArea()
        self.hand_area = HandArea()
        self.opponent_hand_area = OpponentHandArea()

        self._init_cards()

        self.hand_area.rect.centerx = self.screen_rect.centerx
        self.hand_area.rect.bottom = self.screen_rect.bottom

        self.opponent_hand_area.rect.centerx = self.screen_rect.centerx

        self.table_area.rect.center = self.screen_rect.center
        self.table_area.rect.centerx += 50

        self.deck_area.rect.centery = self.screen_rect.centery
        self.deck_area.rect.x = 10

        self.deck_card = CardBack()
        self.deck_card.rect.x = 0
        self.deck_card.rect.y = 0

        self.trump_card = AngledCard(HEARTS, "5", angle=90)
        self.trump_card.rect.x = 12
        self.trump_card.rect.y = (self.trump_card.height - self.trump_card.width) / 2

        self.deck_area.image.blit(self.trump_card.image, self.trump_card.rect)
        self.deck_area.image.blit(self.deck_card.image, self.deck_card.rect)

    def _init_cards(self):
        self.table.attack("♠", "2")
        self.table.attack("♠", "8")
        self.table.defend("♠", "2", "♠", "10")
        self.table.attack("♦", "A")
        self.table.attack("♠", "9")
        self.table.defend("♦", "A", "♣", "2")
        self.table.attack("♥", "K")
        self.table.attack("♠", "3")
        self.table.defend("♠", "3", "♥", "J")

        self.hand = Hand(
            [("♠", "A"), ("♦", "7"), ("♥", "7"), ("♠", "4"), ("♠", "5"), ("♠", "6")]
        )

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.table.attack("♠", "2")
                if event.type == pygame.MOUSEWHEEL:
                    self.table.empty()

            self.screen.blit(self.background_area.image, (0, 0))
            self.screen.blit(self.table_area.image, self.table_area.rect)
            self.screen.blit(self.deck_area.image, self.deck_area.rect)
            self.screen.blit(self.hand_area.image, self.hand_area.rect)
            self.screen.blit(
                self.opponent_hand_area.image, self.opponent_hand_area.rect
            )

            self.hand.update()
            self.hand.draw(self.hand_area.image)

            self.table.update()
            self.table.draw(self.table_area.image)

            self.opponent_hand.update()
            self.opponent_hand.draw(self.opponent_hand_area.image)

            pygame.display.update()
            self.clock.tick(60)  # max 60 loops per second
