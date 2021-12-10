from durakui.areas import OpponentHandArea, HandArea, DeckArea
from durakui.cards import Hand, Battlefield, Deck, OpponentHand


def mock_hand(hand: Hand):
    mock_data = [("♠", "A"), ("♦", "7"), ("♥", "7"), ("♠", "4"), ("♠", "5"), ("♠", "6")]
    hand.set_hand(mock_data)


def mock_opponent_hand(opponent_hand: OpponentHand):
    opponent_hand.set_hand(12)


def mock_battlefield(battlefield: Battlefield):
    battlefield.empty()
    battlefield.attack("♠", "2")
    battlefield.attack("♠", "8")
    battlefield.defend("♠", "2", "♠", "10")
    battlefield.attack("♦", "A")
    battlefield.attack("♠", "9")
    battlefield.defend("♦", "A", "♣", "2")
    battlefield.attack("♥", "K")
    battlefield.attack("♠", "3")
    battlefield.defend("♠", "3", "♥", "J")


def mock_deck(deck: Deck):
    trump = ("♥", "5")
    deck.set_trump_card(*trump)


def mock_action(game, id: int):
    battlefield = game.battlefield_area.battlefield
    opponent_hand = game.opponent_hand_area.opponent_hand

    def clear_opponent_hand():
        opponent_hand.empty()
        game.opponent_hand_area.opponent_hand.clear(
            game.opponent_hand_area.image, OpponentHandArea().image
        )

    hand = game.hand_area.hand
    deck = game.deck_area.deck

    if id == 0:
        clear_opponent_hand()
        opponent_hand.set_hand(5)
        battlefield.attack("♠", "2")
    if id == 1:
        clear_opponent_hand()
        opponent_hand.set_hand(4)
        battlefield.attack("♠", "8")
    if id == 2:
        battlefield.defend("♠", "2", "♠", "10")
    if id == 3:
        clear_opponent_hand()
        opponent_hand.set_hand(3)
        battlefield.attack("♦", "A")
    if id == 4:
        clear_opponent_hand()
        opponent_hand.set_hand(2)
        battlefield.attack("♠", "9")
    if id == 5:
        battlefield.defend("♦", "A", "♣", "2")
    if id == 6:
        clear_opponent_hand()
        opponent_hand.set_hand(1)
        battlefield.attack("♥", "K")
    if id == 7:
        clear_opponent_hand()
        opponent_hand.set_hand(0)
        battlefield.attack("♠", "3")
    if id == 8:
        battlefield.defend("♠", "3", "♥", "J")
    if id == 9:
        game.deck_area.deck.clear(game.deck_area.image, DeckArea().image)
        deck.remove_deck_card()
        opponent_hand.set_hand(1)
    if id == 10:
        hand.empty()
        game.hand_area.hand.clear(game.hand_area.image, HandArea().image)
        hand.set_hand([("♥", "5")])
        deck.empty()
        game.deck_area.deck.clear(game.deck_area.image, DeckArea().image)
