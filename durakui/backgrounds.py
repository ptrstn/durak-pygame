import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface

from durakui.settings import (
    TABLE_BACKGROUND_WIDTH,
    TABLE_BACKGROUND_HEIGHT,
    BATTLEFIELD_WIDTH,
    BATTLEFIELD_HEIGHT,
    TABLE_BACKGROUND_COLOR,
    DECK_BACKGROUND_WIDTH,
    DECK_BACKGROUND_HEIGHT,
    HAND_BACKGROUND_HEIGHT,
    HAND_BACKGROUND_WIDTH,
    OPPONENT_BACKGROUND_WIDTH,
    OPPONENT_BACKGROUND_HEIGHT,
)


class Background(Sprite):
    def __init__(self, width, height, color=None):
        super().__init__()
        self.image = Surface((width, height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        if color:
            self.image.fill(color)


class BattlefieldBackground(Background):
    def __init__(self):
        super().__init__(
            width=BATTLEFIELD_WIDTH,
            height=BATTLEFIELD_HEIGHT,
            # color=BATTLEFIELD_BACKGROUND_COLOR,
        )


class DeckBackground(Background):
    def __init__(self):
        super().__init__(
            width=DECK_BACKGROUND_WIDTH,
            height=DECK_BACKGROUND_HEIGHT,
            # color=DECK_BACKGROUND_COLOR,
        )


class HandBackground(Background):
    def __init__(self):
        super().__init__(
            width=HAND_BACKGROUND_WIDTH,
            height=HAND_BACKGROUND_HEIGHT,
            # color=HAND_BACKGROUND_COLOR,
        )


class OpponentBackground(Background):
    def __init__(self):
        super().__init__(
            width=OPPONENT_BACKGROUND_WIDTH,
            height=OPPONENT_BACKGROUND_HEIGHT,
            # color=OPPONENT_BACKGROUND_COLOR,
        )


class TableBackground(Background):
    def __init__(self):
        super().__init__(
            width=TABLE_BACKGROUND_WIDTH,
            height=TABLE_BACKGROUND_HEIGHT,
            color=TABLE_BACKGROUND_COLOR,
        )
