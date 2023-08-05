from motor.motor_asyncio import AsyncIOMotorClient
import redis
from .setting import load_config

CONF = load_config()

DEBUG = CONF.get("fastapi", dict())["debug"]
SECRET_KEY = CONF.get("fastapi", dict())["key"]
ENVIRONMENT = CONF.get("fastapi", dict())["environment"]
PROJECT_NAME = CONF.get("fastapi", dict())["projectName"]
ALGORITHM = CONF.get("fastapi", dict())["algorithm"]
BASEURL = CONF.get("fastapi", dict())["baseUrl"]

MGDB_CLIENT = AsyncIOMotorClient(
    host=CONF.get("mongodb", dict())["HOST"],
    port=CONF.get("mongodb", dict())["PORT"],
    username=CONF.get("mongodb", dict())["USER"],
    password=CONF.get("mongodb", dict())["PASSWORD"],
)

MGDB = MGDB_CLIENT[CONF.get("mongodb", dict())["NAME"]]

def close_db_client():
    MGDB_CLIENT.close()

REDQUE = redis.Redis(
    host=CONF.get("redis-queue", dict())["HOST"],
    port=CONF.get("redis-queue", dict())["PORT"],
    db=0,
)

REDATA = redis.Redis(
    host=CONF.get("redis-data", dict())["HOST"],
    port=CONF.get("redis-data", dict())["PORT"],
    db=0,
)

# HOST_TAP_DEVICE = "https://api.dev.katalis.info"

# mqtt_config = MQTTConfig(
#     host=CONF.get("mqtt-chat", dict())["HOST"],
#     port=CONF.get("mqtt-chat", dict())["PORT"],
#     keepalive=CONF.get("mqtt-chat", dict())["KEEPALIVE"],
#     username=CONF.get("mqtt-chat", dict())["USERNAME"],
#     password=CONF.get("mqtt-chat", dict())["PASSWORD"],
# )

# CONMQTT = FastMQTT(config=mqtt_config)
