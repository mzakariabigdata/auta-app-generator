""" Visitor module"""

import abc


class AbsVisitor(abc.ABC):
    """
    An abstract base class for visitors.

    Attributes:
    Inherits from abc.ABC.
    """

    def __init__(self):
        self.subject = None
        self.strategy = None

    def visit(self, subject, strategy):
        """
        Abstract method for visiting a subject with a given strategy.

        Args:
        subject: A subject object to visit.
        strategy: A tax strategy object to use for tax calculation.
        """

    def set_strategy(self, strategy):
        """
        Sets the tax strategy to use for tax calculation.
        """
        self.strategy = strategy

    def get_strategy(self):
        """
        Gets the current tax strategy.
        """
        return self.strategy

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


class PayrollVisitor(AbsVisitor):
    """
    A concrete visitor for payroll updates.

    Attributes:
    Inherits from AbsVisitor.
    """

    def visit(self, subject, strategy):
        """
        Visit a subject and execute a given tax strategy for payroll updates.

        Args:
        subject: A subject object to visit.
        strategy: A tax strategy object to use for tax calculation.
        """
        if strategy is not None:
            print(
                f"TaxAuthorityVisitor; Employee name: {subject.name}, salary: {subject.salary}, "
                f"tax: {strategy.execute(subject)}"
            )


class TaxAuthorityVisitor(AbsVisitor):
    """
    A concrete visitor for tax authority updates.

    Attributes:
    Inherits from AbsVisitor.
    """

    def visit(self, subject, strategy):
        """
        Visit a subject and execute a given tax strategy for tax authority updates.

        Args:
        subject: A subject object to visit.
        strategy: A tax strategy object to use for tax calculation.
        """
        if strategy is not None:
            print(
                f"TaxAuthorityVisitor; Employee name: {subject.name},"
                f"salary: {subject.salary},"
                f"tax: {strategy.execute(subject)}"
            )
