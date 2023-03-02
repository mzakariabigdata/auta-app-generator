""" FullTimeEmployee module"""

from . import Employee


class FullTimeEmployee(Employee):
    """Une classe qui représente un employé à temps plein.

    Hérite de la classe Employee et définit un salaire fixe.

    Attributs:
        name (str): le nom de l'employé
        _salary (float): le salaire annuel de l'employé

    Méthodes:
        _calculate_salary(): calcule le salaire annuel de l'employé
    """

    def __init__(self, name: str):
        super().__init__(name)
        self._salary = self._calculate_salary()

    def _calculate_salary(self) -> float:
        """Calcule le salaire annuel de l'employé.

        Retourne:
            float: le salaire annuel de l'employé
        """
        return 120000.0
