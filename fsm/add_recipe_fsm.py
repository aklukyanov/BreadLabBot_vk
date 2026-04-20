from statemachine import State, StateMachine


class AddRecipeFSM(State.Compound):
    waiting_user_recipe = State(initial=True)
    edit_added_recipe = State()
    save_added_recipe = State()
    save_success_added_recipe = State(final=True)

    open_edit_added_recipe = waiting_user_recipe.to(edit_added_recipe)
    open_save_added_recipe = edit_added_recipe.to(save_added_recipe)
    confirm_save = save_added_recipe.to(save_success_added_recipe)

    back = edit_added_recipe.to(waiting_user_recipe) | save_added_recipe.to(edit_added_recipe)



