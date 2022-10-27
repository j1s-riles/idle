from dataclasses import dataclass
import generator_ as g
from constants import gen_ID, gen_type
from generator_factory import GeneratorFactory

class Game():
    def __init__(self) -> None:
        self.generators = {}
        self.generator_factory = GeneratorFactory()
        self.currency = Currency(10.0)

        # The first unlocked PC generator
        self.generators[gen_ID.SLIME_GREEN] = self.generator_factory.get_generator(
            gen_type=gen_type.PC_GEN,
            target=self.currency,
            production_rate=1.0001,
            initial_cost=10.0,
            cost_scalar=1.05 )
        

    def game_loop(self):
        """Single iteration of the main game loop"""
        # First, reconcile all generation in one step
        for gen in self.generators.values():
            gen.generate()

        # Next, update those values for the next tick
        for gen in self.generators.values():
            gen.finalize_increases()

    def buy_generator(self, gen_ID: gen_ID, amt: int) -> bool:
        """Buy a specified amount of a certain generator"""
        new_currency_amt = self.generators[gen_ID].buy(amt, self.currency.quantity)
        if new_currency_amt < 0:
            return False

        self.currency.quantity = new_currency_amt
        return True

@dataclass
class Currency():
    quantity: float