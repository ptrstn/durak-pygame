from durakgui.view import DurakTable


def mock_table_action(table: DurakTable, id):
    if id == 0:
        table.set_trump_card("♣", "4")

        table.set_hand(
            [
                ("♦", "10"),
                ("♠", "3"),
                ("♥", "Q"),
                ("♣", "8"),
                ("♣", "J"),
                ("♣", "K"),
            ]
        )

        table.set_opponent_hand(6)

    elif id == 1:
        table.attack("♦", "2")
        table.set_opponent_hand(table.opponent_hand.number_of_cards - 1)
    elif id == 2:
        table.defend("♦", "2", "♦", "10")
        table.set_hand(
            [
                ("♠", "3"),
                ("♥", "Q"),
                ("♣", "8"),
                ("♣", "J"),
                ("♣", "K"),
            ]
        )
    elif id == 3:
        table.attack("♥", "10")
        table.attack("♥", "2")
        table.set_opponent_hand(table.opponent_hand.number_of_cards - 2)
    elif id == 4:
        table.defend("♥", "10", "♣", "8")
        table.set_hand(
            [
                ("♠", "3"),
                ("♥", "Q"),
                ("♣", "J"),
                ("♣", "K"),
            ]
        )
    elif id == 5:
        table.defend("♥", "2", "♥", "Q")
        table.set_hand(
            [
                ("♠", "3"),
                ("♣", "J"),
                ("♣", "K"),
            ]
        )
    elif id == 6:
        table.attack("♣", "2")
        table.set_opponent_hand(table.opponent_hand.number_of_cards - 1)
    elif id == 7:
        table.defend("♣", "2", "♣", "J")
        table.set_hand(
            [
                ("♠", "3"),
                ("♣", "K"),
            ]
        )
    elif id == 8:
        table.attack("♠", "2")
        table.set_opponent_hand(table.opponent_hand.number_of_cards - 1)
    elif id == 9:
        table.defend("♠", "2", "♠", "3")
        table.set_hand(
            [
                ("♣", "K"),
            ]
        )
    elif id == 10:
        table.attack("♣", "3")
        table.set_opponent_hand(table.opponent_hand.number_of_cards - 1)
    elif id == 11:
        table.defend("♣", "3", "♣", "K")
        table.set_hand([])
    elif id == 12:
        table.clear_battlefield()
    elif id == 13:
        table.set_opponent_hand(6)
    elif id == 14:
        table.set_hand(
            [
                ("♦", "7"),
                ("♠", "7"),
                ("♥", "7"),
            ]
        )
        table.remove_deck_card()
    elif id == 15:
        table.set_hand([("♦", "7"), ("♠", "7"), ("♥", "7"), ("♣", "4")])
        table.remove_trump_card()
    elif id == 16:
        table.reset()
