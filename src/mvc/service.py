"""Module services
"""


class UserService:
    def perform_operation(self, *args, **kwargs):
        return f"Service performed an operation for {self} {kwargs.get('a') + 10} "


class Service:
    def __init__(
        self,
    ) -> None:
        pass

    def perform_operation(self, *args, **kwargs):
        # Effectuer une autre opération qui nécessite des dépendances
        return f"Service performed an operation for {self} {kwargs.get('a') + 10} "


class AnotherService:
    def perform_operation(self, *args, **kwargs):
        # Effectuer une autre opération qui nécessite des dépendances
        return (
            f"AnotherService performed an operation for {self} {kwargs.get('a') + 150}"
        )
