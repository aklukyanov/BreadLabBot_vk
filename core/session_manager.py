from typing import Any, Callable, Optional, Tuple

from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent

from controllers.state_handlers_registry import states
from fsm.main_menu_fsm import MainMenu
from logger import sm_logger
from storage import storage

# Единый экземпляр FSM для всего приложения
fsm = MainMenu(strict=True)

class SessionManager:
    """
    Менеджер сессий пользователей.
    Отвечает за загрузку/сохранение сессии, вызов контроллеров, управление FSM и стеком навигации.
    """

    # ========================================================================
    # ПУБЛИЧНЫЕ МЕТОДЫ-АДАПТЕРЫ
    # ========================================================================

    async def handle_event(self, event: MessageEvent) -> None:
        """Обработка callback-событий от inline-кнопок."""
        await self._process(
            peer_id=event.object.peer_id,
            event=event,
            controller_method_name="handle_event",
            log_prefix="событие",
            send_startup_message=lambda: event.ctx_api.messages.send(
                message="Напишите 'Начать', чтобы начать сессию.",
                user_id=event.object.user_id,
                peer_id=event.object.peer_id,
                random_id=0
            )
        )

    async def handle_message(self, message: Message) -> None:
        """Обработка текстовых сообщений."""
        await self._process(
            peer_id=message.peer_id,
            event=message,
            controller_method_name="handle_message",
            log_prefix="сообщение",
            send_startup_message=lambda: message.answer("Напишите 'Начать', чтобы начать сессию.")
        )

    # ========================================================================
    # УНИВЕРСАЛЬНЫЙ РАБОТНИК (Сердце менеджера)
    # ========================================================================

    async def _process(
        self,
        peer_id: int,
        event: Any,
        controller_method_name: str,
        log_prefix: str,
        send_startup_message: Callable[[], Any]
    ) -> None:
        """
        Универсальный обработчик всех типов событий.

        Args:
            peer_id: ID пользователя/чата.
            event: Объект события (MessageEvent, Message, и т.д.).
            controller_method_name: Имя метода контроллера для вызова.
            log_prefix: Префикс для логов (напр., "событие", "сообщение").
            send_startup_message: Функция для отправки приветственного сообщения,
                                  если сессия не найдена.
        """
        sm_logger.debug(f"Получил {log_prefix}: {event}")

        # 1. Загрузка сессии из хранилища
        session_data = storage.get(peer_id)
        sm_logger.debug(f"Забрал данные из базы: {session_data}")

        if session_data is None:
            await send_startup_message()
            return

        # 2. Получение текущего состояния и вызов контроллера
        state_config = session_data["state_config"]
        current_state = state_config[-1]
        sm_logger.debug(f"Передаю управление {current_state}")

        #    Получаем объект контроллера, который отвечает за текущее состояние пользователя.
        #    states — это словарь, где ключ — имя состояния ("main": MainMenuState()), а значение — экземпляр контроллера.
        controller = states[current_state]
        #    Извлекаем из контроллера нужный метод по его имени.
        #    controller_method_name — это строка, например "handle_event" или "handle_message".
        #    getattr(controller, "handle_event") возвращает саму функцию controller.handle_event.
        handler = getattr(controller, controller_method_name)
        #    Вызываем этот метод, передавая ему событие и данные сессии.
        #    Метод возвращает кортеж: (команда для FSM, обновлённая session_data).
        cmd, session_data = await handler(event, session_data)

        sm_logger.debug(f"Получил от {current_state} команду {cmd} и данные {session_data}")

        if cmd is None:
            return

        # 3. Работа с FSM
        fsm.current_state_value = current_state
        fsm.send(cmd)

        # 4. Обновление стека навигации
        new_state_config = self._update_navigation_stack(state_config, fsm)
        session_data["state_config"] = new_state_config
        sm_logger.debug(f"Новый state config: {new_state_config}")

        # 5. Отрисовка нового экрана
        new_state = new_state_config[-1]
        await states[new_state].show_screen(event, session_data)

        # 6. Сохранение сессии
        storage.set(key=peer_id, value=session_data)
        sm_logger.debug(f"Сохранил в storage {session_data}")

    # ========================================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ
    # ========================================================================

    def _update_navigation_stack(self, state_config: list, fsm: MainMenu) -> list:
        """
        Обновляет стек навигации на основе нового состояния FSM.

        Args:
            state_config: Текущий стек навигации.
            fsm: Экземпляр конечного автомата.

        Returns:
            Обновлённый стек навигации.
        """
        fsm_config = list(fsm.configuration_values)
        new_current_state = fsm_config[-1]
        parent_state = fsm_config[0]

        if new_current_state in state_config:
            # Шаг назад: обрезаем стек до найденного состояния
            idx = state_config.index(new_current_state)
            return state_config[:idx + 1]
        else:
            # Шаг вперёд: добавляем родителя (если нужно) и новое состояние
            if parent_state not in state_config and parent_state != new_current_state:
                state_config.append(parent_state)
            state_config.append(new_current_state)
            return state_config