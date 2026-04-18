from statemachine import State

from fsm.load_recipe_fsm import LoadRecipeProportionsCalcFSM
from logger import fsm_logger


class StarterCalcFSM(State.Compound):

    choose_direction=State(initial=True)
    waiting_sourdough_weight=State()
    choosing_starter_proportions=State()
    show_result_starter_calc=State(final=True)

    enter_direction=choose_direction.to(waiting_sourdough_weight)
    enter_weight=waiting_sourdough_weight.to(choosing_starter_proportions)
    calculate=choosing_starter_proportions.to(show_result_starter_calc)


    back = (
            waiting_sourdough_weight.to(choose_direction) |
            choosing_starter_proportions.to(waiting_sourdough_weight)|
            show_result_starter_calc.to(choosing_starter_proportions)

    )

    def on_enter_state(self, source:State, target: State, event: str):
        fsm_logger.debug(f"Перешли из {source.id} в {target.id}. Событие: {event}")


class ProportionsCalcFSM(State.Compound):
    load_recipe_menu_proportions_calc=LoadRecipeProportionsCalcFSM
    waiting_multiplier=State()
    show_result_proportions_calc=State()

    enter_recipe=load_recipe_menu_proportions_calc.to(waiting_multiplier)
    enter_multiplier=waiting_multiplier.to(show_result_proportions_calc)

    back = show_result_proportions_calc.to(waiting_multiplier) | waiting_multiplier.to(load_recipe_menu_proportions_calc.choose_recipe_proportions_calc)


    def on_enter_state(self, source:State, target: State, event: str):
        fsm_logger.debug(f"Перешли из {source.id} в {target.id}. Событие: {event}")


class ToolsMenuFSM(State.Compound):

    tools=State(initial=True)
    starter_calc=StarterCalcFSM
    proportions_calc=ProportionsCalcFSM

    open_starter_calc=tools.to(starter_calc)
    open_proportions_calc = tools.to(proportions_calc)

    back = (proportions_calc.to(tools)|
            starter_calc.to(tools)
            )

    def on_enter_state(self, source:State, target: State, event: str):
        fsm_logger.debug(f"Перешли из {source.id} в {target.id}. Событие: {event}")


