# Joker Card Game

Joker is a Python-based card game designed for four players. The project is built using three main classes: `Deck`, `Player`, and `Game`.

The game consists of 16 deals.

## Deck Class

The `Deck` class is responsible for creating and managing the deck of cards.

It also allows the first player in each deal to choose the trump suit or play the deal without a trump suit.

## Player Class

The `Player` class creates the players and assigns the necessary attributes to each player.

It also includes the following methods:

- `deal_cards` — responsible for dealing cards to the players.
- `play_card` — allows a player to select a card during the game.

## Game Class

The `Game` class manages the game logic, defines the game rules, and stores the players' results.

It includes several methods:

- `get_last_player` and `get_first_player` — determine the first and last players.
- `ask_for_bids` — allows players to predict the number of cards they expect to win.
- `gather_card` — collects the cards played during a trick.
- `determine_winner_card` and `determine_card_taker` — determine the winning card and the player who takes the cards.
- `rotate_list_for_card_chooser` — ensures the correct order of players taking the first turn during the game. The player who won the previous trick starts the next one.
- `calculate_points` — calculates players' scores after each deal.
- `initial_max_points` and `new_max_point` — calculate bonus points for players who achieve the required score.
- `update_score` and `add_bonus_points` — update and store the players' scores in a JSON file.

## Game Functions

- `single_deal` — runs an individual deal.
- `start_game` — starts the game.

## Running the Game

The game is started using the `Deck` module.