""" App module"""

import os
import yaml
import json

from pattern.visitor import PayrollVisitor, TaxAuthorityVisitor
from pattern.strategy import ProgressiveTaxStrategy, FlatTaxStrategy
from pattern.observer import Payroll, TaxAuthority
from pattern.factory import ObjectFactory
from employees import FullTimeEmployee


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
    config = config_to_json("config.yml")
    employee = FullTimeEmployee("John Doe")

    # Create Payroll and Tax Authority with the tax strategy observers and associate them with their respective visitors
    payroll = Payroll()
    payroll.visitor = PayrollVisitor()
    tax_authority = TaxAuthority()
    tax_authority.visitor = TaxAuthorityVisitor()
    tax_authority.strategy = FlatTaxStrategy()
    # Attach the observers to the employee
    employee.observer = payroll
    employee.observer = tax_authority
    print(employee.__dict__)
    for op in employee.__dict__.get("_observers"):
        print(op.__dict__)

    # Resultat
    print(employee.salary)
    # Notify the observers that the salary has changed
    employee.salary = 6000
    print(employee.salary)

    # Set the tax strategy for the employee
    employee.tax_strategy = FlatTaxStrategy()

    # Notify the observers that the salary has changed
    employee.salary = 600
    print(employee.salary)


def main3():
    class_map = {
        "FullTimeEmployee": FullTimeEmployee,
        "Payroll": Payroll,
        "TaxAuthority": TaxAuthority,
        "PayrollVisitor": PayrollVisitor,
        "TaxAuthorityVisitor": TaxAuthorityVisitor,
        "FlatTaxStrategy": FlatTaxStrategy,
    }

    print("____Start Objet Creation _____")
    config = config_to_json("config.yml")
    employee = ObjectFactory(config.get("employee"), class_map).get_object()
    print("____End Objet Creation ______\n")

    employee.salary = 6000
    print(employee.salary)


if __name__ == "__main__":
    # main()
    main3()
