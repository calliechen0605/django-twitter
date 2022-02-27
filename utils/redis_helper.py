from django.conf import settings
from utils.redis_client import RedisClient
from utils.redis_serializers import DjangoModelSerializer


class RedisHelper:

    @classmethod
    def load_objects(cls, key, queryset):
        conn = RedisClient.get_connection()

        #if in cache
        if conn.exists(key):
            serialized_list = conn.lrange(key, 0, -1)
            objects = []
            for serialized_data in serialized_list:
                deserialized_obj = DjangoModelSerializer.deserialize(serialized_data)
                objects.append(deserialized_obj)
            return objects

        cls._load_objects_to_cache(key, queryset)

        #switch back to list. Data are stored as list
        return list(queryset)

    @classmethod
    def push_object(cls, key, obj, queryset):
        conn = RedisClient.get_connection()
        if not conn.exists(key):
            cls._load_objects_to_cache(key, queryset)
            return
        serialized_data = DjangoModelSerializer.serialize(obj)
        #lpush, if key doesnt exist, it will create (key, list)
        conn.lpush(key, serialized_data)
        # control the list length, remaining segment
        conn.ltrim(key, 0, settings.REDIS_LIST_LENGTH_LIMIT - 1)

    @classmethod
    def _load_objects_to_cache(cls, key, objects):
        conn = RedisClient.get_connection()

        serialized_list = []
        for obj in objects[:settings.REDIS_LIST_LENGTH_LIMIT]:
            serialized_data = DjangoModelSerializer.serialize(obj)
            serialized_list.append(serialized_data)

        if serialized_list:
            # '*' means adding the element to conn one by one; unpack element for coder
            # *[1,2,3] -> 1, 2, 3
            # 1 次网络请求， 传进去100个数
            conn.rpush(key, *serialized_list)
            #Set an expiry flag to this key
            conn.expire(key, settings.REDIS_KEY_EXPIRE_TIME)







