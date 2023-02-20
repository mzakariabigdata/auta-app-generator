""" Observer module"""

import abc


class AbsObserver(abc.ABC):
    def __init__(self):
        self._visitor = None
        self._strategy = None

    @property
    def visitor(self):
        return self._visitor

    @property
    def strategy(self):
        return self._strategy

    @visitor.setter
    def visitor(self, value):
        self._visitor = value

    @strategy.setter
    def strategy(self, value):
        self._strategy = value

    @abc.abstractmethod
    def update(self, subject):
        pass


class Payroll(AbsObserver):
    """The Observer use the visitor to execute the strategy"""

    def __init__(self):
        super().__init__()

    def update(self, subject):
        # self._visitor.visit(subject) # also work
        subject.accept(self._visitor, self._strategy)


class TaxAuthority(AbsObserver):
    def __init__(self):
        super().__init__()

    def update(self, subject):
        # self._visitor.visit(subject) # also work
        subject.accept(self._visitor, self._strategy)
