from statemachine import StateChart, State

from fsm.tools_menu_fsm import ToolsMenu


class MainMenu(StateChart):
    allow_event_without_transition = False
    strict=True

    main=State(initial=True)
    tools_menu=ToolsMenu

    open_tools=main.to(tools_menu)
    back=tools_menu.to(main)

    def on_enter_state(self, source:State, target: State, event: str):
        print(f"Перешли из {source.id} в {target.id}. Событие: {event}")

