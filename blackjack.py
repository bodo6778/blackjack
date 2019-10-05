import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True


class Card:
    # Define a card

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[self.rank]

    # Print the card value
    def __str__(self):
        return f"{self.rank} of {self.suit} with the value of {self.value}"


class Deck:
    # Initialize the deck

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_print = "\n"
        for card in self.deck:
            deck_print = deck_print + "\n" + card.__str__()
        return "The deck has: " + deck_print

    def shuffle(self):
        random.shuffle(self.deck)

    # Deal the top card
    def deal(self):
        dealt_card = self.deck.pop()
        return dealt_card


class Hand:
    # Initialize the hand
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    # Add a card to the hand and calculate its value
    def add_card(self, card):
        self.cards.append(card)
        if card.value == 11:
            self.aces += 1
        self.value = self.value + card.value

    def ace_adjust(self):
        while self.aces > 0 and self.value > 21:
            self.value -= 10
            self.aces -= 1


class Chips:
    # Initialize and keep track of player's chips

    def __init__(self):
        self.total = 1000
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    # Function for making a bet and making sure the bet value is not too high
    while True:
        try:
            chips.bet = int(input("Place your bet: "))
        except TypeError:
            print("You need to input numbers only!")
        else:
            if chips.bet > chips.total:
                print("The bet cannot exceed your chips value")
            else:
                break


def hit(deck, hand):
    # Take a card
    hand.add_card(deck.deal())
    hand.ace_adjust()


def hit_or_stand(deck, hand):
    # Take a card or stop playing
    global playing

    while True:
        decision = input("Press 'h' to hit or 's' to stand!")

        if decision[0].lower() == 'h':
            hit(deck, hand)

        elif decision[0].lower() == 's':
            print("\nYou stand. Dealer is playing.")
            playing = False

        else:
            print("\nTry again:")
            continue
        break


# ----------------------
# Display card functions
# ----------------------


def show_some_cards(player, dealer):
    print(f"\nWith a value of {player.value}, your cards are:")
    for player_cards in player.cards:
        print(player_cards)
    print(f"The dealer card is {dealer.cards[0]}:")


def show_all_cards(player, dealer):
    print(f"\nWith a value of {player.value}, YOUR cards are:")
    for player_cards in player.cards:
        print(player_cards)
    print(f"With a value of {dealer.value}, the DEALER cards are:")
    for dealer_cards in dealer.cards:
        print(dealer_cards)

# --------------
# Game scenarios
# --------------


def player_busts(player, dealer, chips):
    print("\n\nThe dealer won, you busted.\n\n")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("\n\nYou won!\n\n")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("\n\nYou won, the dealer busted!\n\n")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("\n\nThe dealer won.\n\n")
    chips.lose_bet()


def push(player, dealer, chips):
    print("\n\nIt is a tie.\n\n")


# --------------------
# The actual game
# --------------------


while True:
    print("10Welcome to the table!\n")

    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    chips = Chips()

    # Make each hand
    deck.shuffle()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Place the bet
    take_bet(chips)

    # Show your cards and one dealer card
    show_some_cards(player_hand, dealer_hand)

    while playing:
        # Ask the player for his move
        hit_or_stand(deck, player_hand)
        show_some_cards(player_hand, dealer_hand)
        # Check if player has busted
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, chips)
            break
        # Continue if not
        if player_hand.value <= 21:
            # Fill the dealer's hand
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
            # Show cards and run scenarios
            show_all_cards(player_hand, dealer_hand)
            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, chips)
            elif player_hand.value > dealer_hand.value:
                player_wins(dealer_hand, player_hand, chips)
            else:
                push(player_hand, dealer_hand, chips)

    print(f"\nPlayer's chips are: {chips.total}")

    play_again = input("Do you want to play again? Y/N")

    if play_again[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break



