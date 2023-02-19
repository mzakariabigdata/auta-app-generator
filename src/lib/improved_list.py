import pprint

class ImprovedList(list):
    """Dynamic Class as dict"""

    @property
    def inspect(self):
        """display list with inspect for each element"""
        if not self:
            print([])
        else:
            print(f"{self.__class__.__name__}({self[0].__class__.__name__}) data:")
            for value in self:
                method_inspect = getattr(value, "inspect", None)
                if callable(method_inspect):
                    value.inspect()
                else:
                    pertty_peint = pprint.PrettyPrinter(indent=3)
                    pertty_peint.pprint(value)

    def first(self, count=1):
        """return fist count elements"""
        data = self[:count]
        data_size = len(data)
        if data_size > 1:
            return self.__class__(data)
        if data_size == 1:
            return data[0]
        return None

    def last(self, count=1):
        """return last count elements"""
        data = self[-count:]
        data_size = len(data)
        if data_size > 1:
            return self.__class__(data)
        if data_size == 1:
            return data[0]
        return None

    def map(self, called):
        """advance map for call method or attribute"""
        if called.startswith(":"):
            print(called[1:])
            return self.__class__(map(lambda obj: getattr(obj, called[1:])(), self))
        return self.__class__(map(lambda obj: getattr(obj, called), self))
