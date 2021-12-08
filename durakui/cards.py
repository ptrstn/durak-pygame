import pygame

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
)

pygame.init()


class BaseCard(pygame.sprite.Sprite):
    """
    Represents an empty card
    """

    def __init__(self, width=CARD_WIDTH, height=CARD_HEIGHT):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self._draw_base_card()

    def _draw_base_card(self):
        pygame.draw.rect(
            self.image,
            color=CARD_BACKGROUND_COLOR,
            rect=pygame.Rect(0, 0, self.width, self.height),
            border_radius=CARD_RADIUS,
        )
        pygame.draw.rect(
            self.image,
            color=CARD_BORDER_COLOR,
            rect=pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT),
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

        self.image.blit(text_surface, (0, 0))


class AngledCard(Card):
    def __init__(self, suit, value, angle=-12.5):
        super().__init__(suit, value)
        self.image = pygame.transform.rotate(self.image, angle=angle)


class TableCardGroup(pygame.sprite.Group):
    """
    Represents the cards that were put on the table.
    Consists of attack cards and defend cards.
    """

    def __init__(self, spacing=30):
        super().__init__()
        self.spacing = spacing
        self.cards = {}
        self.current_position = 0
        self.update()

    def update(self) -> None:
        for position, card_pair in self.cards.items():
            for card_type, card_dict in card_pair.items():
                card = card_dict.get("card")
                card.rect.center = (
                    card.width + (card.width + self.spacing) * position,
                    card.height,
                )
                card.update()

    def _init_card_dict_attack_position(self, position):
        self.cards[position] = {
            "attack": {"suit": None, "value": None, "card": None},
        }

    def attack(self, suit, value):
        card = Card(suit, value)
        position = self.current_position
        self._init_card_dict_attack_position(position)
        self.cards[position]["attack"] = {
            "suit": suit,
            "value": value,
            "card": card,
        }
        self.current_position += 1
        self.add(card)

    def _find_attack_position(self, suit, value):
        for position, card_pair in self.cards.items():
            attack_card = card_pair.get("attack")
            if attack_card.get("suit") == suit and attack_card.get("value") == value:
                return position
        raise LookupError(f"Attack card '{suit}{value}' not found")

    def defend(self, attack_suit, attack_value, defend_suit, defend_value):
        defend_card = AngledCard(defend_suit, defend_value, angle=CARD_DEFEND_ANGLE)
        position = self._find_attack_position(attack_suit, attack_value)
        self.cards[position]["defend"] = {
            "suit": defend_suit,
            "value": defend_value,
            "card": defend_card,
        }
        self.add(defend_card)

    def empty(self) -> None:
        super().empty()
        self.cards = {}
        self.current_position = 0
