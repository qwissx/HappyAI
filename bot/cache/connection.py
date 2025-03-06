import redis

import settings as st


redis = Redis(host=st.redis_host, port=st.redis_port, db=0)
