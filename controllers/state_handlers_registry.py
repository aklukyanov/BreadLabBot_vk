from controllers.delete_recipe import DeleteRecipeStateHandler
from controllers.main_menu_handlers import MainMenuStateHandler, ToolsMenuStateHandler, AboutBreadLabStateHandler
from controllers.my_recipes_menu_handlers import MyRecipesListStateHandler, WaitingUserRecipeStateHandler
from controllers.save_recipe_handlers import SaveAddedRecipeStateHandler, SaveEditedExistingRecipesStateHandler, \
        SaveSuccessStateHandler
from controllers.base_edit_recipe_handler import EditAddedRecipeStateHandler, EditExistingRecipeStateHandler
from controllers.proportions_calc_handlers import LoadRecipeProportionsCalcStateHandler, ChooseRecipeProportionsCalcStateHandler, \
        WaitingMultiplierStateHandler, ShowResultProportionsCalcStateHandler
from controllers.starter_calc_handlers import ChooseDirectionStateHandler, WaitingSourdoughWeightStateHandler, \
        ChoosingStarterProportionsStateHandler, ShowResultStarterCalcStateHandler
from controllers.view_recipe import EditRecipeStateHandler

states={"main":MainMenuStateHandler(),
        "tools":ToolsMenuStateHandler(),
        "about":AboutBreadLabStateHandler(),
        "choose_direction":ChooseDirectionStateHandler(),
        "waiting_sourdough_weight":WaitingSourdoughWeightStateHandler(),
        "choosing_starter_proportions":ChoosingStarterProportionsStateHandler(),
        "show_result_starter_calc":ShowResultStarterCalcStateHandler(),
        "my_recipes_list":MyRecipesListStateHandler(),
        "view_recipe":EditRecipeStateHandler(),
        "delete_recipe":DeleteRecipeStateHandler(),
        "load_recipe_proportions_calc":LoadRecipeProportionsCalcStateHandler(),
        "choose_recipe_proportions_calc":ChooseRecipeProportionsCalcStateHandler(),
        "waiting_multiplier":WaitingMultiplierStateHandler(),
        "show_result_proportions_calc":ShowResultProportionsCalcStateHandler(),
        "waiting_user_recipe":WaitingUserRecipeStateHandler(),
        "edit_added_recipe":EditAddedRecipeStateHandler(),
        "edit_existing_recipe":EditExistingRecipeStateHandler(),
        "save_added_recipe":SaveAddedRecipeStateHandler(),
        "save_edited_existing_recipe":SaveEditedExistingRecipesStateHandler(),
        "save_success_edited_existing_recipe":SaveSuccessStateHandler(),
        "save_success_added_recipe":SaveSuccessStateHandler(),

        "waiting_user_recipe_proportions_calc": WaitingUserRecipeStateHandler(),
        "edit_added_recipe_proportions_calc": EditAddedRecipeStateHandler(),
        "save_added_recipe_proportions_calc":SaveAddedRecipeStateHandler(),
        }