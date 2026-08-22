import random


class Deck:
    def __init__(self):
        # Define suits and ranks
        self.suits = ["♠", "♥", "♦", "♣"]
        self.ranks = ["A", "K", "Q", "J", "10", "9", "8", "7","6"]
        self.jokers = ["JOKER", "JOKER"]
        self.deck = self.create_deck()
        self.trump_card = 'none'

    def create_deck(self):
        cards = [f"{rank}{suit}" for suit in self.suits for rank in self.ranks]
        cards.remove('6♦')
        cards.remove('6♣')
        cards.extend(self.jokers)
        random.shuffle(cards)
        return cards

    def determine_trump_card(self):
        while True:
            trump_card_number = input(f"what would you like to be trump card? \n choose relevant number in list: {self.suits} or print none:")
            if trump_card_number in ['1', '2', '3', '4', 'none']:
                break
            else:
                print('Incorrect input, you can choose only numbers (1-4) or none')
        if trump_card_number != 'none':
            trump_card = self.suits[int(trump_card_number) - 1]
        else:
            trump_card = 'none'
        return trump_card

