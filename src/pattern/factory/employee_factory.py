from typing import List, Union


class ObjectFactory:
    def __init__(self, conf: dict, class_map: dict):
        self.class_map = class_map
        self.conf = conf

    def get_object(self):
        return self.create_object(self.conf)

    def create_object(self, conf: dict):
        class_type = conf.get("class")
        class_name = self.class_map.get(class_type)
        if class_name is None:
            raise ValueError(f"Class type {class_type} not found in class map")
        obj = class_name(**conf.get("params", {}))
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
