from controllers.delete_recipe import DeleteRecipeStateHandler
from controllers.main_menu_handlers import MainMenuStateHandler, ToolsMenuStateHandler
from controllers.my_recipes_menu_handlers import MyRecipesListStateHandler
from controllers.starter_calc_handlers import ChooseDirectionStateHandler, WaitingSourdoughWeightStateHandler, \
        ChoosingStarterProportionsStateHandler, ShowResultStarterCalcStateHandler
from controllers.view_recipe import ViewRecipeStateHandler

states={"main":MainMenuStateHandler(),
        "tools":ToolsMenuStateHandler(),
        "choose_direction":ChooseDirectionStateHandler(),
        "waiting_sourdough_weight":WaitingSourdoughWeightStateHandler(),
        "choosing_starter_proportions":ChoosingStarterProportionsStateHandler(),
        "show_result_starter_calc":ShowResultStarterCalcStateHandler(),
        "my_recipes_list":MyRecipesListStateHandler(),
        "view_recipe":ViewRecipeStateHandler(),
        "delete_recipe":DeleteRecipeStateHandler()}