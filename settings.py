import os

dev_base_url="http://127.0.0.1:8000"
prod_base_url="http://breadlab-server:8000"

CURRENT_URL=os.getenv("CURRENT_URL", 'http://127.0.0.1:8000')
CURRENT_STORAGE=os.getenv("CURRENT_STORAGE", 'ctx_storage')






