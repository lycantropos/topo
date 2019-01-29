from abc import (ABC,
                 abstractmethod)
from typing import Generic

from .hints import Domain


class Set(ABC, Generic[Domain]):
    @abstractmethod
    def __bool__(self) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __and__(self, other: 'Set') -> 'Set':
        pass

    @abstractmethod
    def __contains__(self, object_: Domain) -> bool:
        pass

    @abstractmethod
    def __or__(self, other: 'Set') -> 'Set':
        pass

    @abstractmethod
    def __sub__(self, other: 'Set') -> 'Set':
        pass

    def __eq__(self, other: 'Set') -> bool:
        return not (self - other) and not (other - self)

    def __rsub__(self, other: 'Set') -> 'Set':
        return NotImplemented

    def __xor__(self, other: 'Set') -> 'Set':
        return (self | other) - (self & other)
