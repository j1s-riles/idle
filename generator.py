import math
from game_enums import gen_type

class Generator:
    def __init__(self, gen_type: gen_type, production_rate: float, initial_cost: float, cost_scalar: float, multiplier=1.0, quantity=0):
        self.gen_type = gen_type
        self.production_rate = production_rate
        self.initial_cost = initial_cost
        self.cost = initial_cost
        self.cost_scalar = cost_scalar
        self.multiplier = multiplier
        self.quantity = quantity

    def buy(self, amt: int, currency) -> float:
        """Attempt to buy a specified number of this generator. -1 on failure."""
        b = self.initial_cost
        r = self.cost_scalar
        k = self.quantity

        # Calculate the cost of buying generators in bulk
        bulk_cost = b * (r ** k * (r**amt - 1)/ (r - 1))
        # Guard if player can't afford
        if bulk_cost > currency:
            return -1

        # Transaction
        new_currency = currency - bulk_cost
        self.quantity = self.quantity + amt

        # Update cost to next step     
        self.cost = b * r**k
        
        return new_currency

    def get_max_buy(self, currency: float) -> int:
        """Finds the maximum number of generators it's possible to buy with the given currency."""
        b = self.initial_cost
        r = self.cost_scalar
        k = self.quantity

        return math.floor(math.log(((currency *  (r-1))/b*r**k) + 1, r))

    def reset_quantity(self) -> int:
        """Resets this generator for prestige. Returns the new quantity"""
        self.quantity = 0
        return self.quantity

    def generate(self):
        """Returns the final production value for a single step of generation"""
        return self.production_rate * self.quantity * self.multiplier

    

    
