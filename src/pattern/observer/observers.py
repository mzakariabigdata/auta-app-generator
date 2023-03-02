""" Observer module"""

import abc


class AbsObserver(abc.ABC):
    """
    Abstract base class for Observer. Defines common interface for concrete observers.

    Attributes:
    _visitor (Visitor): Concrete visitor to be used by the observer.
    _strategy (Strategy): Concrete strategy to be used by the observer.
    """

    def __init__(self):
        self._visitor = None
        self._strategy = None

    @property
    def visitor(self):
        """
        Getter method for _visitor attribute.

        Returns:
        Visitor: Current visitor object.
        """
        return self._visitor

    @property
    def strategy(self):
        """
        Getter method for _strategy attribute.

        Returns:
        Strategy: Current strategy object.
        """
        return self._strategy

    @visitor.setter
    def visitor(self, value):
        """
        Setter method for _visitor attribute.

        Args:
        value (Visitor): Visitor object to be set.
        """
        self._visitor = value

    @strategy.setter
    def strategy(self, value):
        """
        Setter method for _strategy attribute.

        Args:
        value (Strategy): Strategy object to be set.
        """
        self._strategy = value

    @abc.abstractmethod
    def update(self, subject):
        """
        Update method to be implemented by concrete observer.

        Args:
        subject (Subject): The subject object to be observed.
        """


class Payroll(AbsObserver):
    """The Observer use the visitor to execute the strategy
    Concrete observer for payroll updates.

    Attributes:
    Inherits from AbsObserver.
    """

    def update(self, subject):
        """
        Implementation of update method for Payroll.

        Args:
        subject (Subject): The subject object to be observed.
        """
        # self._visitor.visit(subject) # also work
        subject.accept(self._visitor, self._strategy)


class TaxAuthority(AbsObserver):
    """
    Concrete observer for tax authority updates.

    Attributes:
    Inherits from AbsObserver.
    """

    def update(self, subject):
        """
        Implementation of update method for TaxAuthority.

        Args:
        subject (Subject): The subject object to be observed.
        """
        # self._visitor.visit(subject) # also work
        subject.accept(self._visitor, self._strategy)
