"""This module provides an ObjectFactory class for creating objects based on a configuration file.

Classes:
- ObjectFactory: A factory class for creating objects based on a configuration file.

"""


class ObjectFactory:
    """Factory class to create objects based on configuration dictionary.

    This class provides a method for creating objects based on configuration
    dictionaries. It uses a class map to map class names to class objects.

    Attributes:
        conf (dict): A dictionary representing the configuration of the object to create.
        class_map (dict): A dictionary mapping class names to class objects.

    Methods:
        get_object: Create an object based on the configuration passed to the constructor.
        create_object: Create an object based on a configuration dictionary.

    Raises:
        ValueError: If the class type in the configuration dictionary is not found in the class map.

    Example:
        To create an object using the `ObjectFactory` class:

        >>> conf = {'class': 'MyClass', 'params': {'foo': 'bar'}}
        >>> class_map = {'MyClass': MyClass}
        >>> factory = ObjectFactory(conf, class_map)
        >>> obj = factory.get_object()
    """

    def __init__(self, conf: dict, class_map: dict):
        """
        Initialise une instance de ObjectFactory avec un dictionnaire de configuration
        et un mapping de classes.

        Args:
        - conf (dict): Un dictionnaire de configuration contenant des informations sur
                        les objets à créer.
        - class_map (dict): Un dictionnaire de correspondance de types de classe,
                            qui associe les noms des types de classe aux classes Python.

        Returns:
        - None
        """
        self.class_map = class_map
        self.conf = conf

    def get_object(self):
        """
        Crée un objet à partir de la configuration stockée dans l'instance.

        Args:
        - None

        Returns:
        - obj : L'objet créé à partir de la configuration stockée dans l'instance.
        """
        return self.create_object(self.conf)

    def create_object(self, conf: dict):
        """
        Crée un objet à partir d'un dictionnaire de configuration.

        Args:
        - conf (dict): Un dictionnaire de configuration contenant des
                        informations sur l'objet à créer.

        Returns:
        - obj : L'objet créé à partir du dictionnaire de configuration.
        """
        class_type = conf.get("class")
        class_name = self.class_map.get(class_type)
        if class_name is None:
            raise ValueError(f"Class type {class_type} not found in class map")
        obj = class_name(**conf.get("params", {}))
        print(f"{obj.__class__.__name__}()")
        for key, value in conf.items():
            if key in ["class", "params"]:
                continue
            if isinstance(value, list):
                for item in value:
                    child_obj = self.create_object(item)
                    setattr(obj, key, child_obj)
                    print(
                        f"{obj.__class__.__name__}.{key} = {child_obj.__class__.__name__}"
                    )
            else:
                child_obj = self.create_object(value)
                setattr(obj, key, child_obj)
                print(
                    f"{obj.__class__.__name__}.{key} = {child_obj.__class__.__name__}"
                )
        return obj
