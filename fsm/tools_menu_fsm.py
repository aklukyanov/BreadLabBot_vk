from statemachine import State

class StarterCalc(State.Compound):

    choose_direction=State(initial=True)
    waiting_sourdough_weight=State()
    choosing_starter_proportions=State()
    show_result=State(final=True)

    enter_direction=choose_direction.to(waiting_sourdough_weight)
    enter_weight=waiting_sourdough_weight.to(choosing_starter_proportions)
    calculate=choosing_starter_proportions.to(show_result)


    back = (
            waiting_sourdough_weight.to(choose_direction) |
            choosing_starter_proportions.to(waiting_sourdough_weight)

    )

    def on_enter_state(self, source:State, target: State, event: str):
        print(f"Перешли из {source.id} в {target.id}. Событие: {event}")


class ToolsMenu(State.Compound):

    tools=State(initial=True)
    starter_calc=StarterCalc
    proportions_calc=State()

    open_starter_calc=tools.to(starter_calc)
    open_proportions_calc = tools.to(proportions_calc)

    back = (proportions_calc.to(tools)|
            starter_calc.to(tools)
            )

    def on_enter_state(self, source:State, target: State, event: str):
        print(f"Перешли из {source.id} в {target.id}. Событие: {event}")


