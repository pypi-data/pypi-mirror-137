__all__ = ['Config']

from typing import Any


class Config:
    def __getitem__(self, key: str) -> Any:
        return self._state[key]


    def __setitem__(self, key: str, value: Any):
        self._state[key] = value


    def __getattr__(self, attr: str) -> Any:
        return self.__dict__['_state'][attr]


    async def __aenter__(self):
        '''
        startup
        '''
        if self._fetch:
            await self.fetch()

        return self


    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        '''
        shutdown
        '''
        
        if exc_type and exc_value:
            raise exc_value

        if self._commit:
            await self.commit()

        return self
