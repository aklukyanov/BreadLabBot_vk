from vkbottle.bot import Message
from vkbottle_types.events.bot_events import MessageEvent
from vkbottle_types.objects import parent

from controllers.state_handlers_registry import states
from fsm.main_menu_fsm import MainMenu
from logger import sm_logger
from storage import storage

fsm = MainMenu(strict=True)
class SessionManager:

    async def handle_event(self, event:MessageEvent):
        sm_logger.debug(f"Получил событие: {event}")

        #забирает инфо о событии
        peer_id=event.object.peer_id

        "забираем инфу о текущей сессии из хранилища"
        session_data=storage.get(peer_id)
        sm_logger.debug(f"Забрал инфу из базы: {session_data}")


        if session_data is None:
            await event.ctx_api.messages.send(
                message="Напишите 'Начать', чтобы начать сессию.",
                user_id=event.object.user_id,
                peer_id=event.object.peer_id,
                random_id=0)

        else:
            state_config=session_data["state_config"]
            current_state=state_config[-1]
            sm_logger.debug(f"Передаю управление {current_state}")
            cmd, session_data = await states[current_state].handle_event(event=event, session_data=session_data)
            sm_logger.debug(f" Получил от {current_state} команду {cmd} и данные {session_data}")

            if cmd is None:
                return

            fsm.current_state_value = current_state # загружаем состояние в фсм
            fsm.send(cmd) # делаем шаг в фсм

            new_current_state = list(fsm.configuration_values)[-1]
            parent_state=list(fsm.configuration_values)[0]


            if new_current_state in state_config: # если есть, значит это шаг назад
                new_current_state_index=state_config.index(new_current_state)
                new_state_config = state_config[:new_current_state_index + 1] # берем все состояния до текущего включительно (поэтому +1)
            else:
                if parent_state not in state_config and parent_state != new_current_state:
                    state_config.append(parent_state)

                state_config.append(new_current_state) # если состояния нет в списке, значит это шаг вперед.
                new_state_config = state_config

            session_data["state_config"] = new_state_config  # Обновляем временные данные
            sm_logger.debug(f"Новый state config: {new_state_config}")
            new_state = new_state_config[-1]  # Берём последний элемент — строку
            await states[new_state].show_screen(event, session_data) # вызываем экран нового состояния

            storage.set(key=peer_id, value=session_data)
            test_data = storage.get(key=event.object.peer_id)
            sm_logger.debug(f"Сохранил в storage {test_data}")
            print(fsm._graph().to_string())


    async def handle_message(self, message: Message):
        sm_logger.debug(f"Принял сообщение: {message}")

        peer_id = message.peer_id

        # Забираем инфу о текущей сессии из хранилища
        session_data = storage.get(peer_id)
        sm_logger.debug(f"Забрал инфу из базы: {session_data}")

        if session_data is None:
            await message.answer("Напишите 'Начать', чтобы начать сессию.")
            return

        state_config = session_data["state_config"]
        current_state = state_config[-1]
        sm_logger.debug(f"Передаю управление {current_state}")

        # Вызываем handle_message контроллера
        cmd, session_data = await states[current_state].handle_message(
            message=message,
            session_data=session_data
        )
        sm_logger.debug(f"Получил от {current_state} команду {cmd} и данные {session_data}")

        if cmd is None:
            return

        fsm.current_state_value = current_state  # загружаем состояние в фсм
        fsm.send(cmd)  # делаем шаг в фсм

        new_current_state = list(fsm.configuration_values)[-1]
        parent_state = list(fsm.configuration_values)[0]

        if new_current_state in state_config:  # если есть, значит это шаг назад
            new_current_state_index = state_config.index(new_current_state)
            new_state_config = state_config[
                :new_current_state_index + 1]  # берем все состояния до текущего включительно (поэтому +1)
        else:
            if parent_state not in state_config and parent_state != new_current_state:
                state_config.append(parent_state)

            state_config.append(new_current_state)  # если состояния нет в списке, значит это шаг вперед.
            new_state_config = state_config

        session_data["state_config"] = new_state_config  # Обновляем временные данные
        sm_logger.debug(f"Новый state config: {new_state_config}")

        new_state = new_state_config[-1]  # Берём последний элемент — строку
        await states[new_state].show_screen(message, session_data)  # вызываем экран нового состояния

        storage.set(key=peer_id, value=session_data)
        test_data = storage.get(key=peer_id)
        sm_logger.debug(f"Сохранил в storage {test_data}")
