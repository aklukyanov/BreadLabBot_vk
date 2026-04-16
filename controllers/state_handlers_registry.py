from controllers.delete_recipe import DeleteRecipeStateHandler
from controllers.main_menu_handlers import MainMenuStateHandler, ToolsMenuStateHandler
from controllers.my_recipes_menu_handlers import MyRecipesListStateHandler
from controllers.proportions_calc_handlers import LoadRecipeStateHandler, ChooseRecipeStateHandler, \
        WaitingMultiplierStateHandler, ShowResultProportionsCalcStateHandler
from controllers.starter_calc_handlers import ChooseDirectionStateHandler, WaitingSourdoughWeightStateHandler, \
        ChoosingStarterProportionsStateHandler, ShowResultStarterCalcStateHandler
from controllers.view_recipe import EditRecipeStateHandler

states={"main":MainMenuStateHandler(),
        "tools":ToolsMenuStateHandler(),
        "choose_direction":ChooseDirectionStateHandler(),
        "waiting_sourdough_weight":WaitingSourdoughWeightStateHandler(),
        "choosing_starter_proportions":ChoosingStarterProportionsStateHandler(),
        "show_result_starter_calc":ShowResultStarterCalcStateHandler(),
        "my_recipes_list":MyRecipesListStateHandler(),
        "view_recipe":EditRecipeStateHandler(),
        "delete_recipe":DeleteRecipeStateHandler(),
        "load_recipe":LoadRecipeStateHandler(),
        "choose_recipe":ChooseRecipeStateHandler(),
        "waiting_multiplier":WaitingMultiplierStateHandler(),
        "show_result_proportions_calc":ShowResultProportionsCalcStateHandler(),}