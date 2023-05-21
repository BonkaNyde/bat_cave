import pickle, redis


from .exceptions import RedisKeyError
from ..config import Config



class Redis(object):
    
    def __init__(self, db:int=0):
        """
        pass in the db you want to use
        """
        if db:
            self.redis = redis.from_url(f'{Config.REDIS_URL}/{db}')
        else:
            self.redis = redis.from_url(Config.REDIS_URL)

    def clear_keys(self):
        self.redis.flushdb()


    def check_key_exists(self, key):

        if not isinstance(key, str):
            key = str(key)

        return bool(self.redis.exists(key))

    
    def delete_key(self, key):
        if not isinstance(key, str):
            key = str(key)
        
        return self.redis.delete(key)


    def get_key(self, key):
    
        if not isinstance(key, str):
            key = str(key)
           
        return self.redis.get(key)
    

    def keys(self):
        return self.redis.keys()


    def ping(self):
        return self.redis.ping()

    def set_key(self, key, value):

        if not isinstance(key, str):
            key = str(key)

        return self.redis.set(key, value)


    def set_keys(self, objects:dict):
    
        pipe = self.redis.pipeline()

        for key, value in objects.items():
            pipe.execute_command('set', key, pickle.dumps(value))

        pipe.execute()


    def save_list(self, key:str, list_):
        """
        """
        self.redis.rpush(key, *list_)


    def get_from_list(self, key, indices=[]):
        """
        """

        if not isinstance(key, str):
            key = str(key)

        pipe = self.redis.pipeline()
        for idx in indices:
            pipe.execute_command('lindex', key, idx)

        res = pipe.execute()

        return res


    def get_multiple_keys(self, keys=[]):
        """
        """

        res = []
        for key in keys:
            redis_value = self.redis.get(key)

            if redis_value is None:
                raise RedisKeyError

            obj = pickle.loads(redis_value)
            obj.update({'meal_id' : int(key)})
            res.append(obj)
            
        return res



app_cache = Redis(0)
rq_cache = Redis(1)
metrics_redis_cache = Redis(2)
connected_user_cache = Redis(3)
# Redis(4) is occupied by flask_session
flask_session_cache = Redis(4)
disconnected_user_cache = Redis(5)
