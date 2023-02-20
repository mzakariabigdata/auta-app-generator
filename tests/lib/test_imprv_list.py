from src.lib import ImprovedList
from io import StringIO
import sys


def test_inspect():
    # Test display an empty list
    empty_list = ImprovedList()
    empty_list.inspect

    # Test display a list with one element
    one_element_list = ImprovedList([1])
    one_element_list.inspect

    # Test display a list with several elements of different types
    complex_list = ImprovedList([1, "string", [1, 2], {"a": 1, "b": 2}])
    complex_list.inspect

    # Test display a list with several elements of different types nested

    complex_list = ImprovedList(
        [1, "string", [1, 2], {"a": 1, "b": {"z": 1, "m": [1, 2]}}]
    )
    complex_list.inspect

    # Test that inspect method is called on element with inspect method defined
    class Inspectable:
        def __init__(self, name):
            self.name = name

        def inspect(self):
            print(f"Inspectable({self.name})")

    inspectable_list = ImprovedList([Inspectable("element1"), Inspectable("element2")])
    captured_output = StringIO()  # créer un StringIO pour capturer la sortie
    sys.stdout = captured_output  # rediriger la sortie standard vers StringIO
    inspectable_list.inspect == 5  # appeler la méthode inspect() sur la liste
    sys.stdout = sys.__stdout__  # remettre la sortie standard à sa valeur par défaut
    assert (
        captured_output.getvalue()
        == "ImprovedList(Inspectable) data:\nInspectable(element1)\nInspectable(element2)\n"
    )  # la chaîne de caractères attendue pour la sortie de la méthode


def test_first():
    # Test getting the first element of a list
    simple_list = ImprovedList([1, 2, 3])
    assert simple_list.first() == 1

    # Test getting the first two elements of a list
    assert simple_list.first(2) == ImprovedList([1, 2])

    # Test getting the first element of an empty list
    empty_list = ImprovedList()
    assert empty_list.first() is None


def test_last():
    # Test getting the last element of a list
    simple_list = ImprovedList([1, 2, 3])
    assert simple_list.last() == 3

    # Test getting the last two elements of a list
    assert simple_list.last(2) == ImprovedList([2, 3])

    # Test getting the last element of an empty list
    empty_list = ImprovedList()
    assert empty_list.last() is None


def test_map():
    # Test calling a method on each element of a list
    simple_list = ImprovedList([1, 2, 3])
    assert simple_list.map(":__str__") == ImprovedList(["1", "2", "3"])
    assert simple_list.map("real") == ImprovedList([1.0, 2.0, 3.0])

    # Test calling an attribute on each element of a list
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def upper_name(self):
            return self.name.upper()

    people_list = ImprovedList(
        [Person("Alice", 25), Person("Bob", 30), Person("Charlie", 35)]
    )
    assert people_list.map("name") == ImprovedList(["Alice", "Bob", "Charlie"])
    assert people_list.map("age") == ImprovedList([25, 30, 35])
    assert people_list.map(":upper_name") == ImprovedList(["ALICE", "BOB", "CHARLIE"])
