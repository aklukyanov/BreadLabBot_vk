from statemachine import State

from logger import fsm_logger


class LoadRecipeFSM(State.Compound):
    load_recipe=State(initial=True)
    choose_recipe=State(final=True)
    add_recipe_load=State(final=True)

    open_choose_recipe=load_recipe.to(choose_recipe)
    open_add_recipe_load=load_recipe.to(add_recipe_load)

    back = choose_recipe.to(load_recipe)|add_recipe_load.to(load_recipe)

    def on_enter_state(self, source:State, target: State, event: str):
        fsm_logger.debug(f"Перешли из {source.id} в {target.id}. Событие: {event}")

