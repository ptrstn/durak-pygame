import sys

import pygame

from durakui.cards import (
    TableCardGroup,
    Hand,
    AngledCard,
    BaseCard,
    CardBack,
    OpponentHand,
)
from durakui.constants import SPADES, CLUBS, HEARTS
from durakui.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    TABLE_BACKGROUND_COLOR,
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

        self._init_cards()

        self.background = pygame.Surface((width, height))
        self.background.fill("Maroon")  # "Maroon"

        self.hand_area = pygame.Surface(
            ((CARD_WIDTH + HAND_CARD_SPACING) * len(self.hand), CARD_HEIGHT * 1.15),
            pygame.SRCALPHA,
        )
        # self.hand_area.fill("blue")
        self.hand_area_rect = self.hand_area.get_rect()
        self.hand_area_rect.centerx = self.screen_rect.centerx
        self.hand_area_rect.bottom = self.screen_rect.bottom

        self.opponent_area = pygame.Surface(
            (CARD_WIDTH * 2, CARD_HEIGHT * 2), pygame.SRCALPHA
        )
        # self.hand_area.fill("blue")
        self.opponent_area_rect = self.opponent_area.get_rect()
        self.opponent_area_rect.centerx = self.screen_rect.centerx

        self.table_area = pygame.Surface(
            (
                (CARD_WIDTH + TABLE_CARD_SPACING) * MAX_NUMBER_OF_TABLE_CARDS,
                CARD_HEIGHT * 1.15,
            ),
            pygame.SRCALPHA,
        )
        # self.table_area.fill("red")
        self.table_area_rect = self.table_area.get_rect()
        self.table_area_rect.center = self.screen_rect.center
        self.table_area_rect.centerx += 50

        self.deck_area = pygame.Surface(
            (CARD_HEIGHT + 12, CARD_HEIGHT), pygame.SRCALPHA
        )
        # self.deck_area.fill("lightblue")
        self.deck_area_rect = self.deck_area.get_rect()
        self.deck_area_rect.centery = self.screen_rect.centery
        self.deck_area_rect.x = 10

        self.deck_card = CardBack()
        self.deck_card.rect.x = 0
        self.deck_card.rect.y = 0

        self.trump_card = AngledCard(HEARTS, "5", angle=90)
        self.trump_card.rect.x = 12
        self.trump_card.rect.y = (self.trump_card.height - self.trump_card.width) / 2

        self.deck_area.blit(self.trump_card.image, self.trump_card.rect)
        self.deck_area.blit(self.deck_card.image, self.deck_card.rect)

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

            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.table_area, self.table_area_rect)
            self.screen.blit(self.deck_area, self.deck_area_rect)
            self.screen.blit(self.hand_area, self.hand_area_rect)
            self.screen.blit(self.opponent_area, self.opponent_area_rect)

            self.hand.update()
            self.hand.draw(self.hand_area)

            self.table.update()
            self.table.draw(self.table_area)

            self.opponent_hand.update()
            self.opponent_hand.draw(self.opponent_area)

            pygame.display.update()
            self.clock.tick(60)  # max 60 loops per second
