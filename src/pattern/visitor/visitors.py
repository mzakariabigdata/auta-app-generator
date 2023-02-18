""" Visitor module"""

import abc


class AbsVisitor(abc.ABC):
    """Abs visitor

    Args:
        abc (abs): _description_
    """

    def visit(self, subject, strategy):
        pass


class PayrollVisitor(AbsVisitor):
    """Pyroll visitor

    Args:
        AbsVisitor (Visitor): _description_
    """

    def visit(self, subject, strategy):
        if strategy is not None:
            print(
                "TaxAuthorityVisitor; Employee name: {}, salary: {}, tax: {}".format(
                    subject.name, subject.salary, strategy.execute(subject)
                )
            )


class TaxAuthorityVisitor(AbsVisitor):
    """Tax authority visitor

    Args:
        AbsVisitor (Visitor): _description_
    """

    def visit(self, subject, strategy):
        if strategy is not None:
            print(
                f"TaxAuthorityVisitor; Employee name: {subject.name},"
                f"salary: {subject.salary},"
                f"tax: {strategy.execute(subject)}"
            )
