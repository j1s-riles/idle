from constants import gen_type
import generator_ as g

class GeneratorFactory:
    def get_generator(self, gen_type:gen_type, target, production_rate: float, 
        initial_cost: float, cost_scalar: float, multiplier=1.0, quantity=0):
        
        if gen_type is gen_type.PC_GEN:
            return g.CurrencyGenerator(
                target=target,
                production_rate=production_rate,
                initial_cost=initial_cost,
                cost_scalar=cost_scalar,
                multiplier=multiplier,
                quantity=quantity
            )

        if gen_type is gen_type.GEN_GEN:
            return g.GeneratorGenerator(
                target=target,
                production_rate=production_rate,
                initial_cost=initial_cost,
                cost_scalar=cost_scalar,
                multiplier=multiplier,
                quantity=quantity
            )

        if gen_type is gen_type.MULTI_GEN:
            return g.MultiplierGenerator(
                target=target,
                production_rate=production_rate,
                initial_cost=initial_cost,
                cost_scalar=cost_scalar,
                multiplier=multiplier,
                quantity=quantity
            ) 