import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--num_games', default=1000, help='Number of games to play.')
def simulate(num_games):
    import pandas as pd
    from vegas_dice_game.game import Game

    scores = []
    for i in range(1000):
        my_game = Game()
        new_scores = my_game.play_game(verbosity=0)
        scores.append(new_scores)

    df = pd.DataFrame(scores)
    print(df.sum())

@click.command()
def play():
    from vegas_dice_game.game import Game

    my_game = Game(
        strategies = ["RandomStrategy", "RandomStrategy", "RandomStrategy", "InputStrategy"]
    )
    new_scores = my_game.play_game()


cli.add_command(simulate)
cli.add_command(play)

if __name__ == '__main__':
    cli()