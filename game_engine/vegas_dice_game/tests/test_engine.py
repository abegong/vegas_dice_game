from vegas_dice_game.engine import Game
from vegas_dice_game.game import GameEngine

def test_setup():
    """A smoke test to verify that play_game executes without errors."""

    game = Game()
    game.play_game()


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
