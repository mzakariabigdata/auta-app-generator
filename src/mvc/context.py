"""Module context with DependencyContainer"""


class DependencyContainer:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._services = {}
        self._context = None

    @property
    def service(self):
        return self._services

    @service.setter
    def service(self, service):
        # print(service.__class__.__name__, service)
        self._services[service.__class__.__name__] = service

    @service.deleter  # detach function
    def service(self, name):
        self._services.remove(name)

    def get_service(self, name):
        return self._services[name]

    def set_context(self, context):
        self._context = context

    def get_context(self):
        return self._context


class Context:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dependency_container):
        self._dependency_container = dependency_container
        self._dependency_container.set_context(self)

    def get_dependency_container(self):
        return self._dependency_container

    def __repr__(self):
        return f"Context(dependency_container={self._dependency_container!r})"
