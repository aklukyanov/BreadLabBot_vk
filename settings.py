dev_base_url="http://127.0.0.1:8000"
prod_base_url="http://breadlab-server:8000"

#MODE может быть prod или dev
MODE='prod'

if MODE=='dev':
    CURRENT_URL = dev_base_url
    CURRENT_STORAGE = 'dev'  # 'prod' - redis или 'dev' для разработки
elif MODE=='prod':
    CURRENT_URL=prod_base_url
    CURRENT_STORAGE = 'prod'


