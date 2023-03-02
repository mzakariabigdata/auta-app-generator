"""
Module contenant la classe UserController pour gérer les requêtes utilisateur.

Ce module définit la classe UserController qui permet de gérer les requêtes utilisateur
en récupérant le service correspondant depuis le conteneur de dépendances et en appelant
sa méthode perform_operation.

Classes:

UserController: une classe pour gérer les requêtes utilisateur.
"""


class UserController:
    """
    A class representing a controller for handling user requests.

    Args:
    context: A Context object representing the context in which the controller operates.

    Attributes:
    _context: A Context object representing the context in which the controller operates.
    """

    def __init__(self, context):
        """
        Constructs a new UserController object.

        Args:
        context: A Context object representing the context in which the controller operates.
        """
        self._context = context

    def handle_request(self, service_name, *args, **kwargs):
        """
        Handles a user request by retrieving the specified service from
          the dependency container and calling its perform_operation method.

        Args:
        service_name: A string representing the name of the service to be retrieved.
        *args: Any additional arguments to be passed to the service's perform_operation method.
        **kwargs: Any additional keyword arguments to be passed to the service's
                     perform_operation method.

        Returns:
        The result of the service's perform_operation method.
        """
        service = self._context.get_dependency_container().get_service(service_name)
        result = service.perform_operation(*args, **kwargs)
        # Utiliser les données produites par les services pour produire
        # une réponse à une requête utilisateur
        return result

    def get_context(self):
        """
        Returns the context object associated with this controller.

        Returns:
        A Context object representing the context in which this controller operates.
        """
        return self._context
