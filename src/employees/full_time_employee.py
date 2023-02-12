""" FullTimeEmployee module"""

from . import Employee


class FullTimeEmployee(Employee):
    def __init__(self, name: str):
        super().__init__(name)
        self._salary = self._calculate_salary()

    def _calculate_salary(self) -> float:
        return 120000.0
