import re
from typing import Any
from src.lib.improved_list import ImprovedList
from src.lib.exception import BaseMultipleFound, BaseNotFound
from collections import OrderedDict


class Filter:
    op_funcs = {
        "lt": lambda x, y: x < y
        if type(x) == type(y)
        else Filter.raise_type_error("<", x, y),
        "gt": lambda x, y: x > y
        if type(x) == type(y)
        else Filter.raise_type_error(">", x, y),
        "endswith": lambda x, y: x.endswith(y)
        if isinstance(x, str) and isinstance(y, str)
        else Filter.raise_type_error("endswith", x, y),
        "startswith": lambda x, y: x.startswith(y)
        if isinstance(x, str) and isinstance(y, str)
        else Filter.raise_type_error("startswith", x, y),
        "in": lambda x, y: x in y
        if type(y) in (list, set)
        else Filter.raise_type_error("in", x, y),
        "contains": lambda x, y: y in x
        if isinstance(x, str) and isinstance(y, str)
        else Filter.raise_type_error("contains", x, y),
        "nin": lambda x, y: x not in y
        if type(y) in (list, set)
        else Filter.raise_type_error("nin", x, y),
        "not": lambda x, y: x != y
        if type(x) == type(y)
        else Filter.raise_type_error("!=", x, y),
        "lte": lambda x, y: x <= y
        if type(x) == type(y)
        else Filter.raise_type_error("<=", x, y),
        "gte": lambda x, y: x >= y
        if type(x) == type(y)
        else Filter.raise_type_error(">=", x, y),
    }

    def __init__(self, attribute, operator, value):
        self.attribute = attribute
        self.operator = operator
        self.value = value

    def evaluate(self, obj):
        attr_value = getattr(obj, self.attribute)
        # print(attr_value, self.attribute, self.value)
        if self.operator is not None:
            if self.operator in self.op_funcs:
                return self.op_funcs[self.operator](attr_value, self.value)
            else:
                raise ValueError(f"Invalid operator {self.operator}")
        elif self.contains_regex(self.value):
            return re.match(self.value, attr_value)
        else:
            return attr_value == self.value
    
    def contains_regex(self, s):
        """
        Checks whether a string contains a regular expression.

        Args:
            s (str): The string to check.

        Returns:
            True if the string contains a regular expression, False otherwise.
        """
        try:
            re.compile(s)
        except (re.error, TypeError):
            return False
        return True

    @staticmethod
    def raise_type_error(op: str, x: Any, y: Any) -> None:
        """
        Raises a TypeError indicating that the given operands are not supported for a given operator.

        Args:
            op (str): The operator that caused the TypeError.
            x (Any): The first operand of the operator.
            y (Any): The second operand of the operator.

        Raises:
            TypeError: If the given operands are not supported for the given operator.
        """
        raise TypeError(
            f"unsupported operand type(s) for {op}: '{type(x).__name__}' and '{type(y).__name__}'"
        )


class Query:
    """
    query1 = Query([
    Filter("age", "gt", 25),
    Filter("country", None, "France")
        ])

    query2 = Query([
        Filter("name__startswith", None, "J"),
        Filter("country", None, "Spain")
    ])

    # AND
    query_and = query1 & query2
    # équivaut à Query([
    #    Filter("age", "gt", 25),
    #    Filter("country", None, "France"),
    #    Filter("name__startswith", None, "J"),
    #    Filter("country", None, "Spain")
    # ])

    # OR
    query_or = query1 | query2
    # équivaut à Query([
    #    Query([
    #        Filter("age", "gt", 25),
    #        Filter("country", None, "France")
    #    ]),
    #    Query([
    #        Filter("name__startswith", None, "J"),
    #        Filter("country", None, "Spain")
    #    ])
    # ])
    """

    def __init__(self, filters):
        self.filters = filters

    def __and__(self, other):
        return Query(self.filters + other.filters)

    def __or__(self, other):
        return Query([self, other])

    def evaluate(self, obj):
        return all(filter.evaluate(obj) for filter in self.filters)


