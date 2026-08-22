from deck import Deck
from player import Player,list_of_players
import random
import json


class Game:

    def __init__(self, player_list,deck):
        self.players = player_list
        self.deck = deck
        self.last_player_index = len(player_list) - 1
        self.bids = {}
        self.fulfilled_bids = {}
        self.total_bids = 0
        self.players_sequence_for_play = self.players
        self.max_points = self.initial_max_points()

    def get_last_player(self):
        return self.players[-1]

    def get_first_player(self):
        return self.players[0]

    def ask_for_bids(self,player):
        while True:
            try:
                bid = int(input(f"{player.name}, how many cards do you plan to take (0-9)? "))
                if 0 <= bid <= 9:
                    if player == self.get_last_player() and self.total_bids + bid == 9:
                        print("Your bid cannot make the total equal to 9. Choose another number.")
                    else:
                        self.bids[player.name] = bid
                        self.fulfilled_bids[player.name] = 0
                        self.total_bids += bid
                        break
                else:
                    print("Invalid input. Please enter a number between 0 and 9.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def gather_card(self,player_list):
        card_list = []
        demanded_suit = False
        for player in player_list:
            card = player.play_card()
            if player == player_list[0] and card == 'JOKER':
                suits = ["♠", "♥", "♦", "♣"]
                asked_suit_number= input(f"Which suit do you ask from players: choose a relevant number {suits} or print 'none'")
                if asked_suit_number != 'none':
                    asked_suit = suits[int(asked_suit_number)-1]
                    demanded_suit = True
                    print(f'Asked suit is {asked_suit}')
            if demanded_suit and player != player_list[0]:
                card_order = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, '10': 10, '9': 9, '8': 8,
                              '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
                possible_cards = [card for card in player.hand + [card] if card[-1] == asked_suit]
                if len(possible_cards)>0:
                    def card_value(card):
                        value = card[:-1]
                        return card_order[value]
                    highest_card = sorted(possible_cards, key=card_value, reverse=True)[0]
                    while card != highest_card and card != 'JOKER':
                        player.hand.append(card)
                        print(f'You have to play highest {asked_suit}')
                        card = player.play_card()
            card_list.append(card)
        return card_list

    def determine_winner_card(self, card_list, trump_card):
        rank_order = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
                      '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

        winner_card_index = 0
        winner_card = card_list[0]
        winner_suit = winner_card[-1]
        try:
            winner_rank = rank_order[winner_card[:-1]]
        except KeyError:
            winner_rank = 100

        for index in range(1, len(card_list)):
            current_card = card_list[index]
            if current_card != 'JOKER':
                current_suit = current_card[-1]
                current_rank = rank_order[current_card[:-1]]
            if current_card == 'JOKER':
                winner_card_index = index
                winner_rank = 100
            elif current_suit == winner_suit:
                if current_rank > winner_rank:
                    winner_card_index = index
                    winner_rank = current_rank
            elif current_suit == trump_card and card_list[0] != 'JOKER':
                winner_card_index = index
                winner_rank = current_rank
                winner_suit = current_suit

        return winner_card_index

    def determine_card_taker(self,player_list, index):
        card_taker = player_list[index]
        self.fulfilled_bids[card_taker.name] += 1
        return card_taker

    def rotate_list_for_card_chooser(self,index):
        self.players_sequence_for_play = self.players_sequence_for_play[index:] + self.players_sequence_for_play[:index]

    def calculate_points(self,said, fulfilled):
        point_dict = {}
        for name, value in said.items():
            if value == fulfilled[name]:
                if value == 9:
                    point = 900
                else:
                    point = (value + 1) * 50
            elif value > 0 and fulfilled[name] == 0:
                for player in self.players:
                    if player.name == name:
                        player.bonus_status = False
                point = -500

            else:
                for player in self.players:
                    if player.name == name:
                        player.bonus_status = False
                point = fulfilled[name] * 10
            point_dict[name] = point
        return point_dict

    def initial_max_points(self):
        names = [player.name for player in self.players]
        self.max_points = {name:0 for name in names}
        return self.max_points

    def new_max_point(self,initial_points,point_dict):
        for player,points in initial_points.items():
            if points < point_dict[player]:
                self.max_points[player] = point_dict[player]
        return self.max_points

    def update_score(self,points):
        try:
            with open("scores.json", 'r') as file:
                score = json.load(file)
        except FileNotFoundError:
            with open("scores.json", "w") as file:
                score = {player.name:0 for player in self.players}
                json.dump(score, file, indent=4)

        for name in score:
            score[name] += points[name]

        with open("scores.json", "w") as file:
            json.dump(score, file, indent=4)

    def add_bonus_points(self):
        for player in self.players:
            if player.bonus_status:
                print(f'{player.name} is getting bonus')
                with open("scores.json", 'r') as file:
                    score = json.load(file)
                    score[player.name] += self.max_points[player.name]
                with open("scores.json", "w") as file:
                    json.dump(score, file, indent=4)


def single_deal(list_of_players):
    global game_number
    game_number += 1
    random.shuffle(list_of_players)
    deck = Deck()
    game = Game(list_of_players,deck.deck)
    last_player = game.get_last_player()
    first_player = game.get_first_player()
    print(f'{last_player.name} is the last player')
    print(f'{first_player.name} is the first player')
    for player in game.players:
        player.deal_cards(deck, first_player.name)
        print(f'PLayer_{player.player_number},{player.name}: {player.hand}')
        game.ask_for_bids(player)
    for _ in range(9):
        cards = game.gather_card(game.players_sequence_for_play)
        winner_index = game.determine_winner_card(cards,deck.trump_card)
        card_taker = game.determine_card_taker(game.players_sequence_for_play,winner_index)
        print(f'Player_{card_taker.player_number},{card_taker.name}, took the cards ')
        game.rotate_list_for_card_chooser(winner_index)
    bids =game.bids
    fulfilled_bids = game.fulfilled_bids
    print(f'player bids were: {bids}')
    print(f'player fulfilled bids were: {fulfilled_bids}')
    points = game.calculate_points(bids,fulfilled_bids)
    game.update_score(points)
    if game_number % 4 == 0:
        game.add_bonus_points()
        game.initial_max_points()
        for player in list_of_players:
            player.bonus_status = True
    print('This deal is over \n ')


def determine_game_winner():
    with open("scores.json", 'r') as file:
        score = json.load(file)
        max_value = max(score.values())
        winners = {item for item in score.items() if item[1] == max_value}
        for winner in winners:
            print(f'Winner is {winner[0]} with {winner[1]} points')


game_number = 0

def start_game():
    player_1 = Player()
    player_2 = Player()
    player_3 = Player()
    player_4 = Player()
    with open('scores.json', 'w') as file:
        json.dump({player.name:0 for player in list_of_players}, file)
    for _ in range(16):
        single_deal(list_of_players)
    determine_game_winner()


if __name__ == '__main__':
    start_game()