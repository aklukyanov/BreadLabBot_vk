from statemachine import State

from logger import fsm_logger


class SessionMenuFSM(State.Compound):

    choose_recipe=State(initial=True)
    choose_session=State()
    baking_session=State()


    open_choose_session = choose_recipe.to(choose_session) # Показ рецепта + меню ("Начать новую" или "Продолжить")
    open_baking_session = choose_session.to(baking_session) # Режим активной сессии. Добавление фото и текста


    back = (baking_session.to(choose_session) |
            choose_session.to(choose_recipe))

    def on_enter_state(self, source:State, target: State, event: str):
        fsm_logger.debug(f"Перешли из {source.id} в {target.id}. Событие: {event}")