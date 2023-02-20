""" Employee module"""
from __future__ import annotations
from pattern.observer import AbsObserver
import abc


# The Subject class
class Subject(abc.ABC):
    def __init__(self):
        self._observers = []

    @property
    def observer(self):
        return self._observers

    @observer.setter  # attach function
    def observer(self, observer):
        if not isinstance(observer, AbsObserver):
            raise TypeError("Observer must be a subclass of AbsObserver.")
        if observer not in self._observers:
            self._observers.append(observer)

    @observer.deleter  # detach function
    def observer(self, observer):
        if not isinstance(observer, AbsObserver):
            raise TypeError("Observer must be a subclass of AbsObserver.")
        try:
            self._observers.remove(observer)
        except ValueError:
            raise ValueError("Observer is not attached to this subject.")

    def set_observer(self, observer):
        if not isinstance(observer, AbsObserver):
            raise TypeError("Observer must be a subclass of AbsObserver.")
        self._observers = [observer]

    # def attach(self, observer):
    #     if observer not in self._observers:
    #         self._observers.append(observer)

    # def detach(self, observer):
    #     try:
    #         self._observers.remove(observer)
    #     except ValueError:
    #         pass

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def accept(self, visitor: Visitor, strategy: Strategy) -> None:
        visitor.visit(self, strategy)

    def _calculate_salary(self) -> float:
        pass


# The Employee class
class Employee(Subject):
    def __init__(self, name, salary=None):
        super().__init__()
        self._name = name
        self._salary = salary

    @property
    def name(self):
        return self._name

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, new_salary):
        self._salary = new_salary
        self.notify()

    def _calculate_salary(self) -> float:
        pass
