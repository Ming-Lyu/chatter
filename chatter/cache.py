import aioredis
from channels.db import database_sync_to_async
from channels_redis.core import ConnectionPool
from django.conf import settings
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logging.getLogger(__name__)

class ChatCache:
    '''Make use of default server, differenciate using prefix
    '''
    prefix = 'chat'
    hosts = {'address': settings.CHANNEL_LAYERS['default']['CONFIG']['hosts'][0]} 

    def __init__(self):
        # only one host used here
        self.pool = ConnectionPool(self.hosts)
        self.flag = 0 # signal for long run task

    def remove_flag(self):
        # bad name
        self.flag^=1
    
    async def update_cache(self, users_id:list=None):
        ''' Updateing Cached database rows, coordination needed in cs.
        '''
        if not self.flag:
            async with self.connection() as conn:
                await conn.delete(f'{self.prefix}')
                await conn.sadd(f'{self.prefix}', *users_id)
                logging.info(f'Updated cache(users data){users_id[:10]}... to redis')

    async def check_status(self, user_id=None, current_role=None):
        '''return user ids that is online(all users) :(
        '''
        async with self.connection() as conn:
            # chat_list = await conn.smembers(f'{self.prefix}:{user_id}:{current_role}')
            users = await conn.smembers(f'{self.prefix}', encoding='utf-8')
            # res = set(chat_list) & set(users)
            # logging.info(f'Online users {users}')
            return users

    async def sismember(self, key, member):
        async with self.connection() as conn:
            await conn.sismember(key, member)

    def connection(self):
        return self.ConnectionContextManager(self.pool)

    async def sadd(self, *values, user_id=None):
        '''Cache user list
        '''
        async with self.connection() as conn:
            if user_id:
                await conn.sadd(f'{self.prefix}:{user_id}', *values)
            else:
                await conn.sadd(f'{self.prefix}:', *values)

    async def delete(self, user_id=None):
        '''Reset chat list
        '''
        async with self.connection() as conn:
            await conn.delete(f'{self.prefix}:{user_id}')

    async def smembers(self, user_id=None):
        '''Get all members list
           if user passed, -> chatlist(not supported)
        '''
        async with self.connection() as conn:
            if user_id:
                await conn.smembers(f'{self.prefix}:{user_id}')
            else:
                await conn.smembers(f'{self.prefix}:')

    async def srem(self, member):
        '''Remove soecific member
        '''
        async with self.connection() as conn:
            await conn.srem(f'{self.prefix}:', member)

    class ConnectionContextManager:
        """Async context manager for connection
        """
        def __init__(self, pool):
            self.pool = pool

        async def __aenter__(self):
            self.conn = await self.pool.pop()
            return self.conn

        async def __aexit__(self, exc_type, exc, tb):
            if exc:
                self.pool.conn_error(self.conn)
            else:
                self.pool.push(self.conn)
            self.conn = None
