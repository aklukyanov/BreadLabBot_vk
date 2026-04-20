from statemachine import State

from fsm.add_recipe_fsm import AddRecipeFSM
from logger import fsm_logger

class MyRecipesMenuFSM(State.Compound):
    my_recipes_list=State(initial=True)
    view_recipe=State()
    add_recipe=AddRecipeFSM
    edit_existing_recipe=State()
    delete_recipe=State()
    save_edited_existing_recipe=State()
    save_success_edited_existing_recipe=State()

    open_view_recipe=my_recipes_list.to(view_recipe)
    open_add_recipe = my_recipes_list.to(add_recipe)
    open_edit_existing_recipe=view_recipe.to(edit_existing_recipe)
    open_delete_recipe=view_recipe.to(delete_recipe)
    open_my_recipes_list=delete_recipe.to(my_recipes_list)
    open_save_edited_existing_recipe=edit_existing_recipe.to(save_edited_existing_recipe)
    update_existing_recipe=edit_existing_recipe.to(save_edited_existing_recipe)
    confirm_update_existing_recipe=save_edited_existing_recipe.to(save_success_edited_existing_recipe)
    save_as_new=save_edited_existing_recipe.to(save_success_edited_existing_recipe)
    save_as_version=save_edited_existing_recipe.to(save_success_edited_existing_recipe)

    back = (view_recipe.to(my_recipes_list) |
            edit_existing_recipe.to(view_recipe) |
            add_recipe.to(my_recipes_list) |
            delete_recipe.to(view_recipe)|
            save_edited_existing_recipe.to(edit_existing_recipe)|
            save_success_edited_existing_recipe.to(my_recipes_list))

    def on_enter_state(self, source:State, target: State, event: str):
        fsm_logger.debug(f"Перешли из {source.id} в {target.id}. Событие: {event}")

