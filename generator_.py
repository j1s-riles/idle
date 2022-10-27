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

    def buy(self, amt: int, currency) -> float:
        """Attempt to buy a specified number of this generator. Returns the currency remaining after purchase. 
        Returns -1 on failure."""
        b = self.initial_cost
        r = self.cost_scalar
        k = self.quantity_purchased

        # Calculate the cost of buying generators in bulk
        bulk_cost = b * (r ** k * (r**amt - 1)/ (r - 1))
        # Guard if player can't afford
        if bulk_cost > currency:
            return -1

        # Transaction
        new_currency = currency - bulk_cost
        self.quantity += amt
        self.quantity_purchased += amt

        # Update cost to next step     
        self.cost = b * r**k
        
        return new_currency

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

class MultiplierGenerator(Generator_):
    def generate(self) -> None:
        """Generates target multiplier"""
        self.target.multiplier_next *= self.find_generation_value()
    

    
