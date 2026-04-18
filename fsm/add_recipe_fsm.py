from statemachine import State


class AddRecipeFSM(State.Compound):
    waiting_user_recipe = State(initial=True)
    edit_user_recipe = State()
    save_user_recipe = State()
    save_success = State(final=True)

    open_edit_recipe = waiting_user_recipe.to(edit_user_recipe)
    open_save_user_recipe = edit_user_recipe.to(save_user_recipe)
    confirm_save = save_user_recipe.to(save_success)

    back = edit_user_recipe.to(waiting_user_recipe) | save_user_recipe.to(edit_user_recipe)