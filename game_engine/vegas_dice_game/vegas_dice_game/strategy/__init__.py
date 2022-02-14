from vegas_dice_game.strategy.base import (
    Strategy,
    RandomStrategy,
    InputStrategy,
)
from vegas_dice_game.strategy.jonah import (
    JonahsGreatStrategy
)
from vegas_dice_game.strategy.machine_learning import (
    MLBasedStrategy,
    BinaryLogisticCasinoClassifierStrategy,
    MultinomialLogisticCasinoClassifierStrategy,
)

strategy_registry = {
    "RandomStrategy" : RandomStrategy,
    "InputStrategy" : InputStrategy,
    "JonahsGreatStrategy" : JonahsGreatStrategy,
    "MLBasedStrategy" : MLBasedStrategy,
    "MultinomialLogisticCasinoClassifierStrategy" : MultinomialLogisticCasinoClassifierStrategy,
    "BinaryLogisticCasinoClassifierStrategy" : BinaryLogisticCasinoClassifierStrategy,
}