from functools import cached_property
from pkgutil import resolve_name
from typing import Final
from typing import Generic
from typing import TypeVar

B = TypeVar("B")


class ClassReference(Generic[B]):
    def __init__(self, reference: str | type, bound: type[B]) -> None:
        self.reference: Final = reference
        self.bound: Final = bound

    @cached_property
    def resolved(self) -> type[B]:
        resolved = (
            resolve_name(self.reference)
            if isinstance(self.reference, str)
            else self.reference
        )
        assert isinstance(resolved, type)
        assert issubclass(resolved, self.bound)
        return resolved
