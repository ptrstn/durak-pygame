import pygame

from durakui.settings import (
    CARD_FONT_NAME,
    CARD_FONT_SIZE,
    CARD_SUIT_FONT_NAME,
    CARD_SUIT_FONT_SIZE,
    CARD_CENTER_FONT_SIZE,
    CARD_BACKGROUND_COLOR,
    CARD_WIDTH,
    CARD_HEIGHT,
    CARD_RADIUS,
    CARD_BORDER_COLOR,
    CARD_INNER_RECT_WIDTH_SCALE,
    CARD_INNER_RECT_HEIGHT_SCALE,
    CARD_INNER_RECT_COLOR,
    CARD_INNER_RECT_THICKNESS,
    CARD_TEXT_COLORS,
    CARD_CORNER_TEXT_MARGIN_LEFT,
    CARD_CORNER_TEXT_MARGIN_TOP,
)

pygame.init()


class Card:
    FONT_CORNER_VALUE = pygame.font.SysFont(CARD_FONT_NAME, CARD_FONT_SIZE)
    FONT_CORNER_SUIT = pygame.font.SysFont(CARD_SUIT_FONT_NAME, CARD_SUIT_FONT_SIZE)
    FONT_CENTER = pygame.font.SysFont(CARD_SUIT_FONT_NAME, CARD_CENTER_FONT_SIZE)

    def __init__(self, value="3", suit="♦"):
        self.surface = Card._draw_card(value, suit)

    @staticmethod
    def _draw_card_background_on_surface(surface):
        pygame.draw.rect(
            surface,
            color=CARD_BACKGROUND_COLOR,
            rect=pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT),
            border_radius=CARD_RADIUS,
        )
        pygame.draw.rect(
            surface,
            color=CARD_BORDER_COLOR,
            rect=pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT),
            border_radius=CARD_RADIUS,
            width=1,
        )

    @staticmethod
    def _draw_inner_rectangle_on_surface(surface):
        rect = surface.get_rect()
        inner_rectangle = pygame.Rect(
            0,
            0,
            CARD_WIDTH / CARD_INNER_RECT_WIDTH_SCALE,
            CARD_HEIGHT / CARD_INNER_RECT_HEIGHT_SCALE,
        )
        inner_rectangle.center = rect.center

        pygame.draw.rect(
            surface,
            CARD_INNER_RECT_COLOR,
            inner_rectangle,
            width=CARD_INNER_RECT_THICKNESS,
        )

    @staticmethod
    def _draw_text_on_surface(surface, value, suit):
        text_color = CARD_TEXT_COLORS[suit]

        text_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)

        text_value_surface = Card.FONT_CORNER_VALUE.render(value, True, text_color)
        text_suit_surface = Card.FONT_CORNER_SUIT.render(suit, True, text_color)

        text_surface.blit(
            text_value_surface,
            (CARD_CORNER_TEXT_MARGIN_LEFT, CARD_CORNER_TEXT_MARGIN_TOP),
        )

        text_surface.blit(
            text_suit_surface,
            (
                CARD_CORNER_TEXT_MARGIN_LEFT,
                CARD_CORNER_TEXT_MARGIN_TOP + CARD_FONT_SIZE,
            ),
        )

        rotated_text_surface = pygame.transform.rotate(text_surface, 180)
        text_surface.blit(rotated_text_surface, (0, 0))

        text_center_suit_surface = Card.FONT_CENTER.render(suit, True, text_color)
        text_center_suit_rect = text_center_suit_surface.get_rect(
            center=(CARD_WIDTH / 2, CARD_HEIGHT / 2)
        )

        text_surface.blit(rotated_text_surface, (0, 0))
        text_surface.blit(text_center_suit_surface, text_center_suit_rect)

        surface.blit(text_surface, (0, 0))

    @staticmethod
    def _draw_card(value, suit):
        surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
        Card._draw_card_background_on_surface(surface)
        Card._draw_inner_rectangle_on_surface(surface)
        Card._draw_text_on_surface(surface, value, suit)

        return surface
