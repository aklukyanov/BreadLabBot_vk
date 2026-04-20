from vkbottle import Keyboard, Callback

def error_keyboard(retry_cmd: str) -> str:
    """
    Возвращает клавиатуру с кнопками:
    - Попробовать ещё раз (cmd = retry_cmd)
    - Назад (back)
    - В главное меню (to_main)
    """
    return (
        Keyboard(inline=True)
        .add(Callback("🔄 Отправить заново", payload={"cmd": retry_cmd}))
        .row()
        .add(Callback("⬅️ Назад", payload={"cmd": "back"}))
        .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
    ).get_json()

def step_back_or_cancel_keyboard(step_back_cmd, cancel_cmd):
    return (
        Keyboard(inline=True)
        .add(Callback("⬅️ Назад", payload={"cmd": step_back_cmd}))
        .row()
        .add(Callback("🏠 В главное меню", payload={"cmd": cancel_cmd}))
    ).get_json()



#Главное меню
main_menu_keyboard = (
    Keyboard(inline=True)

    .add(Callback("📋 Мои рецепты", payload={"cmd": "my_recipes_menu"}))
    .row()
    .add(Callback("🔧 Инструменты", payload={"cmd": "tools"}))
    .row()
    .add(Callback("ℹ️ О проекте", payload={"cmd": "open_about"}))
).get_json()

