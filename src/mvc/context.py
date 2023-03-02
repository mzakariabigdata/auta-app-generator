"""Module context with DependencyContainer"""


class DependencyContainer:
    """
    A singleton class for managing dependencies.

    Attributes:
    _instance: The singleton instance of the DependencyContainer class.
    _services: A dictionary of registered services.
    _context: The current context of the DependencyContainer.
    """

    _instance = None

    def __new__(cls):
        """
        Create a new instance of the DependencyContainer class.

        Returns:
        The singleton instance of the DependencyContainer class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initialize the DependencyContainer object.

        Attributes:
        _services: An empty dictionary to hold the registered services.
        _context: None by default, this will be set when a Context object is created.
        """
        self._services = {}
        self._context = None

    @property
    def service(self):
        """
        Get the dictionary of registered services.

        Returns:
        A dictionary of registered services.
        """
        return self._services

    @service.setter
    def service(self, service):
        """
        Set a new service in the dictionary of registered services.

        Args:
        service: A new service to be registered.
        """
        # print(service.__class__.__name__, service)
        self._services[service.__class__.__name__] = service

    @service.deleter  # detach function
    def service(self, name):
        """
        Delete a service from the dictionary of registered services.

        Args:
        name: The name of the service to be deleted.
        """
        self._services.remove(name)

    def get_service(self, name):
        """
        Get a registered service from the dictionary.

        Args:
        name: The name of the service to be retrieved.

        Returns:
        The service object associated with the given name.
        """
        return self._services[name]

    def set_context(self, context):
        """
        Set the current context of the DependencyContainer.

        Args:
        context: The Context object to be set as the current context.
        """
        self._context = context

    def get_context(self):
        """
        Get the current context of the DependencyContainer.

        Returns:
        The current context of the DependencyContainer.
        """
        return self._context


class Context:
    """
    A singleton class representing the context of the application.

    Attributes:
    _instance: The singleton instance of the Context class.
    _dependency_container: The DependencyContainer object associated with the context.
    """

    _instance = None

    def __new__(cls):
        """
        Create a new instance of the Context class.

        Returns:
        The singleton instance of the Context class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dependency_container):
        """
        Initialize the Context object.

        Args:
        dependency_container: The DependencyContainer object associated with the context.
        """
        self._dependency_container = dependency_container
        self._dependency_container.set_context(self)

    def get_dependency_container(self):
        """
        Get the DependencyContainer object associated with the context.

        Returns:
        The DependencyContainer object associated with the context.
        """
        return self._dependency_container

    def __repr__(self):
        """
        Return a string representation of the Context object.

        Returns:
        A string representation of the Context object.
        """
        return f"Context(dependency_container={self._dependency_container!r})"
