"""Module services
"""


class UserService:
    """
    A class that provides user-related services.

    Methods:
    perform_operation: Performs an operation for a given user.
    """

    def perform_operation(self, **kwargs):
        """
        Performs an operation for a given user.

        Args:
        *args: A tuple of positional arguments.
        **kwargs: A dictionary of keyword arguments.

        Returns:
        A string containing the result of the operation.
        """
        return f"Service performed an operation for {self} {kwargs.get('a') + 10} "


class Service:
    """
    A class that provides a generic service.

    Methods:
    perform_operation: Performs a generic operation.
    """

    def __init__(
        self,
    ) -> None:
        pass

    def perform_operation(self, **kwargs):
        """
        Performs a generic operation.

        Args:
        *args: A tuple of positional arguments.
        **kwargs: A dictionary of keyword arguments.

        Returns:
        A string containing the result of the operation.
        """
        # Effectuer une autre opération qui nécessite des dépendances
        return f"Service performed an operation for {self} {kwargs.get('a') + 10} "


class AnotherService:
    """
    A class that provides another service.

    Methods:
    perform_operation: Performs an operation.
    """

    def perform_operation(self, **kwargs):
        """
        Performs an operation.

        Args:
        *args: A tuple of positional arguments.
        **kwargs: A dictionary of keyword arguments.

        Returns:
        A string containing the result of the operation.
        """
        # Effectuer une autre opération qui nécessite des dépendances
        return (
            f"AnotherService performed an operation for {self} {kwargs.get('a') + 150}"
        )
