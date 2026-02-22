from abc import ABC, abstractmethod
from enum import Enum


class CombineMeta:
    def __prepare__(self, name, bases, **kwargs):
        namespace = {}
        for metaclass in self._get_most_derived_metaclasses(bases):
            ns = metaclass.__prepare__(name, bases, **kwargs)
            if type(ns) in (dict, type(namespace)):
                namespace.update(ns)
            else:
                if type(namespace) is not dict:
                    raise TypeError(
                        "metaclass conflict: " "multiple custom namespaces defined."
                    )
                ns.update(namespace)
                namespace = ns
        return namespace

    def __call__(self, name, bases, namespace, **kwargs):
        metaclasses = self._get_most_derived_metaclasses(bases)
        if len(metaclasses) > 1:
            merged_name = "__".join(meta.__name__ for meta in metaclasses)
            ns = self.__prepare__(merged_name, metaclasses)
            metaclass = self(merged_name, tuple(metaclasses), ns, **kwargs)
        else:
            (metaclass,) = metaclasses or (type,)
        return metaclass(name, bases, namespace, **kwargs)

    @staticmethod
    def _get_most_derived_metaclasses(bases):
        metaclasses = []
        for metaclass in map(type, bases):
            if metaclass is not type:
                metaclasses = [
                    other for other in metaclasses if not issubclass(metaclass, other)
                ]
                if not any(issubclass(other, metaclass) for other in metaclasses):
                    metaclasses.append(metaclass)
        return metaclasses


combine_meta = CombineMeta()


class EnumABC(ABC, Enum, metaclass=combine_meta):
    @classmethod
    @abstractmethod
    def fields(cls):
        pass

    @classmethod
    @abstractmethod
    def get_name(self):
        pass
