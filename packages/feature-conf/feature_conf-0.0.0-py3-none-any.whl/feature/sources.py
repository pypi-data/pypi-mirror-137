import abc
import os
from typing import Iterable

import immutables


class Source(abc.ABC):
    @abc.abstractmethod
    def resolve(self, name: str) -> str | None:
        ...

    def resolve_many(
        self,
        prefix: str,
        names: Iterable[str],
    ) -> immutables.Map[str, str]:
        return immutables.Map(
            {
                name: value
                for name in names
                if (value := self.resolve(f"{prefix}_{name}")) is not None
            }
        )


class EnvVars(Source):
    def resolve(cls, name: str) -> str | None:
        try:
            return os.environ[name]
        except KeyError:
            return None
