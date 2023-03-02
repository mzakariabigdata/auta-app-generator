""" App module"""

import os
import yaml
import json
from datetime import date

from pattern.visitor import PayrollVisitor, TaxAuthorityVisitor
from pattern.strategy import ProgressiveTaxStrategy, FlatTaxStrategy
from pattern.observer import Payroll, TaxAuthority
from pattern.factory import ObjectFactory
from employees import FullTimeEmployee
from mvc import UserService, Service, AnotherService, DependencyContainer
from lib import OrmCollection, ObjDict, ImprovedList, Query, Filter


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
    employee.salary = 50
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
    # from datetime import datetime
    # from typing import List

    # class MyClass:
    #     def __init__(self, name: str, date: str):
    #         self.name = name
    #         self.date = datetime.strptime(date, "%Y-%m-%d")

    # def compare_by_date(a: MyClass, b: MyClass) -> int:
    #     if a.date < b.date:
    #         return -1
    #     elif a.date > b.date:
    #         return 1
    #     else:
    #         return 0

    # # Créer une liste d'objets MyClass non triée
    # objects = ImprovedList(
    #     [
    #         MyClass("Obj1", "2022-01-05"),
    #         MyClass("Obj2", "2022-02-03"),
    #         MyClass("Obj2", "2022-02-03"),
    #         MyClass("Obj2", "2022-02-03"),
    #         MyClass("Obj3", "2021-12-25"),
    #         MyClass("Obj4", "2022-01-20"),
    #     ]
    # )

    # # Trier la liste d'objets MyClass par date en utilisant la fonction compare_by_date
    # sorted_objects = objects.map(
    #     called=".date",
    #     filter_func=None,
    #     max_elements=None,
    #     reverse_order=False,
    #     sort_func=compare_by_date,
    #     return_type="ImprovedList",
    # )

    # # Afficher le résultat trié
    # for obj in sorted_objects:
    #     print(f"{obj.name} - {obj.date}")

    my_list = ImprovedList([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    result = my_list.map(lambda x: x**2, max_elements=3, reverse_order=False)
    print(result)


if __name__ == "__main__":
    main()
    # main2()
    # main3()
