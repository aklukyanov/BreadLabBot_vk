def convert_dict_to_pretty_print(dict_to_convert: dict, multiplier: int = None, show_hydration: bool = True) -> str:
    """
    Преобразует рецепт из словаря в красивое текстовое представление.

    Args:
        dict_to_convert: Словарь с рецептом (должен содержать 'title' и 'groups').
        multiplier: Множитель для отображения в заголовке (например, ×2).
        show_hydration: Показывать ли гидратацию в конце.

    Returns:
        Отформатированная строка для вывода пользователю.
    """
    recipe = dict_to_convert
    answer_for_user = []

    # Заголовок
    if recipe.get('title') is None:
        title = '🍞 БЕЗ НАЗВАНИЯ'
    else:
        title = f"🍞 {recipe['title']}"

    if multiplier:
        title += f" ×{multiplier}"

    answer_for_user.append(title + '\n')

    # Группы ингредиентов
    for group in recipe['groups']:
        answer_for_user.append(f"{group['name']}:")

        for ingredient in group['ingredients']:
            name = ingredient['name']
            quantity = ingredient.get('amount', ingredient.get('quantity'))
            unit = ingredient.get('unit', '')

            if quantity is None:
                answer_for_user.append(f"• {name} - ?")
            else:
                formatted_quantity = format_quantity_and_unit(quantity, unit)
                answer_for_user.append(f"• {name} - {formatted_quantity}")

        answer_for_user.append("")  # пустая строка после каждой группы

    # Гидратация
    if show_hydration and 'hydration' in recipe:
        answer_for_user.append(f"💧 Гидратация: {recipe['hydration']}%")

    return "\n".join(answer_for_user)


def format_quantity_and_unit(quantity: float, unit: str) -> str:
    """
    Форматирует количество и единицу измерения для красивого вывода.

    Поддерживает:
    - г. ↔ кг.
    - мл. ↔ л.
    - Склонение 'пакетик', 'стакан'.

    Args:
        quantity: Количество.
        unit: Единица измерения.

    Returns:
        Отформатированная строка (например, "1.5 кг." или "3 стакана").
    """
    # Граммы → килограммы
    if unit == 'г.' and quantity >= 1000:
        kg = quantity / 1000
        return f"{int(kg)} кг." if kg.is_integer() else f"{kg} кг."

    # Килограммы → граммы
    if unit == 'кг.' and quantity < 1:
        g = quantity * 1000
        return f"{int(g)} г." if g.is_integer() else f"{g} г."

    # Миллилитры → литры
    if unit == 'мл.' and quantity >= 1000:
        l = quantity / 1000
        return f"{int(l)} л." if l.is_integer() else f"{l} л."

    # Литры → миллилитры
    if unit == 'л.' and quantity < 1:
        ml = quantity * 1000
        return f"{int(ml)} мл." if ml.is_integer() else f"{ml} мл."

    # Склонение "пакетик"
    if unit == 'пакетик':
        if quantity == 1:
            return f"{quantity} пакетик"
        if 1 < quantity < 5:
            return f"{quantity} пакетика"
        if quantity >= 5:
            return f"{quantity} пакетиков"

    # Склонение "стакан"
    if unit == 'стакан':
        if quantity == 1:
            return f"{quantity} стакан"
        if 1 < quantity < 5:
            return f"{quantity} стакана"
        if quantity >= 5:
            return f"{quantity} стаканов"

    # По умолчанию
    return f"{quantity} {unit}"