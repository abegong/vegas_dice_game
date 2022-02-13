from vegas_dice_game.game import Game
from vegas_dice_game.engine import GameEngine, Casino

def test_setup():
    """A smoke test to verify that play_game executes without errors."""

    game = Game()
    game.play_game()

    assert False


def test__any_players_with_dice_remain():
    game = GameEngine()
    assert game._any_players_with_dice_remain() == True

    # Zero out all players' dice
    for p in game.players:
        p.dice_remaining = 0
    
    assert game._any_players_with_dice_remain() == False

def test__get_next_player():
    game = GameEngine()
    assert game.next_player_id == 0

    game._get_next_player()
    assert game.next_player_id == 1
    
    game._get_next_player()
    assert game.next_player_id == 2

    game._get_next_player()
    assert game.next_player_id == 3

    game._get_next_player()
    assert game.next_player_id == 0

    # Zero out all players' dice
    for p in game.players:
        p.dice_remaining = 0
    
    game._get_next_player()
    assert game.next_player_id == -1

def test__score_casino():
    # Whoever has the most dice wins.
    assert GameEngine._score_casino(
        Casino(
            id_ = 0,
            payouts = [50],
            placed_dice = [1, 0, 0, 0]
        )
    ) == [50, 0, 0, 0]

    # Whoever has the most dice wins, even if others have a lot of dice
    assert GameEngine._score_casino(
        Casino(
            id_ = 0,
            payouts = [50],
            placed_dice = [4, 3, 2, 1]
        )
    ) == [50, 0, 0, 0]

    # No bets -> no payouts
    assert GameEngine._score_casino(
        Casino(
            id_ = 0,
            payouts = [50],
            placed_dice = [0, 0, 0, 0]
        )
    ) == [0, 0, 0, 0]

    # Nobody wins ties
    assert GameEngine._score_casino(
        Casino(
            id_ = 0,
            payouts = [50],
            placed_dice = [1, 1, 0, 0]
        )
    ) == [0, 0, 0, 0]

    # Really. Nobody wins ties
    assert GameEngine._score_casino(
        Casino(
            id_ = 0,
            payouts = [50],
            placed_dice = [1, 1, 1, 1]
        )
    ) == [0, 0, 0, 0]

    # ...unless there's a runner-up
    assert GameEngine._score_casino(
        Casino(
            id_ = 0,
            payouts = [50],
            placed_dice = [2, 2, 1, 0]
        )
    ) == [0, 0, 50, 0]

    # When there are multiple payouts, there can be multiple winners.
    assert GameEngine._score_casino(
        Casino(
            id_ = 0,
            payouts = [50, 30, 20],
            placed_dice = [0, 1, 2, 3]
        )
    ) == [0, 20, 30, 50]