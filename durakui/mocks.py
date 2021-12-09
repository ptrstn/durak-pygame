from durakui.cards import Hand, TableCardGroup, Deck, OpponentHand


def mock_hand(hand: Hand):
    mock_data = [("♠", "A"), ("♦", "7"), ("♥", "7"), ("♠", "4"), ("♠", "5"), ("♠", "6")]
    hand.set_hand(mock_data)


def mock_opponent_hand(opponent_hand: OpponentHand):
    opponent_hand.set_hand(6)


def mock_table(table: TableCardGroup):
    table.empty()
    table.attack("♠", "2")
    table.attack("♠", "8")
    table.defend("♠", "2", "♠", "10")
    table.attack("♦", "A")
    table.attack("♠", "9")
    table.defend("♦", "A", "♣", "2")
    table.attack("♥", "K")
    table.attack("♠", "3")
    table.defend("♠", "3", "♥", "J")


def mock_deck(deck: Deck):
    trump = ("♥", "5")
    deck.set_trump_card(*trump)
