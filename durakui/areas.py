import pygame

from durakui.cards import TableCardGroup, Hand, OpponentHand, Deck
from durakui.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CARD_WIDTH,
    CARD_HEIGHT,
    TABLE_CARD_SPACING,
    MAX_NUMBER_OF_TABLE_CARDS,
    TRUMP_CARD_OFFSET,
    CARD_DIAGONAL,
)

BACKGROUND_AREA_WIDTH = SCREEN_WIDTH
BACKGROUND_AREA_HEIGHT = SCREEN_HEIGHT

HAND_AREA_WIDTH = SCREEN_WIDTH
HAND_AREA_HEIGHT = CARD_HEIGHT * 1.15

OPPONENT_HAND_AREA_WIDTH = CARD_DIAGONAL * 2
OPPONENT_HAND_AREA_HEIGHT = CARD_DIAGONAL * 2

DECK_AREA_WIDTH = CARD_HEIGHT + TRUMP_CARD_OFFSET
DECK_AREA_HEIGHT = CARD_HEIGHT


class BackgroundArea(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = BACKGROUND_AREA_WIDTH
        self.height = BACKGROUND_AREA_HEIGHT
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill("Maroon")


class TableArea(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = (CARD_WIDTH + TABLE_CARD_SPACING) * MAX_NUMBER_OF_TABLE_CARDS
        self.height = CARD_HEIGHT * 1.15
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill("Blue")

        self.table = TableCardGroup()


class DeckArea(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = DECK_AREA_WIDTH
        self.height = DECK_AREA_HEIGHT
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill("Green")

        self.deck = Deck()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.deck.update()
        self.deck.draw(self.image)


class HandArea(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = HAND_AREA_WIDTH
        self.height = HAND_AREA_HEIGHT
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill("Pink")

        self.hand = Hand()


class OpponentHandArea(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = OPPONENT_HAND_AREA_WIDTH
        self.height = OPPONENT_HAND_AREA_HEIGHT
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.image.fill("Purple")

        self.opponent_hand = OpponentHand()
