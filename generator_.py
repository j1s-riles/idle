from abc import abstractmethod, ABC
import math
from constants import gen_type, TICK_SCALAR

class Generator_(ABC):
    def __init__(self, target, production_rate: float, 
        initial_cost: float, cost_scalar: float, multiplier: float, quantity:int):
        self.target = target
        self.production_rate = production_rate
        self.initial_cost = initial_cost
        self.cost = initial_cost
        self.cost_scalar = cost_scalar
        self.multiplier = multiplier
        self.quantity = quantity
        self.quantity_purchased = 0
        self.quantity_next = 0
        self.multiplier_next = 1

    def price_check(self, amt: int) -> float:
        """Finds the cost of buying a specified number of generators"""
        b = self.initial_cost
        r = self.cost_scalar
        k = self.quantity_purchased

        # Calculate the cost of buying generators in bulk
        return b * (r ** k * (r**amt - 1)/ (r - 1))

    def buy(self, amt: int) -> None:
        """Increase the quantity and cost of generators"""
        self.quantity += amt
        self.quantity_purchased += amt

        # Update cost to next step     
        self.cost = self.initial_cost * self.cost_scalar**self.quantity_purchased
        

    def get_max_buy(self, currency: float) -> int:
        """Finds the maximum number of generators it's possible to buy with the given currency."""
        b = self.initial_cost
        r = self.cost_scalar
        k = self.quantity_purchased

        return math.floor(math.log(((currency *  (r-1))/b*r**k) + 1, r))

    def find_generation_value(self) -> float:
        """Returns the final production value for a single step of generation"""
        return self.production_rate * self.quantity * self.multiplier * TICK_SCALAR

    def finalize_increases(self) -> None:
        """Updates any properties modified this tick."""
        self.quantity += self.quantity_next
        self.multiplier *= self.multiplier_next

        self.quantity_next = 0
        self.multiplier_next = 1

    @abstractmethod
    def generate(self) -> None:
        pass

class CurrencyGenerator(Generator_):
    def generate(self) -> None:
        """Generates target currency"""
        self.target.quantity += self.find_generation_value()

class GeneratorGenerator(Generator_):
    def generate(self) -> None:
        """Generates target generator"""
        self.target.quantity_next += self.find_generation_value()

class SlimeGenerator(Generator_):
    def generate(self) -> None:
        """Generates target slime"""
        self.target.quantity_next += self.find_generation_value()

class MultiplierGenerator(Generator_):
    def generate(self) -> None:
        """Generates target multiplier"""
        self.target.multiplier_next *= self.find_generation_value()


class GeneratorFactory:
    def get_generator(self, gen_type:gen_type, target, production_rate: float, 
        initial_cost: float, cost_scalar: float, multiplier=1.0, quantity=0):
        """Returns a new generator of specified type"""
        if gen_type is gen_type.PC_GEN:
            return CurrencyGenerator(
                target=target,
                production_rate=production_rate,
                initial_cost=initial_cost,
                cost_scalar=cost_scalar,
                multiplier=multiplier,
                quantity=quantity
            )

        if gen_type is gen_type.SLIME_GEN:
            return SlimeGenerator(
                target=target,
                production_rate=production_rate,
                initial_cost=initial_cost,
                cost_scalar=cost_scalar,
                multiplier=multiplier,
                quantity=quantity
            )

        if gen_type is gen_type.GEN_GEN:
            return GeneratorGenerator(
                target=target,
                production_rate=production_rate,
                initial_cost=initial_cost,
                cost_scalar=cost_scalar,
                multiplier=multiplier,
                quantity=quantity
            )

        if gen_type is gen_type.MULTI_GEN:
            return MultiplierGenerator(
                target=target,
                production_rate=production_rate,
                initial_cost=initial_cost,
                cost_scalar=cost_scalar,
                multiplier=multiplier,
                quantity=quantity
            )