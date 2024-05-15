import cards_functions  as cf


if __name__ == "__main__":
    deck = cf.create_deck(has_jokers= False,)

    see_cards = deck.see_cards()

    print(see_cards)
    print(deck.see_no_of_cards())
    pass