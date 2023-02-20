""" App module"""

import os
import yaml
import json

from pattern.visitor import PayrollVisitor, TaxAuthorityVisitor
from pattern.strategy import ProgressiveTaxStrategy, FlatTaxStrategy
from pattern.observer import Payroll, TaxAuthority
from pattern.factory import ObjectFactory
from employees import FullTimeEmployee
from mvc import UserService, Service, AnotherService, DependencyContainer
from lib import OrmCollection, ObjDict, ImprovedList


def absolute_path(file):
    """Get absolute path"""
    script_dir = os.path.dirname(__file__)
    return os.path.join(script_dir, file)


def config_to_json(file) -> dict:
    """Convert Configfile to Json"""
    with open(absolute_path(file), "r", encoding="utf-8") as tmpf:
        config_loaded = yaml.load(tmpf, Loader=yaml.FullLoader)
    return config_loaded


def main():
    class_map_employee = {
        "FullTimeEmployee": FullTimeEmployee,
        "Payroll": Payroll,
        "TaxAuthority": TaxAuthority,
        "PayrollVisitor": PayrollVisitor,
        "TaxAuthorityVisitor": TaxAuthorityVisitor,
        "FlatTaxStrategy": FlatTaxStrategy,
    }

    print("____Start Objet Creation _____")
    config = config_to_json("config_employee.yml")
    employee = ObjectFactory(config.get("employee"), class_map_employee).get_object()
    print("____End Objet Creation ______\n")

    employee.salary = 6000
    print(employee.salary)

    # result1 = user_controller.handle_request('ObjectFactory', class_map_services)
    # result1 = user_controller.handle_request('ObjectFactory', class_map_employee)


def main2():
    class_map_services = {
        "DependencyContainer": DependencyContainer,
        "UserService": UserService,
        "Service": Service,
        "AnotherService": AnotherService,
    }
    print("____Start Objet Creation _____")
    config = config_to_json("config_services.yml")
    dependency_container = ObjectFactory(
        config.get("dependency_container"), class_map_services
    ).get_object()
    print(dependency_container.__dict__)
    print("____End Objet Creation ______\n")


def main3():
    my_orm_collection = OrmCollection(
        [
            ObjDict({"name": "Alice", "age": 25, "gender": "female"}),
            ObjDict({"name": "Bob", "age": 40, "gender": "male"}),
            ObjDict({"name": "Charlie", "age": 30, "gender": "male"}),
            ObjDict({"name": "Dave", "age": 30, "gender": "male"}),
        ]
    )

    results = my_orm_collection.where(age__gt=25, name__contains="v")
    print(results)
    results2 = my_orm_collection.where((("age", "lte", 30),) | (("name", "startswith", "A"),))
    print(results2)


if __name__ == "__main__":
    # main()
    # main2()
    main3()
