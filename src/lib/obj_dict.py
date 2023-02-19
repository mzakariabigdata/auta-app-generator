import pprint
from src.lib.orm_collection import OrmCollection

# class ObjDictException(AttributeError):
#     """Associated objdixt Exception"""


class ObjDict(dict):
    """Dynamic Class as dict"""

    def __getattr__(self, name):
        if name in self:
            return self._clean_item(self[name])
        raise KeyError("no such attribute: " + name)

    def __setattr__(self, name, value):
        self[name] = self._clean_item(value)

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise KeyError("No such attribute: " + name)

    @property
    def inspect(self):
        """Return a pretty formatted informatopn of object"""
        pretty_print = pprint.PrettyPrinter(indent=4)
        pretty_print.pprint(self)

    def select(self, wanted_keys):
        """Filter dict by returning only some keys"""
        return self.__class__(
            {k: v for (k, v) in self.items() if k in set(wanted_keys)}
        )

    @staticmethod
    def _clean_item(item):
        """Improve type of object"""
        if isinstance(item, dict):
            return ObjDict(item)
        if isinstance(item, list):
            return OrmCollection(item)
        return item
