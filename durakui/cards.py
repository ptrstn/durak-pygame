import pygame
from pygame.sprite import Sprite, Group
from pygame.surface import Surface

from durakui.constants import HAMMER_AND_SICKLE, COMMUNIST_RED, COMMUNIST_YELLOW
from durakui.settings import (
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
    CARD_FONT_SIZE,
    CARD_FONT_NAME,
    CARD_SUIT_FONT_NAME,
    CARD_SUIT_FONT_SIZE,
    CARD_CENTER_FONT_SIZE,
    CARD_DEFEND_ANGLE,
    HAND_CARD_SPACING,
    BATTLEFIELD_CARD_SPACING,
    TRUMP_CARD_ANGLE,
    TRUMP_CARD_OFFSET,
    CARD_DIAGONAL,
    OPPONENT_CARD_ANGLE,
)
from durakui.utils import calculate_rotation_offset, elementwise_add

pygame.init()


class BaseCard(Sprite):
    """
    Represents an empty card
    """

    def __init__(
        self, width=CARD_WIDTH, height=CARD_HEIGHT, base_color=CARD_BACKGROUND_COLOR
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.base_color = base_color
        self.image = Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self._draw_base_card()

    def _draw_base_card(self):
        pygame.draw.rect(
            self.image,
            color=self.base_color,
            rect=pygame.rect.Rect(0, 0, self.width, self.height),
            border_radius=CARD_RADIUS,
        )
        pygame.draw.rect(
            self.image,
            color=CARD_BORDER_COLOR,
            rect=pygame.rect.Rect(0, 0, self.width, self.height),
            border_radius=CARD_RADIUS,
            width=1,
        )


class BaseCardFront(BaseCard):
    """
    Represents the front of a card with no value
    """

    def __init__(self):
        super().__init__()

        inner_rectangle = pygame.Rect(
            0,
            0,
            self.width / CARD_INNER_RECT_WIDTH_SCALE,
            self.height / CARD_INNER_RECT_HEIGHT_SCALE,
        )
        inner_rectangle.center = self.rect.center

        pygame.draw.rect(
            self.image,
            CARD_INNER_RECT_COLOR,
            inner_rectangle,
            width=CARD_INNER_RECT_THICKNESS,
        )


class Card(BaseCardFront):
    FONT_CORNER_VALUE = pygame.font.SysFont(CARD_FONT_NAME, CARD_FONT_SIZE)
    FONT_CORNER_SUIT = pygame.font.SysFont(CARD_SUIT_FONT_NAME, CARD_SUIT_FONT_SIZE)
    FONT_CENTER = pygame.font.SysFont(CARD_SUIT_FONT_NAME, CARD_CENTER_FONT_SIZE)

    def __init__(self, suit, value):
        super().__init__()
        self.suit = suit
        self.value = value
        text_color = CARD_TEXT_COLORS[self.suit]

        text_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        text_value_surface = Card.FONT_CORNER_VALUE.render(self.value, True, text_color)
        text_suit_surface = Card.FONT_CORNER_SUIT.render(self.suit, True, text_color)

        text_surface.blit(
            text_value_surface,
            (CARD_CORNER_TEXT_MARGIN_LEFT, CARD_CORNER_TEXT_MARGIN_TOP),
        )

        text_surface.blit(
            text_suit_surface,
            (
                CARD_CORNER_TEXT_MARGIN_LEFT,
                CARD_CORNER_TEXT_MARGIN_TOP + CARD_FONT_SIZE - 5,
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

        self.image.blit(text_surface, (0, 0))


class AngledCard(Card):
    def __init__(self, suit, value, angle):
        super().__init__(suit, value)
        self.image = pygame.transform.rotate(self.image, angle=angle)


class CardBack(BaseCard):
    FONT_CENTER = pygame.font.SysFont("DejaVu Sans", CARD_CENTER_FONT_SIZE)

    def __init__(self, base_color="WhiteSmoke", symbol=HAMMER_AND_SICKLE):
        super().__init__(base_color=base_color)
        inner_rectangle = pygame.Rect(
            0,
            0,
            self.width - 25,
            self.height - 25,
        )
        inner_rectangle.center = self.rect.center

        pygame.draw.rect(
            self.image, color=COMMUNIST_RED, rect=inner_rectangle, border_radius=5
        )

        inner_inner_rectangle = pygame.Rect(
            0,
            0,
            self.width - 40,
            self.height - 40,
        )
        inner_inner_rectangle.center = self.rect.center

        pygame.draw.rect(
            self.image,
            color=COMMUNIST_YELLOW,
            rect=inner_inner_rectangle,
            width=2,
        )

        symbol_surface = CardBack.FONT_CENTER.render(symbol, True, COMMUNIST_YELLOW)
        symbol_surface_rect = symbol_surface.get_rect(
            center=(CARD_WIDTH / 2, CARD_HEIGHT / 2)
        )

        self.image.blit(symbol_surface, symbol_surface_rect)


class AngledCardBack(CardBack):
    def __init__(self, angle):
        super().__init__()
        self.original = self.image
        self.image = pygame.transform.rotate(self.original, angle=angle)
        self.pivot = (0, CARD_HEIGHT)
        self.offset = calculate_rotation_offset(
            self.original, angle=angle, pivot=self.pivot
        )
        self.rect = self.image.get_rect(
            topleft=elementwise_add(
                (CARD_DIAGONAL, CARD_DIAGONAL - CARD_HEIGHT), self.offset
            )
        )


class Battlefield(Group):
    """
    Represents the cards that were put on the table.
    Consists of attack cards and defend cards.
    """

    def __init__(self, spacing=BATTLEFIELD_CARD_SPACING):
        super().__init__()
        self.spacing = spacing
        self.cards = {}
        self.current_position = 0

    def _init_card_dict_attack_position(self, position):
        self.cards[position] = {
            "attack": {"suit": None, "value": None, "card": None},
        }

    def attack(self, suit, value):
        card = Card(suit, value)
        self._init_card_dict_attack_position(self.current_position)
        self.cards[self.current_position]["attack"] = {
            "suit": suit,
            "value": value,
            "card": card,
        }

        card.rect.topleft = (
            (card.width + self.spacing) * self.current_position,
            0,
        )

        self.add(card)
        self.current_position += 1

    def _find_attack_position(self, suit, value):
        for position, card_pair in self.cards.items():
            attack_card = card_pair.get("attack")
            if attack_card.get("suit") == suit and attack_card.get("value") == value:
                return position
        raise LookupError(f"Attack card '{suit}{value}' not found")

    def defend(self, attack_suit, attack_value, defend_suit, defend_value):
        defend_card = AngledCard(defend_suit, defend_value, angle=CARD_DEFEND_ANGLE)
        defend_position = self._find_attack_position(attack_suit, attack_value)
        self.cards[defend_position]["defend"] = {
            "suit": defend_suit,
            "value": defend_value,
            "card": defend_card,
        }

        defend_card.rect.topleft = (
            (defend_card.width + self.spacing) * defend_position,
            0,
        )
        self.add(defend_card)

    def empty(self):
        super().empty()
        self.cards = {}
        self.current_position = 0


def split_suit_value(suit_value):
    return suit_value[0], suit_value[1:]


class Hand(Group):
    def __init__(self, suit_value_pairs: list = None, spacing=HAND_CARD_SPACING):
        super().__init__()
        self.spacing = spacing
        self.set_hand(suit_value_pairs)

    def set_hand(self, suit_value_pairs: list):
        if suit_value_pairs:
            self.empty()
            for position, suit_value_pair in enumerate(suit_value_pairs):
                card = Card(*suit_value_pair)
                card.rect.topleft = (
                    (card.width + self.spacing) * position,
                    0,
                )
                self.add(card)


class OpponentHand(Group):
    def __init__(self, angle=OPPONENT_CARD_ANGLE):
        super().__init__()
        self.number_of_cards = 0
        self.angle = angle

    def set_hand(self, number_of_cards: int):
        self.empty()
        self.number_of_cards = number_of_cards
        start_angle = int(number_of_cards / 2 + 1) * (self.angle)
        for idx in range(0, number_of_cards):
            angle = start_angle - self.angle * idx
            card = AngledCardBack(angle=angle)
            self.add(card)


class Deck(Group):
    def __init__(self):
        super().__init__()
        self.deck_card = CardBack()
        self.trump_card = BaseCard()

    def set_trump_card(self, suit, value):
        self.trump_card = AngledCard(suit, value, angle=TRUMP_CARD_ANGLE)
        self.trump_card.rect.x = TRUMP_CARD_OFFSET
        self.trump_card.rect.y = (self.trump_card.height - self.trump_card.width) / 2
        self.empty()
        self.add(self.trump_card)
        self.add(self.deck_card)

    def remove_deck_card(self):
        self.remove(self.deck_card)
