import generator as g
from game_enums import gen_ID, gen_type

class Game():
    def __init__(self) -> None:
        self.generators = {}
        # The first unlocked PC generator
        self.generators[gen_ID.PC1] = g.Generator(
            gen_type=gen_type.PC_GEN,
            production_rate=1.0001,
            initial_cost=10.0,
            cost_scalar=1.05 )
        
        self.currency = 10.0

    def generate_currency(self):
        """Trigger generators of Primary Currency"""
        for gen in self.generators.values():
            if gen.gen_type is g.gen_type.PC_GEN:
                self.currency += gen.generate()

    def game_loop(self):
        """Single iteration of the main game loop"""
        self.generate_currency()

    def buy_generator(self, gen_ID: gen_ID, amt: int) -> bool:
        """Buy a specified amount of a certain generator"""
        new_currency = self.generators[gen_ID].buy(amt, self.currency)
        if new_currency < 0:
            return False

        self.currency = new_currency
        return True
