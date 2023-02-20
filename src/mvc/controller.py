class UserController:
    def __init__(self, context):
        self._context = context

    def handle_request(self, service_name, *args, **kwargs):
        service = self._context.get_dependency_container().get_service(service_name)
        result = service.perform_operation(*args, **kwargs)
        # Utiliser les données produites par les services pour produire une réponse à une requête utilisateur
        return result
