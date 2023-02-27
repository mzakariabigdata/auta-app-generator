import pprint
from typing import List, Any, Union, Callable, Optional


class ImprovedList(list):
    """
    A dynamic list subclass that provides additional functionality.

    This class extends the built-in `list` class to provide additional methods
    for working with lists, including inspecting the elements of a list and
    performing advanced mapping operations.

    Attributes:
        None

    Methods:
        inspect: Display each element in the list with an inspect method.
        first: Return the first one or more elements of the list.
        last: Return the last one or more elements of the list.
        map: Apply a callable or attribute to each element of the list.

    Usage:
        lst = ImprovedList([1, 2, 3])
        lst.inspect()  # Prints the list with each element's inspect method.
        lst.first()    # Returns the first element of the list.
        lst.last(2)    # Returns the last two elements of the list.
        lst.map(str)    # Returns a new list with each element converted to a string.
    """

    @property
    def inspect(self) -> None:
        """Display a list with inspect for each element.

        If the ImprovedList is empty, an empty list is displayed.
        If not empty, the element type and the data are displayed.
        The inspect method is called if it exists for each element.
        Otherwise, the value is pretty-printed using pprint.

        Returns:
            None.
        """
        if not self:
            print([])
        else:
            element_type = self[0].__class__.__name__
            print(f"{self.__class__.__name__}({element_type}) data:")
            for value in self:
                method_inspect = getattr(value, "inspect", None)
                if callable(method_inspect):
                    value.inspect()
                else:
                    pertty_peint = pprint.PrettyPrinter(indent=3)
                    pertty_peint.pprint(value)

    def first(self, count: int = 1) -> Union[None, Any, "ImprovedList"]:
        """Return the first count elements of the ImprovedList.

        Args:
            count (int): The number of elements to return. Default is 1.

        Returns:
            If count > 1, an ImprovedList containing the first count elements.
            If count = 1, the first element.
            If the ImprovedList is empty or count = 0, None.
        """
        data = self[:count]
        data_size = len(data)
        if data_size > 1:
            return self.__class__(data)
        if data_size == 1:
            return data[0]
        return None

    def last(self, count: int = 1) -> Union[None, Any, "ImprovedList"]:
        """Return the last count elements of the ImprovedList.

        Args:
            count (int): The number of elements to return. Default is 1.

        Returns:
            If count > 1, an ImprovedList containing the last count elements.
            If count = 1, the last element.
            If the ImprovedList is empty or count = 0, None.
        """
        data = self[-count:]
        data_size = len(data)
        if data_size > 1:
            return self.__class__(data)
        if data_size == 1:
            return data[0]
        return None

    def filter(self, filter_func: Callable) -> "ImprovedList":
        """Return a new ImprovedList containing only the elements for which filter_func returns True."""
        return self.__class__(filter(filter_func, self))

    def map(
        self,
        called: Union[str, Callable],
        filter_func: Optional[Callable] = None,
        max_elements: Optional[int] = None,
        reverse_order: bool = False,
        sort_func: Optional[Callable] = None,
        return_type: str = "ImprovedList",
        *args,
        **kwargs,
    ) -> Union["ImprovedList", List]:
        """Apply a map function to the ImprovedList, optionally filtered by a condition.

        If the called argument is None, a ValueError is raised.
        If the called argument is callable, the function is applied to each element.
        If the called argument starts with ':', the method or attribute specified after ':'
        is called or accessed for each element.
        If the called argument starts with '.', the attribute specified after '.'
        is accessed for each element.

        If filter_func is not None, only elements that satisfy the condition are processed.

        Args:
            called (str or callable): The method or attribute name or the callable function to apply.
            filter_func (callable): A function that returns True for elements to be processed, False otherwise.
            max_elements (int, optional): The maximum number of elements to process. Defaults to None.
            reverse_order (bool): If True, the elements are processed in reverse order.
            return_type (str): The type of object to return. Defaults to "ImprovedList".
            *args: Additional arguments to be passed to the called function or method.
            **kwargs: Additional keyword arguments to be passed to the called function or method.


        Returns:
            An ImprovedList containing the results of applying the called function to each selected element.
        """

        if called is None:
            raise ValueError("called cannot be None")

        # Sélectionner les éléments dans l'ordre inversé si reverse_order est True.
        elements = self[:max_elements]
        if reverse_order:
            elements = reversed(elements)

        # Trier les éléments si sort_func est fourni.
        if sort_func is not None:
            elements.sort(key=sort_func)

        # Appliquer la fonction appelée à chaque élément.
        if callable(called):
            if filter_func is None:
                result = map(lambda x: called(x, *args, **kwargs), elements)
            else:
                result = map(
                    lambda x: called(x, *args, **kwargs),
                    filter(filter_func, elements),
                )

        # Appeler la méthode ou accéder à l'attribut pour chaque élément.
        elif isinstance(called, str):
            if called.startswith(":"):
                method_name = called[1:]

                def call_method(obj):
                    method = getattr(obj, method_name)
                    if not callable(method):
                        raise TypeError(f"{method_name} is not callable")
                    return method(*args, **kwargs)

                if filter_func is None:
                    result = map(call_method, elements)
                else:
                    result = map(call_method, filter(filter_func, elements))
            elif called.startswith("."):
                attr_name = called[1:]

                def get_attribute(obj):
                    try:
                        return getattr(obj, attr_name)
                    except AttributeError:
                        raise AttributeError(
                            f"{obj.__class__.__name__} object has no attribute '{attr_name}'"
                        )

                if filter_func is None:
                    result = map(get_attribute, elements)
                else:
                    result = map(get_attribute, filter(filter_func, elements))
            else:
                raise TypeError(
                    "called must be a string start with ':' for obj method or '.' obj attribute, or a callable"
                )
        else:
            # Si l'argument appelé n'est ni une chaîne de caractères ni un objet callable, on lève une erreur.
            raise TypeError(
                "called must be a string start with ':' for obj method or '.' obj attribute, or a callable"
            )
        # Convertir le résultat en ImprovedList ou en list en fonction de return_type.
        if return_type == "ImprovedList":
            return self.__class__(result)
        if return_type == "list":
            return list(result)
        raise ValueError("return_type must be 'ImprovedList' or 'list'")
