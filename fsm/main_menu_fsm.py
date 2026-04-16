from tkinter import Menu

from statemachine import StateChart, State

from fsm.my_recipes_menu_fsm import MyRecipesMenuFSM
from fsm.tools_menu_fsm import ToolsMenuFSM

from logger import fsm_logger

class MainMenu(StateChart):
    allow_event_without_transition = False
    strict=True

    main=State(initial=True)
    tools_menu=ToolsMenuFSM
    my_recipes_menu=MyRecipesMenuFSM

    open_tools=main.to(tools_menu)
    open_my_recipes_menu=main.to(my_recipes_menu)

    back=tools_menu.to(main) | my_recipes_menu.to(main)

    to_main=tools_menu.to(main) | my_recipes_menu.to(main)

    def on_enter_state(self, source:State, target: State, event: str):
        fsm_logger.debug(f"Перешли из {source.id} в {target.id}. Событие: {event}")


