
class play_space:
    def __init__(self, accessible_to = 'everyone', visible_to = 'everyone', can_see_no_of_cards = False, access_keys = (), vision_keys = ()):
        self.__cards = []

        if visible_to != 'everyone' and visible_to != 'some':
            raise ValueError(f"{visible_to} has been assigned to visibile_to-> can only be assigned values of 'everyone' and 'some'.")
        self.__visible_to = visible_to

        if accessible_to != 'everyone' and accessible_to != 'some':
            raise ValueError("visibile_to can only be assigned values of 'everyone' and 'some'.")
        self.__accessible_to = accessible_to

        self.__access_keys = access_keys
        self.__vision_keys = vision_keys
        self.__can_see_no_of_cards = can_see_no_of_cards




    def validate_access(self, access_key):
        if self.__accessible_to == 'everyone':
            return True
        elif self.__accessible_to == 'no_one':
            return False
        elif self.__accessible_to =='some':
            if access_key in self.__access_keys:
                return True
            else: 
                return False

    def validate_vision(self, vision_key):
        if self.__visible_to == 'everyone':
            return True
        elif self.__visible_to == 'no_one':
            return False
        elif self.__visible_to =='some':
            if vision_key in self.__vision_keys:
                return True
            else: 
                return False

    def see_cards(self, vision_key = ()):
        validation_check = self.validate_vision(vision_key)

        if validation_check:
            return self.__cards.copy()
        else: 
            print("This play_space can't be viewed by you.")
            return ()
    
    def see_no_of_cards(self):


        if self.__can_see_no_of_cards:
            return len(self.__cards)
        else: 
            print("This play_space can't be viewed by you.")
            return ()
    

    def is_valid_card(self, card):
        valid_ranks = {'2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', 'joker'}
        valid_suits = {'hearts', 'diamonds', 'clubs', 'spades', 'joker'}

        rank, suit = card
        
        if rank == 'joker' and suit != 'joker':
            return False
        if suit == 'joker' and rank != 'joker':
            return False
        if rank not in valid_ranks:
            return False
        if suit not in valid_suits:
            return False
        return True

    
    def add_card_to_space(self, card, access_key = ()):
        validation_check = self.validate_access(access_key)

        if validation_check:
            if self.is_valid_card(card):
                self.__cards.append(card)
                return True
            else:
                rank, suit = card
                print(f"The card {rank} of {suit} is not an accepted card type, and wasn't added.")
        else:
            print("You can't add cards to this play_space.")

        return False

    def add_cards_to_space(self, cards, private_key = ()):
        for card in cards:
            self.add_card_to_space(card, private_key)

    def shuffle(self, private_key = ()):
        validation_check = self.validate_access(private_key)

        if validation_check:
            self.__cards.shuffle()
            return True
        else: 
            print("This play_space can't be interacted with by you.")
            return False
        
    def deal_to(self, other_playspace, access_key = ()):
        validation_check = self.validate_access(access_key)

        if self.see_no_of_cards(self, private_key) == 0:
            print("This playspace has no cards to deal.")
            return False

        if validation_check:
            can_pass = other_playspace.add_card_to_space(self.__cards[0])
            if can_pass:
                return True
            else:
                print("The other playspace can't be interacted with by you.")
                return False
        else: 
            print("This play_space can't be interacted with by you.")
            return False

    def send_all_to(self, other_playspace, access_key = ()):
        validation_check = self.validate_player(access_key)
        validation_check_2 = other_playspace.validate_player(access_key)

        if validation_check and validation_check_2:
            for card in self.__cards:
                other_playspace.add_card_to_space(card)
            self.__cards.clear()
            return True
        else:
            print("You can't access one or both of these playspaces.")
            return False
        


def create_deck(has_jokers = True, no_of_jokers = 2, visible_to = 'everyone',accessible_to = 'everyone', access_keys = (), vision_keys = ()):
    deck = play_space(accessible_to = accessible_to, visible_to = visible_to, access_keys = access_keys, vision_keys = vision_keys, can_see_no_of_cards = True)

    valid_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    valid_suits = ['hearts', 'diamonds', 'clubs', 'spades']

    for suit in valid_suits:
        for rank in valid_ranks:
            card = rank, suit
            deck.add_card_to_space(card)

    if has_jokers:
        joker = 'joker', 'joker'
        for x in range(no_of_jokers):
            deck.add_card_to_space(joker)

    return deck

