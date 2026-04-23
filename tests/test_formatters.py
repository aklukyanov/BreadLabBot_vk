import pytest

from utils.formatters import format_quantity_and_unit


class TestFormatQuantityAndUnit:

    @pytest.mark.parametrize('quantity,unit,expected', [
        pytest.param(1000, "г.", "1 кг."),
        pytest.param(1500, "г.", "1.5 кг."),
        pytest.param(500, "г.", "500 г."),
        # Килограммы → граммы
        pytest.param(0.5, "кг.", "500 г."),
        pytest.param(1, "кг.", "1 кг."),
        # Миллилитры → литры
        pytest.param(1000, "мл.", "1 л."),
        # Пакетики
        pytest.param(1, "пакетик", "1 пакетик"),
        pytest.param(3, "пакетик", "3 пакетика"),
        pytest.param(5, "пакетик", "5 пакетиков"),
        # Стаканы
        pytest.param(1, "стакан", "1 стакан"),
        pytest.param(3, "стакан", "3 стакана"),
        # Обычные единицы
        pytest.param(200, "г.", "200 г."),
        # Граничные
        pytest.param(0, "г.", "0 г."),
        pytest.param(-5, "г.", "-5 г."),
        pytest.param(0.5, "г.", "0.5 г."),
        # Неизвестная единица
        pytest.param(10, "ложка", "10 ложка"),
        # Пустая единица
        pytest.param(10, "", "10 "),
    ])
    def test_format_grams_to_kilograms(self,quantity,unit,expected):
        assert format_quantity_and_unit(quantity,unit) == expected


import pytest
from utils.formatters import convert_dict_to_pretty_print


class TestConvertDictToPrettyPrint:

    # Образец рецепта
    SAMPLE_RECIPE = {
        "title": "БЕЛЫЙ ХЛЕБ",
        "groups": [
            {
                "name": "Опара",
                "ingredients": [
                    {"name": "мука", "quantity": 150, "unit": "г."},
                    {"name": "вода", "quantity": 150, "unit": "мл."},
                    {"name": "закваска", "quantity": 30, "unit": "г."}
                ]
            },
            {
                "name": "Тесто",
                "ingredients": [
                    {"name": "мука", "quantity": 350, "unit": "г."},
                    {"name": "вода", "quantity": 200, "unit": "мл."},
                    {"name": "соль", "quantity": 10, "unit": "г."}
                ]
            }
        ],
        "hydration": 70.0
    }

    def test_basic_recipe(self):
        result = convert_dict_to_pretty_print(self.SAMPLE_RECIPE)
        assert "🍞 БЕЛЫЙ ХЛЕБ" in result
        assert "Опара:" in result
        assert "• мука - 150 г." in result
        assert "Тесто:" in result
        assert "💧 Гидратация: 70.0%" in result

    def test_with_multiplier(self):
        result = convert_dict_to_pretty_print(self.SAMPLE_RECIPE, multiplier=2)
        assert "🍞 БЕЛЫЙ ХЛЕБ ×2" in result

    def test_without_hydration(self):
        result = convert_dict_to_pretty_print(self.SAMPLE_RECIPE, show_hydration=False)
        assert "💧 Гидратация" not in result

    def test_null_title(self):
        recipe = {**self.SAMPLE_RECIPE, "title": None}
        result = convert_dict_to_pretty_print(recipe)
        assert "🍞 БЕЗ НАЗВАНИЯ" in result

    def test_missing_quantity(self):
        recipe = {
            "title": "ТЕСТ",
            "groups": [
                {"name": "Ингредиенты", "ingredients": [
                    {"name": "мука", "unit": "г."}  # quantity отсутствует
                ]}
            ]
        }
        result = convert_dict_to_pretty_print(recipe)
        assert "• мука - ?" in result

    def test_uses_amount_field(self):
        """Проверяет, что функция использует поле 'amount', если 'quantity' нет."""
        recipe = {
            "title": "ТЕСТ",
            "groups": [
                {"name": "Ингредиенты", "ingredients": [
                    {"name": "мука", "amount": 500, "unit": "г."}
                ]}
            ]
        }
        result = convert_dict_to_pretty_print(recipe)
        assert "• мука - 500 г." in result


