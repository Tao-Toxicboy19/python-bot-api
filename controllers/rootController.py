from config.redis_config import redis_client
import json

def rootController():
    values = json.loads(redis_client.get("result:3m"))

    return values