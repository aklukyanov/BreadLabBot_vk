import pytest
from core.session_manager import SessionManager
from fsm.main_menu_fsm import MainMenu


@pytest.fixture(scope="module")
def fsm():
    return MainMenu(strict=True)

@pytest.fixture(scope="module")
def session_manager():
    return SessionManager()


def test_step_forward(session_manager, fsm):
    state_config = ["main"]
    fsm.current_state_value = "main"
    fsm.send("open_tools")
    new_config = session_manager._update_navigation_stack(state_config, fsm)
    assert new_config == ["main", "tools_menu", "tools"]


def test_step_backward(session_manager, fsm):
    state_config = ["main", "tools_menu", "tools", "starter_calc", "choose_direction"]
    fsm.current_state_value = "choose_direction"
    fsm.send("back")
    new_config = session_manager._update_navigation_stack(state_config, fsm)
    assert new_config == ["main", "tools_menu", "tools"]


def test_back_to_main_menu(session_manager, fsm):
    """Проверяет, что при возврате в главное меню стек сбрасывается до ['main']."""
    state_config = ["main", "my_recipes_menu", "my_recipes_list", "view_recipe", "delete_recipe"]
    fsm.current_state_value = "delete_recipe"
    fsm.send("to_main")  # Переход в главное меню

    new_config = session_manager._update_navigation_stack(state_config, fsm)

    assert new_config == ["main"]