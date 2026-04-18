from statemachine import State

from fsm.add_recipe_fsm import AddRecipeFSM
from logger import fsm_logger

class MyRecipesMenuFSM(State.Compound):
    my_recipes_list=State(initial=True)
    view_recipe=State()
    add_recipe=AddRecipeFSM
    edit_recipe=State()
    delete_recipe=State()

    open_view_recipe=my_recipes_list.to(view_recipe)
    open_add_recipe = my_recipes_list.to(add_recipe)
    open_edit_recipe=view_recipe.to(edit_recipe)
    open_delete_recipe=view_recipe.to(delete_recipe)
    open_my_recipes_list=delete_recipe.to(my_recipes_list)

    back = (view_recipe.to(my_recipes_list) |
            edit_recipe.to(view_recipe) |
            add_recipe.to(my_recipes_list) |
            delete_recipe.to(view_recipe))

    def on_enter_state(self, source:State, target: State, event: str):
        fsm_logger.debug(f"Перешли из {source.id} в {target.id}. Событие: {event}")

