""" Strategy module"""

import abc


class AbsTaxStrategy(abc.ABC):
    def execute(self, salary):
        pass


class ProgressiveTaxStrategy(AbsTaxStrategy):
    def execute(self, subject):
        if subject._salary <= 3000:
            return 0.0
        elif subject._salary <= 6000:
            return 0.1 * (subject._salary - 3000)
        else:
            return 0.2 * (subject._salary - 6000) + 900


class FlatTaxStrategy(AbsTaxStrategy):
    def execute(self, subject):
        result = 0.15 * subject._salary
        subject._salary = result
        return result
