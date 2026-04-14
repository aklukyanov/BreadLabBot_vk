import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S"
)

logging.getLogger("vkbottle").setLevel(logging.WARNING)
logging.getLogger("statemachine.engines.sync").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("statemachine.invoke").setLevel(logging.WARNING)
logging.getLogger("statemachine.engines.base").setLevel(logging.WARNING)


sm_logger = logging.getLogger("BreadLab. 📦 SessionManager")
fsm_logger = logging.getLogger("BreadLab. 🤖 FSM")
api_client_logger = logging.getLogger("BreadLab. APIClient")
