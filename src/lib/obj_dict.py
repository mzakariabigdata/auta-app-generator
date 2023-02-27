import pprint
from src.lib.orm_collection import OrmCollection

# class ObjDictException(AttributeError):
#     """Associated objdixt Exception"""


class ObjDict(dict):
    """Dynamic Class as dict"""

    def __getattr__(self, name: str):
        """Get attribute value"""
        try:
            return self._clean_item(self[name])
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    def __setattr__(self, name: str, value):
        """Set Any attribute value"""
        self[name] = self._clean_item(value)

    def __delattr__(self, name: str):
        """Delete attribute"""
        try:
            del self[name]
        except KeyError:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            )

    def to_dict(self) -> dict:
        """Return a dictionary representation of the object"""
        result = {}
        for key, value in self.items():
            if isinstance(value, ObjDict):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "ObjDict":
        """Create an object from a dictionary"""
        result = cls()
        for key, value in data.items():
            result[key] = cls._clean_item(value)
        return result

    def update(self, data: dict):
        """Update the object with a dictionary"""
        for key, value in data.items():
            self[key] = self._clean_item(value)

    def items(self):
        """Return the keys and values of the object as tuples"""
        return [(key, self._clean_item(value)) for key, value in super().items()]

    def copy(self) -> "ObjDict":
        """Return a deep copy of the object"""
        return self.__class__(self.to_dict())

    @property
    def inspect(self):
        """Return a pretty formatted information of object"""
        pprint.pprint(self, indent=4)

    def select(self, wanted_keys: list):
        """Filter dict by returning only some keys"""
        if not isinstance(wanted_keys, list):
            raise TypeError(
                f"Argument 'wanted_keys' should be a list, got '{type(wanted_keys).__name__}' instead."
            )
        selected_items = {}
        for key in wanted_keys:
            if not isinstance(key, str):
                raise TypeError(f"Element {key} in 'wanted_keys' list is not a string")
            try:
                selected_items[key] = self[key]
            except KeyError:
                raise KeyError(
                    f"'{self.__class__.__name__}' object has no attribute '{key}'"
                )
        return self.__class__(selected_items)

    @staticmethod
    def _clean_item(item):
        """Improve type of object"""
        if isinstance(item, dict):
            return ObjDict(item)
        if isinstance(item, list):
            return OrmCollection(item)
        return item
