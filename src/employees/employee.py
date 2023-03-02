""" Employee module"""
from __future__ import annotations
import abc
from pattern.observer import AbsObserver


# The Subject class
class Subject(abc.ABC):
    """
    A abstract class representing a subject of observation, which can have multiple observers
      attached to it.

    Attributes:
    _observers: A list of AbsObserver objects registered to receive updates, representing the
        observers attached to the subject.

    Methods:
    observer: A getter function that returns the list of observers.
    observer: A setter function that attaches an observer to the subject.
    observer: A deleter function that detaches an observer from the subject.
    set_observer: A function that sets a single observer as the only observer attached to
                 the subject.
    notify: A function that notifies all the attached observers of a change in the subject.
    accept: A function that accepts a visitor and a strategy and calls the visitor's visit
            function passing the subject and the strategy as arguments.
    _calculate_salary: An abstract method that calculates the salary of the subject.

    """

    def __init__(self):
        """
        Constructs a new Subject object.
        """
        self._observers = []

    @property
    def observer(self):
        """
        Gets the list of registered observers.

        Returns:
        A list of observers registered to receive updates.
        """
        return self._observers

    @observer.setter  # attach function
    def observer(self, observer):
        """
        Attaches a new observer to the list of registered observers.

        Args:
        observer: An observer object to be registered for updates.

        Raises:
        TypeError: If the observer is not a subclass of AbsObserver.
        """
        if not isinstance(observer, AbsObserver):
            raise TypeError("Observer must be a subclass of AbsObserver.")
        if observer not in self._observers:
            self._observers.append(observer)

    @observer.deleter  # detach function
    def observer(self, observer):
        """
        Detaches an observer from the list of registered observers.

        Args:
        observer: An observer object to be removed from the list of registered observers.

        Raises:
        TypeError: If the observer is not a subclass of AbsObserver.
        ValueError: If the observer is not attached to the subject.
        """
        if not isinstance(observer, AbsObserver):
            raise TypeError("Observer must be a subclass of AbsObserver.")
        try:
            self._observers.remove(observer)
        except ValueError as exc:
            raise ValueError("Observer is not attached to this subject.") from exc

    def set_observer(self, observer):
        """
        Sets the observer to the list of registered observers, replacing any existing observers.

        Args:
        observer: An observer object to be registered for updates.

        Raises:
        TypeError: If the observer is not a subclass of AbsObserver.
        """
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
        """
        A function that notifies all the attached observers of a change in the subject.
        """
        for observer in self._observers:
            observer.update(self)

    def accept(self, visitor: Visitor, strategy: Strategy) -> None:
        """
        Accepts a visitor and a strategy for processing the subject.

        Args:
        visitor: A Visitor object representing the visitor.
        strategy: A Strategy object representing the strategy.

        Raises:
        NotImplementedError: If the function is not implemented in a subclass.
        """
        visitor.visit(self, strategy)

    def _calculate_salary(self) -> float:
        """
        An abstract method that calculates the salary for the subject.
        """


# The Employee class
class Employee(Subject):
    """
    A class representing an employee in the observer pattern.

    Args:
    name: A string representing the name of the employee.
    salary: A float representing the employee's salary.

    Attributes:
    _name: A string representing the name of the employee.
    _salary: A float representing the employee's salary.
    """

    def __init__(self, name, salary=None):
        """
        Initializes a new instance of the Employee class.

        Args:
        name: A string representing the name of the employee.
        salary: A float representing the employee's salary.
        """
        super().__init__()
        self._name = name
        self._salary = salary

    @property
    def name(self):
        """
        Returns the name of the employee.
        """
        return self._name

    @property
    def salary(self):
        """
        Returns the salary of the employee.
        """
        return self._salary

    @salary.setter
    def salary(self, new_salary):
        # if new_salary != self._salary:
        self._salary = new_salary
        self.notify()

    def _calculate_salary(self) -> float:
        pass
