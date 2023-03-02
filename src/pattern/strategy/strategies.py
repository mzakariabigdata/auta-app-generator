""" Strategy module"""

import abc


class AbsTaxStrategy(abc.ABC):
    """Abstract base class for implementing different tax strategies.

    Attributes:
    Inherits from abc.ABC.
    """

    def __init__(self) -> None:
        self.subject = None

    @abc.abstractmethod
    def execute(self, subject):
        """Abstract method that must be implemented in concrete strategy classes.

        Args:
        salary: float, the salary on which the tax will be applied.

        Returns:
        float, the amount of tax to be paid.
        """

    def set_subject(self, subject):
        """
        Sets the subject to visit.
        """
        self.subject = subject

    def get_subject(self):
        """
        Gets the current subject.
        """
        return self.subject


class ProgressiveTaxStrategy(AbsTaxStrategy):
    """A concrete tax strategy class that implements a progressive tax system.

    Attributes:
    Inherits from AbsTaxStrategy.
    """

    def execute(self, subject):
        """Applies a progressive tax system based on the salary.

        Args:
        salary: float, the salary on which the tax will be applied.

        Returns:
        float, the amount of tax to be paid.
        """
        if subject.salary <= 3000:
            return 0.0
        if subject.salary <= 6000:
            return 0.1 * (subject.salary - 3000)
        return 0.2 * (subject.salary - 6000) + 900


class FlatTaxStrategy(AbsTaxStrategy):
    """A concrete tax strategy class that implements a flat tax system.

    Attributes:
    Inherits from AbsTaxStrategy.
    """

    def execute(self, subject):
        """Applies a flat tax rate on the salary.

        Args:
        salary: float, the salary on which the tax will be applied.

        Returns:
        float, the amount of tax to be paid.
        """
        result = 0.15 * subject.salary
        # subject.salary = result # RecursionError: maximum recursion depth exceeded
        return result
