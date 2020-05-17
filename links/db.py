from redis import Redis

DEFAULT_URL = 'redis://@localhost:6379/0'


class DomainsRepository:
    def init_app(self, store_name: str = 'domains', url: str = DEFAULT_URL):
        self.store_name = store_name
        self.redis: Redis = Redis.from_url(url, decode_responses=True)

    def add(self, ts: int, domains: set) -> None:
        key_part = ':'.join(domains)
        key = f'{ts}:{key_part}'
        self.redis.zadd(self.store_name, {key: ts})

    def get_range(self, from_: int, to: int) -> list:
        keys = (str(k)
                for k in self.redis.zrangebyscore(self.store_name, from_, to))
        result = set()
        for key in keys:
            domains = key.split(':')[1:]
            result.update(domains)
        return list(result)
