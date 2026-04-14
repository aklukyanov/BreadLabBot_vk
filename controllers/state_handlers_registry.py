from controllers.main_manu_handlers import MainMenuState, ToolsMenuState
from controllers.starter_calc_handlers import ChooseDirectionStateHandler, WaitingSourdoughWeightStateHandler, \
        ChoosingStarterProportionsStateHandler, ShowResultStarterCalcStateHandler

states={"main":MainMenuState(),
        "tools":ToolsMenuState(),
        "choose_direction":ChooseDirectionStateHandler(),
        "waiting_sourdough_weight":WaitingSourdoughWeightStateHandler(),
        "choosing_starter_proportions":ChoosingStarterProportionsStateHandler(),
        "show_result_starter_calc":ShowResultStarterCalcStateHandler()}