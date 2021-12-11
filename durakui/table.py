from pygame.sprite import Group

from durakui.backgrounds import (
    BattlefieldBackground,
    DeckBackground,
    HandBackground,
    OpponentBackground,
    TableBackground,
)
from durakui.cards import Battlefield, Hand, Deck, OpponentHand


class DurakTable(Group):
    def __init__(self):
        super().__init__()
        self.battlefield_background = BattlefieldBackground()
        self.deck_background = DeckBackground()
        self.hand_background = HandBackground()
        self.opponent_background = OpponentBackground()
        self.table_background = TableBackground()

        self.battlefield = Battlefield()
        self.hand = Hand()
        self.deck = Deck()
        self.opponent_hand = OpponentHand()

        self.add_deck_card()

        self._position_backgrounds()
        self._add_backgrounds_to_group()

    def _position_backgrounds(self):
        self.hand_background.rect.centerx = self.table_background.rect.centerx
        self.hand_background.rect.bottom = self.table_background.rect.bottom
        self.opponent_background.rect.centerx = self.table_background.rect.centerx
        self.battlefield_background.rect.center = self.table_background.rect.center
        self.battlefield_background.rect.centerx += 50
        self.battlefield_background.rect.centery += 25
        self.deck_background.rect.centery = self.table_background.rect.centery
        self.deck_background.rect.x = 10

    def _add_backgrounds_to_group(self):
        """
        Adds backgrounds to main table group. Order is important.
        """
        self.add(self.table_background)
        self.add(self.battlefield_background)
        self.add(self.deck_background)
        self.add(self.opponent_background)
        self.add(self.hand_background)

    def add_deck_card(self):
        self.clear(self.deck_background.image, self.table_background.image)
        self.deck.add_deck_card()
        self.deck.draw(self.deck_background.image)

    def remove_deck_card(self):
        self.clear(self.deck_background.image, self.table_background.image)
        self.deck.remove_deck_card()
        self.deck.draw(self.deck_background.image)

    def remove_trump_card(self):
        self.clear(self.deck_background.image, self.table_background.image)
        self.deck.remove_trump_card()
        self.deck.draw(self.deck_background.image)

    def set_trump_card(self, suit: str, value: str):
        self.clear(self.deck_background.image, self.table_background.image)
        self.deck.set_trump_card(suit, value)
        self.deck.draw(self.deck_background.image)

    def set_opponent_hand(self, number_of_cards: int):
        self.clear(self.opponent_background.image, self.table_background.image)
        self.opponent_hand.set_hand(number_of_cards)
        self.opponent_hand.draw(self.opponent_background.image)

    def set_hand(self, suit_value_pairs: list):
        self.clear(self.hand_background.image, self.table_background.image)
        self.hand.set_hand(suit_value_pairs)
        self.hand.draw(self.hand_background.image)

    def attack(self, suit: str, value: str):
        self.clear(self.battlefield_background.image, self.table_background.image)
        self.battlefield.attack(suit, value)
        self.battlefield.draw(self.battlefield_background.image)

    def defend(
        self, attack_suit: str, attack_value: str, defend_suit: str, defend_value: str
    ):
        self.clear(self.battlefield_background.image, self.table_background.image)
        self.battlefield.defend(attack_suit, attack_value, defend_suit, defend_value)
        self.battlefield.draw(self.battlefield_background.image)

    def clear_battlefield(self):
        self.clear(self.battlefield_background.image, self.table_background.image)
        self.battlefield.empty()

    def reset(self):
        self.remove_trump_card()
        self.add_deck_card()
        self.clear_battlefield()
        self.set_hand([])
        self.set_opponent_hand(0)