#Инструменты
tools_menu_keyboard = (
    Keyboard(inline=True)
    .add(Callback("🧮 Калькулятор закваски", payload={"cmd": "open_starter_calc"}))
    .row()
    .add(Callback("⚖️ Расчет пропорций", payload={"cmd": "open_proportions_calc"}))
    .row()
    .add(Callback("◀️ Назад", payload={"cmd": "back"}))
    .row()
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()

#starter_calc
choose_direction_keyboard = (
    Keyboard(inline=True)
    .add(Callback("50% → 100%", payload={"cmd": "enter_direction", "direction": "50to100"}))
    .row()
    .add(Callback("100% → 50%", payload={"cmd": "enter_direction", "direction": "100to50"}))
    .row()
    .add(Callback("◀️ Назад", payload={"cmd": "back"}))
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()

choosing_starter_proportions_50to100_keyboard = (
    Keyboard(inline=True)
    .add(Callback("1:1:1", payload={"cmd": "calculate", "starter_proportions": "1:1:1"}))
    .add(Callback("1:2:2", payload={"cmd": "calculate", "starter_proportions": "1:2:2"}))
    .add(Callback("1:3:3", payload={"cmd": "calculate", "starter_proportions": "1:3:3"}))
    .add(Callback("1:4:4", payload={"cmd": "calculate", "starter_proportions": "1:4:4"}))
    .row()
    .add(Callback("1:5:5", payload={"cmd": "calculate", "starter_proportions": "1:5:5"}))
    .add(Callback("1:6:6", payload={"cmd": "calculate", "starter_proportions": "1:6:6"}))
    .add(Callback("1:7:7", payload={"cmd": "calculate", "starter_proportions": "1:7:7"}))
    .add(Callback("1:8:8", payload={"cmd": "calculate", "starter_proportions": "1:8:8"}))
    .row()
    .add(Callback("⬅️ Назад", payload={"cmd": "back"}))
    .row()
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()

choosing_starter_proportions_100to50_keyboard = (
    Keyboard(inline=True)
    .add(Callback("1:0.5:1", payload={"cmd": "calculate", "starter_proportions": "1:0.5:1"}))
    .add(Callback("1:1:2", payload={"cmd": "calculate", "starter_proportions": "1:1:2"}))
    .add(Callback("1:1.5:3", payload={"cmd": "calculate", "starter_proportions": "1:1.5:3"}))
    .add(Callback("1:2:4", payload={"cmd": "calculate", "starter_proportions": "1:2:4"}))
    .row()
    .add(Callback("⬅️ Назад", payload={"cmd": "back"}))
    .row()
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()

#my_recipes_menu

my_recipes_menu_keyboard = (
    Keyboard(inline=True)
    .add(Callback("➕ Добавить рецепт", payload={"cmd": "open_add_recipe"}))
    .row()
    .add(Callback("📋 Мои рецепты", payload={"cmd": "show_recipes_list"}))
    .row()
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()

back_to_recipes_keyboard = (
    Keyboard(inline=True)
    .add(Callback("📋 Мои рецепты", payload={"cmd": "open_my_recipes_list"}))
    .row()
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()

def view_recipe_keyboard(mode) -> str:
    """Клавиатура для экрана отображения рецепта"""
    keyboard= Keyboard(inline=True)
    if mode=="edit_recipe":
        keyboard.add(Callback("✏️ Редактировать", payload={"cmd": "open_edit_existing_recipe"}))
        keyboard.row()
        keyboard.add(Callback("🗑 Удалить", payload={"cmd": "open_delete_recipe"}))
        keyboard.row()
        keyboard.add(Callback("◀️ Назад", payload={"cmd": "back"}))
        keyboard.row()
        keyboard.add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
        return keyboard.get_json()
    if mode=="proportions_calc":
        keyboard.add(Callback("◀️ Назад", payload={"cmd": "back"}))
        keyboard.row()
        keyboard.add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
        return keyboard.get_json()


back_only_keyboard = (
    Keyboard(inline=True)
    .add(Callback("⬅️ Назад", payload={"cmd": "back"}))
).get_json()




def approve_keyboard(yes_cmd: str, no_cmd: str) -> str:
    return (
        Keyboard(inline=True)
        .add(Callback("✅ Да", payload={"cmd": yes_cmd}))
        .row()
        .add(Callback("❌ Нет", payload={"cmd": no_cmd}))
    ).get_json()

def recipes_keyboard(recipes, current_page, has_prev, has_next):
#создает клавиатуру из рецептов пользователя
    keyboard = Keyboard(inline=True)
    # Кнопки рецептов (максимум 4)
    for recipe in recipes:
        title = recipe['recipe']['data']['title']
        recipe_id = recipe['id']

        keyboard.add(Callback(title, payload={"cmd": "open_view_recipe", "recipe_id": recipe_id}))
        keyboard.row()

    # Навигация (2 кнопки)
    if has_prev:
        keyboard.add(
            Callback("◀️ Назад", payload={"cmd": "show_recipes_list", "page": current_page - 1}))

    if has_next:
        keyboard.add(
            Callback("Вперёд ▶️", payload={"cmd": "show_recipes_list", "page": current_page + 1}))

    keyboard.row()
    keyboard.add(Callback("➕ Добавить рецепт", payload={"cmd": "open_add_recipe"}))
    keyboard.add(Callback("🏠 В главное меню", payload={"cmd": 'to_main'}))
    return keyboard.get_json()



def recipes_keyboard_proportions_calc(recipes, current_page, has_prev, has_next):
    # создает клавиатуру из рецептов пользователя
    keyboard = Keyboard(inline=True)
    # Кнопки рецептов (максимум 4)
    for recipe in recipes:
        title = recipe['recipe']['data']['title']
        recipe_id = recipe['id']

        keyboard.add(Callback(title, payload={"cmd": "enter_recipe", "recipe_id": recipe_id}))
        keyboard.row()

    # Навигация (2 кнопки)
    if has_prev:
        keyboard.add(
            Callback("◀️ Назад", payload={"cmd": "show_recipes_list", "page": current_page - 1}))

    if has_next:
        keyboard.add(
            Callback("Вперёд ▶️", payload={"cmd": "show_recipes_list", "page": current_page + 1}))

    keyboard.row()
    keyboard.add(Callback("◀️ Назад", payload={"cmd": "back"}))
    keyboard.add(Callback("🏠 В главное меню", payload={"cmd": 'to_main'}))
    return keyboard.get_json()

load_recipe_keyboard = (
    Keyboard(inline=True)
    .add(Callback("📋 Список рецептов", payload={"cmd": "open_choose_recipe_proportions_calc"}))
    .row()
    .add(Callback("➕ Добавить новый", payload={"cmd": "open_add_recipe_proportions_calc"}))
    .row()
    .add(Callback("⬅️ Назад", payload={"cmd": "back"}))  # 👈 back вместо to_main
    .row()
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()


def edit_recipe_approve_keyboard(recipe_id, mode=None):
    if mode=="me_recipes":
        keyboard= Keyboard(inline=True)
        keyboard.add(Callback("✅ Всё верно", payload={"cmd": "approve_recipe_edit", "recipe_id": recipe_id}))
        keyboard.row()
        keyboard.add(Callback("🔄 Начать заново", payload={"cmd": "edit_recipe", "recipe_id": recipe_id}))
        keyboard.row()
        keyboard.add(Callback("📋 Список рецептов", payload={"cmd": "my_recipes_list"}))
        keyboard.row()
        keyboard.add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
        return keyboard.get_json()
    if mode=='add_recipe':
        keyboard=Keyboard(inline=True)
        keyboard.add(Callback("✅ Всё верно", payload={"cmd": "approve_recipe_edit", "recipe_id": recipe_id, "mode":mode}))
        keyboard.row()
        keyboard.add(Callback("⬅️ Назад", payload={"cmd": mode,"mode":mode}))
        keyboard.row()
        keyboard.add(Callback("🏠 В главное меню", payload={"cmd": 'to_main',"mode":mode}))
        return keyboard.get_json()


def approving_edit_keyboard(approve_cmd: str, restart_cmd: str) -> str:
    return (
        Keyboard(inline=True)
        .add(Callback("✅ Всё верно", payload={"cmd": approve_cmd}))
        .row()
        .add(Callback("🔄 Начать заново", payload={"cmd": restart_cmd}))
        .row()
        .add(Callback("⬅️ Назад", payload={"cmd": "back"}))
        .row()
        .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
    ).get_json()

save_or_cancel_keyboard = (
    Keyboard(inline=True)
    .add(Callback("💾 Сохранить", payload={"cmd": "confirm_save"}))
    .row()
    .add(Callback("⬅️ Назад", payload={"cmd": "back"}))
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()

save_choice_keyboard = (
    Keyboard(inline=True)
    .add(Callback("✨ Сохранить как новый", payload={"cmd": "save_as_new"}))
    .row()
    .add(Callback("📎 Сохранить как версию", payload={"cmd": "save_as_version"}))
    .row()
    .add(Callback("⬅️ Назад", payload={"cmd": "back"}))
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()

update_existing_recipe_keyboard = (
    Keyboard(inline=True)
    .add(Callback("🔄 Обновить существующий", payload={"cmd": "update_existing_recipe"}))
    .row()
    .row()
    .add(Callback("⬅️ Назад", payload={"cmd": "back"}))
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()

confirm_update_existing_recipe_keyboard = (
    Keyboard(inline=True)
    .add(Callback("🔄 Подтвердить обновление", payload={"cmd": "confirm_update_existing_recipe"}))
    .row()
    .row()
    .add(Callback("⬅️ Назад", payload={"cmd": "back"}))
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()



to_my_recipes_or_main_keyboard = (
    Keyboard(inline=True)
    .add(Callback("📋 В мои рецепты", payload={"cmd": "back"}))
    .row()
    .add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
).get_json()