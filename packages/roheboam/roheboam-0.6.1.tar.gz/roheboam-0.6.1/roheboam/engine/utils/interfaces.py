from abc import ABC, abstractmethod


class MapDictionaryToMethodArguments(ABC):
    @abstractmethod
    def to_call_kwargs(self):
        return


class TransformToCallKeywordArguments(ABC):
    @abstractmethod
    def transform_to_kwargs(self):
        return


class MissingMethodArgumentException(Exception):
    pass


lookup = {"MapDictionaryToMethodArguments": MapDictionaryToMethodArguments, "MissingMethodArgumentException": MissingMethodArgumentException}
