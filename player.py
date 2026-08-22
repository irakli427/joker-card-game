
list_of_players = []



class Player:

    def __init__(self):
        self.player_number = len(list_of_players)+1
        self.name = input(f"Player_{self.player_number} please enter your name: ")
        while self.name in [player.name for player in list_of_players] or len(self.name)<1:
            print('Name already used or used empty name, try something else')
            self.name = input(f"Player_{self.player_number} please enter your name: ")
        self.hand = []
        list_of_players.append(self)
        self.bonus_status = True

    def deal_cards(self, deck, first_player,cards_per_player=9):
        for num_of_cards in range(1,cards_per_player+1):
            self.hand.append(deck.deck.pop())
            if num_of_cards == 3 and self.name == first_player:
                print(f'{self.name} those are first three cards: {self.hand}')
                deck.trump_card = deck.determine_trump_card()
                print(f'Trump card is: {deck.trump_card}')

    def play_card(self):
        print(f'Player_{self.player_number},{self.name}, it is your hand: {self.hand}')
        while True:
            try:
                card_number = int(input(f'which card would you like to play? choose number between 1-{len(self.hand)}: '))
                if 0 < card_number <=len(self.hand):
                    break
                else:
                    print(f'please enter valid number from 1 to {len(self.hand)}')
            except ValueError:
                print("Invalid input. Please enter a valid number.")


        while card_number < 0 or card_number > len(self.hand):
            print(f'You have to choose number from 1 to {len(self.hand)} ')
            card_number = int(input(f'which card would you like to play? choose number between 1-{len(self.hand)}: '))
        card = self.hand.pop(card_number -1)
        return card


