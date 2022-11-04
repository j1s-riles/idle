from dataclasses import dataclass
from constants import slime_type
from slime import SlimeFactory

class Game():
    def __init__(self) -> None:
        self.slimes = {}
        self.slimefactory = SlimeFactory()
        self.gel = Currency(10.0)

        #TODO: implement loading parameters from config
        # The first unlocked gel-producing slime
        self.slimes[slime_type.GREEN] = self.slimefactory.get_slime(
            slimetype=slime_type.GREEN,
            targets={slime_type.GEL:self.gel}
        )
        

    def game_loop(self):
        """Single iteration of the main game loop"""
        # First, reconcile all generation in one step
        for slime in self.slimes.values():
            slime.generate_all()

        # Next, update those values for the next tick
        for slime in self.slimes.values():
            slime.finalize_all()

    def buy_slimes(self, slimetype: slime_type, amt: int) -> bool:
        """Buy a specified amount of a certain slime. Returns true on success."""
        price = self.slimes[slimetype].buy(amt, self.gel.quantity)
        self.gel.quantity -= price
        return bool(price)

@dataclass
class Currency():
    quantity: float