class OrmCollection(ImprovedList):
    """
    A list-like collection class that extends ImprovedList and that implements an ORM overlay (wrapper) for a list of objects,
    providing an interface and additional methods for querying and manipulating objects in the list.
    """

    def where(self, *args, **kwargs) -> "OrmCollection":
        """
        Filters the collection to only include objects that match the provided criteria.

        Args:
            *args (Query): Query objects that are combined using the OR operator.
            **kwargs (dict): Key-value pairs of field names and values to filter by.
                Valid operators include "lt", "gt", "lte", "gte", "endswith", "startswith", "in", "nin", "contains".
                If an invalid operator is used, a ValueError is raised.

        Returns:
            OrmCollection: A new OrmCollection containing only objects where at least one of the given attributes matches.

        Raises:
            ValueError: If an invalid operator is used.
        """

        results = self.__class__()
        filters = []
        for query in args:
            for filter_ in query.filters:
                filters.append(filter_)

        for key, value in kwargs.items():
            if "__" in key:
                attribute, operator = key.split("__")
                if operator not in Filter.op_funcs:
                    raise ValueError(f"Invalid operator {operator}")
                filters.append(Filter(attribute, operator, value))
            else:
                filters.append(Filter(key, None, value))

        print(len(filters))
        for elm in self:
            matches = True
            for filter_ in filters:
                matches = matches and filter_.evaluate(elm)
                if not matches:
                    break
            if matches:
                results.append(elm)

        return results

    def find_by(self, **kwargs) -> object:
        """
        Finds a single object in the collection that matches the provided criteria. Raises an exception if no or more than
        one object is found.

        Args:
            **kwargs: Key-value (Dictionary) of field names and values to filter by.

        Returns:
            The first object in the OrmCollection where all given attributes match.

        Raises:
            BaseNotFound: If no objects are found that match the given attributes.
            BaseMultipleFound: If more than one object is found that matches the given attributes.
        """
        matching_objs = self.where(**kwargs)
        if len(matching_objs) == 0:
            raise BaseNotFound(f"No {self.__class__.__name__} found for {kwargs}")
        if len(matching_objs) > 1:
            raise BaseMultipleFound(
                f"More than one {self.__class__.__name__} found for {kwargs}"
            )
        return matching_objs.first()

    def order_by(self, key=None, reverse=False):
        """
        Sort the objects in the collection based on a field or a custom function.

        Args:
            key (str or function, optional): Field name or function to sort by. Defaults to None.
            reverse (bool, optional): True to sort in descending order, False to sort in ascending order. Defaults to False.

        Returns:
            A new OrmCollection containing the sorted objects.

        Raises:
            ValueError: If key is None and not all elements in the list are integers or floats.
            TypeError: If key is not a valid attribute name or function.
        """
        if not key:
            if all(isinstance(item, (int, float)) for item in self):
                return self.__class__(sorted(self))
            raise ValueError("All elements in the list must be integers or floats.")
        if isinstance(key, str):
            return self.__class__(
                sorted(self, key=lambda x: getattr(x, key), reverse=reverse)
            )
        elif callable(key):
            return self.__class__(sorted(self, key=key, reverse=reverse))
        else:
            raise TypeError("key must be a string attribute name or a function")

    def group_by(self, key_func):
        """
        Group the objects in the collection based on a given function.

        Args:
            key_func (function): A function that takes an object as input and returns the group key.

        Returns:
            A dictionary where the keys are the return values of the key function and
            the values are OrmCollections containing the corresponding objects.

        Raises:
            N/A
        """
        groups = {}
        for obj in self:
            key = key_func(obj)
            if key not in groups:
                groups[key] = OrmCollection()
            groups[key].append(obj)
        return groups

    def limit(self, count):
        """
        Return a new OrmCollection with the first n objects in the collection.

        Args:
            count (int): The number of objects to include in the new collection.

        Returns:
            A new OrmCollection containing the first n objects in the collection.

        Raises:
            N/A
        """
        return self.__class__(self[:count])

    def offset(self, count):
        """
        Return a new OrmCollection with the objects after the first n objects in the collection.

        Args:
            count (int): The number of objects to skip.

        Returns:
            A new OrmCollection containing the objects after the first n objects in the collection.

        Raises:
            N/A
        """
        return self.__class__(self[count:])

    def all(self):
        """
        Return a new OrmCollection containing all objects in the collection.

        Args:
            N/A

        Returns:
            A new OrmCollection containing all objects in the collection.

        Raises:
            N/A
        """
        return self.__class__(self)

    def _check_simple_type(self, lst):
        """
        Check if all items in the given list are of simple types.

        Args:
            lst (list): The list to check.

        Returns:
            bool: True if all items in the list are of simple types (int, float, or str), False otherwise.

        Raises:
            N/A
        """
        return all(isinstance(item, (int, float, str)) for item in lst)

    def distinct(self, *args):
        """
        Return a new OrmCollection containing only the unique objects in the collection
        based on one or more attributes.

        Args:
            *args (str): One or more attribute names to use for finding unique objects.

        Returns:
            A new OrmCollection containing only the unique objects in the collection.

        Raises:
            ValueError: If no arguments are provided or if at least one argument is not a field.
            AttributeError: If at least one argument is not an attribute of the objects in the collection.
        """

        # If no args are provided, return a new collection with unique elements
        if not args and self._check_simple_type(self):
            return self.__class__(list(OrderedDict.fromkeys(self)))
        elif not args and not self._check_simple_type(self):
            raise ValueError("At least one field must be provided")

        for field in args:
            if not hasattr(self[0], field):
                raise AttributeError(
                    f"Le champ '{field}' n'existe pas dans la classe {self[0].__class__.__name__}."
                )

        distinct_values = []
        seen = set()
        for elm in self:
            # distinct_values.append(tuple(getattr(elm, field) for field in args))
            values = tuple(getattr(elm, field) for field in args)
            if values not in seen:
                seen.add(values)
                distinct_values.append(elm)

        # return self.__class__(list(dict.fromkeys(distinct_values)))
        return self.__class__(distinct_values)

    def contains_regex(self, s):
        """
        Checks whether a string contains a regular expression.

        Args:
            s (str): The string to check.

        Returns:
            True if the string contains a regular expression, False otherwise.
        """
        try:
            re.compile(s)
        except (re.error, TypeError):
            return False
        return True
