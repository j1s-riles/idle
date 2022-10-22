import math
from constants import gen_type, TICK_SCALAR

class Generator():
    def __init__(self, gen_type: gen_type, production_rate: float, initial_cost: float, cost_scalar: float, multiplier=1.0, quantity=0):
        self.gen_type = gen_type
        self.production_rate = production_rate
        self.initial_cost = initial_cost
        self.cost = initial_cost
        self.cost_scalar = cost_scalar
        self.multiplier = multiplier
        self.quantity = quantity
        self.quantity_purchased = 0

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

    def reset_quantity(self) -> None:
        """Resets this generator for prestige. Returns the new quantity"""
        self.quantity = 0
        self.quantity_purchased = 0

    def generate(self) -> float:
        """Returns the final production value for a single step of generation"""
        return self.production_rate * self.quantity * self.multiplier * TICK_SCALAR



    

    
