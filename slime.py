from generator_ import GeneratorFactory
from constants import gen_type, slime_type
from abc import ABC, abstractmethod

class Slime(ABC):
    def __init__(self, slimetype: slime_type, targets:dict, quantity=0) -> None:
        self.slimetype = slimetype
        self.quantity = quantity
        self.generators = []
        self.generator_factory = GeneratorFactory()
        self._build_generators(targets)

    def add_generator(self, type:gen_type, target, production_rate:float, initial_cost:float, cost_scalar:float):
        """Adds a new generator to the slime"""
        self.generators.append(self.generator_factory.get_generator(
            gen_type=type,
            target=target,
            production_rate=production_rate,
            initial_cost=initial_cost,
            cost_scalar=cost_scalar,
            quantity= self.quantity
        ))

    def price_check(self, amt:int) -> float:
        """Finds the cost of buying new slimes of specified amount"""
        total_price = 0.0
        for gen in self.generators:
            total_price += gen.price_check(amt)
        return total_price

    def buy(self, amt:int, currency) -> float:
        """Attempts to buy specified number of slimes. Returns the total price.
        If unsuccessful, returns 0.0"""
        total_price = self.price_check(amt=amt)
        if total_price > currency:
            return 0.0
        
        # Buy
        new_currency = currency - total_price
        for gen in self.generators:
            gen.buy(amt)
        
        self.quantity += amt

        return total_price

    def generate_all(self):
        """Run a generation step on all of this slime's generators"""
        for gen in self.generators:
            gen.generate()

    def finalize_all(self):
        """Finalize generation updates on all of this slime's generators"""
        for gen in self.generators:
            gen.finalize_increases()

    @abstractmethod
    def _build_generators(self, targets) -> None:
        """Builds the appropriate lineup of generator's for this slime type"""
        pass

class GreenSlime(Slime):
    def _build_generators(self, targets) -> None:
        """Adds a simple PC generator"""
        self.add_generator(
            type=gen_type.PC_GEN, 
            target=targets[slime_type.GEL],
            production_rate=1.0001,
            initial_cost=10.0,
            cost_scalar=1.05
            )

class SlimeFactory():
    def get_slime(self, slimetype:slime_type, targets:dict) -> Slime:
        """Returns a new slime of the specified type with specified generation targets"""
        if slimetype == slime_type.GREEN:
            return GreenSlime(slimetype=slimetype, targets=targets)
