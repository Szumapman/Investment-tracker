import abc


class AbstractCache(abc.ABC):
    @abc.abstractmethod
    async def get_from_cache(self, key: str) -> bytes | None:
        pass

    @abc.abstractmethod
    async def set_to_cache(self, key: str, value: object, expire: int) -> None:
        pass

    @abc.abstractmethod
    async def delete_from_cache(self, key: str) -> None:
        pass
