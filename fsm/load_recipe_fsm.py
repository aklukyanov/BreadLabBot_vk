from statemachine import State

from logger import fsm_logger



class LoadRecipeProportionsCalcFSM(State.Compound):
    load_recipe_proportions_calc=State(initial=True)
    choose_recipe_proportions_calc=State(final=True)
    add_recipe_proportions_calc=State(final=True)

    open_choose_recipe_proportions_calc=load_recipe_proportions_calc.to(choose_recipe_proportions_calc)
    open_add_recipe_proportions_calc=load_recipe_proportions_calc.to(add_recipe_proportions_calc)

    back = choose_recipe_proportions_calc.to(load_recipe_proportions_calc) | add_recipe_proportions_calc.to(load_recipe_proportions_calc)

    def on_enter_state(self, source:State, target: State, event: str):
        fsm_logger.debug(f"Перешли из {source.id} в {target.id}. Событие: {event}")

