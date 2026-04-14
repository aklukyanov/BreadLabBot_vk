from vkbottle import Keyboard, Callback

def step_back_or_cancel_keyboard(step_back_cmd, cancel_cmd):
    return (
        Keyboard(inline=True)
        .add(Callback("⬅️ Назад", payload={"cmd": step_back_cmd}))
        .row()
        .add(Callback("🏠 В главное меню", payload={"cmd": cancel_cmd}))
    ).get_json()


def rerun_function_keyboard(rerun_cmd, to_main_cmd, rerun_func):
    keyboard=Keyboard(inline=True)
    if rerun_func=='starter_calc':
            keyboard.add(Callback("🔄 Посчитать заново", payload={"cmd": rerun_cmd}))
    if rerun_func=='edit_recipe':
        keyboard.add(Callback("📋 Список рецептов", payload={"cmd": rerun_cmd}))
    if rerun_func == 'proportions_calc':
        keyboard.add(Callback("🔄 Посчитать заново", payload={"cmd": rerun_cmd}))

    keyboard.row()
    keyboard.add(Callback("🏠 В главное меню", payload={"cmd": to_main_cmd})).get_json()
    return keyboard

#Главное меню
main_menu_keyboard = (
    Keyboard(inline=True)
    .add(Callback("🎯 Новая выпечка", payload={"cmd": "new_bake"}))
    .row()
    .add(Callback("📋 Мои рецепты", payload={"cmd": "my_recipes"}))
    .row()
    .add(Callback("🔧 Инструменты", payload={"cmd": "tools"}))
    .row()
    .add(Callback("ℹ️ О проекте", payload={"cmd": "about"}))
).get_json()

#Инструменты
tools_menu_keyboard = (
    Keyboard(inline=True)
    .add(Callback("🧮 Калькулятор закваски", payload={"cmd": "open_starter_calc"}))
    .row()
    .add(Callback("⚖️ Расчет пропорций", payload={"cmd": "proportions_calc"}))
    .row()
    .add(Callback("💧 Трекер гидратации", payload={"cmd": "hydration_tracker"}))
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




def approve_keyboard(yes_cmd, no_cmd, recipe_id):
    return (
        Keyboard(inline=True)
        .add(Callback("✅ Да", payload={"cmd": yes_cmd, 'recipe_id':recipe_id}))
        .row()
        .add(Callback("❌ Нет", payload={"cmd": no_cmd, 'recipe_id':recipe_id}))
    ).get_json()

def recipes_keyboard(recipes, current_page, has_prev, has_next, mode=''):
#создает клавиатуру из рецептов пользователя
    keyboard = Keyboard(inline=True)

    # Кнопки рецептов (максимум 4)
    for recipe in recipes:
        title = recipe['recipe']['data']['title']
        recipe_id = recipe['id']

        keyboard.add(Callback(title, payload={"cmd": "view_recipe", "recipe_id": recipe_id,"mode":mode}))
        keyboard.row()

    # Навигация (2 кнопки)
    if has_prev:
        keyboard.add(
            Callback("◀️ Назад", payload={"cmd": "recipes_page", "page": current_page - 1, "mode":mode}))

    if has_next:
        keyboard.add(
            Callback("Вперёд ▶️", payload={"cmd": "recipes_page", "page": current_page + 1, "mode":mode}))

    keyboard.row()

    if mode == 'my_recipes':
        keyboard.add(Callback("➕ Добавить рецепт", payload={"cmd": "add_recipe"}))
        keyboard.add(Callback("📋 Мои рецепты", payload={"cmd": "my_recipes"}))
        keyboard.add(Callback("🏠 В главное меню", payload={"cmd": 'to_main'}))
    if mode=='proportions_calc':
        keyboard.add(Callback("⚖️ Расчет пропорций", payload={"cmd": "proportions_calc", "mode": mode}))
        keyboard.add(Callback("🏠 В главное меню", payload={"cmd": 'to_main', "mode": mode}))

    return keyboard.get_json()

def my_recipes_keyboard (mode=''):
        keyboard=Keyboard(inline=True)
        keyboard.add(Callback("📋 Список рецептов", payload={"cmd": "my_recipes_list", "mode":mode}))
        keyboard.row()
        keyboard.add(Callback("➕ Добавить новый", payload={"cmd": "add_recipe", "mode":mode}))
        keyboard.row()
        keyboard.add(Callback("⬅️ Назад", payload={"cmd": 'to_main'}))
        keyboard.row()
        keyboard.add(Callback("🏠 В главное меню", payload={"cmd": 'to_main'}))
        return keyboard.get_json()



def edit_recipe_keyboard(recipe_id, mode=None):
    if mode=='my_recipes':
        keyboard=Keyboard(inline=True)
        keyboard.add(Callback("✏️ Редактировать", payload={"cmd": "edit_recipe", "recipe_id": recipe_id, "mode":mode}))
        keyboard.add(Callback("🗑 Удалить", payload={"cmd": "delete_recipe", "recipe_id": recipe_id, "mode":mode}))
        keyboard.row()
        keyboard.add(Callback("◀️ Назад", payload={"cmd": "my_recipes_list", "mode":mode}))
        keyboard.row()
        keyboard.add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
        return keyboard.get_json()
    if mode=='add_recipe':
        keyboard=Keyboard(inline=True)
        keyboard.add(Callback("✏️ Редактировать", payload={"cmd": "edit_recipe", "recipe_id": recipe_id, "mode":mode}))
        keyboard.row()
        keyboard.add(Callback("◀️ Назад", payload={"cmd": "my_recipes_list", "mode":mode}))
        keyboard.row()
        keyboard.add(Callback("🏠 В главное меню", payload={"cmd": "to_main"}))
        return keyboard.get_json()


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


def approving_keyboard(approve_cmd, step_back_cmd, to_main_cmd, mode=None):
    return (
        Keyboard(inline=True)
        .add(Callback("✅ Всё верно", payload={"cmd": approve_cmd, "mode":mode}))
        .row()
        .add(Callback("⬅️ Назад", payload={"cmd": step_back_cmd,"mode":mode}))
        .row()
        .add(Callback("🏠 В главное меню", payload={"cmd": to_main_cmd,"mode":mode}))
    ).get_json()
