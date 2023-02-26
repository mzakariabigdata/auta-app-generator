import pytest
from src.lib import (
    OrmCollection,
    ObjDict,
)


@pytest.fixture
def my_orm_collection():
    """Fixture that returns an instance of the OrmCollection class with test data.

    Returns an instance of the OrmCollection class containing four dictionaries created with
    the class ObjDict, each representing a person with a name (key "name"), an age (key "age")
    and a sex ("gender" key).

    Returns:
        OrmCollection: an instance of the OrmCollection class.
            - 'name': str, the name of the person.
            - 'age': int, the age of the person.
            - 'gender': str, the gender of the person.
    """
    return OrmCollection(
        [
            ObjDict({"name": "Alice", "age": 25, "gender": "female"}),
            ObjDict({"name": "Bob", "age": 40, "gender": "male"}),
            ObjDict({"name": "Charlie", "age": 30, "gender": "male"}),
            ObjDict({"name": "Dave", "age": 30, "gender": "male"}),
        ]
    )


@pytest.fixture
def my_orm_collection_group():
    """
    A fixture that returns an ORM collection of objects representing people, with additional data
    on their occupation.

    Returns an instance of the OrmCollection class containing four dictionaries created with
    the class ObjDict, each representing a person with a name (key "name"), an age (key "age"),
    a sex ("gender" key) and occupation ("taf" key)

    Returns:
        OrmCollection: A collection of ObjDict objects, where each object has the following fields:
            - 'name': str, the name of the person.
            - 'age': int, the age of the person.
            - 'gender': str, the gender of the person.
            - 'taf': str, the occupation of the person.
    """
    return OrmCollection(
        [
            ObjDict({"name": "Alice", "age": 25, "gender": "female", "taf": "psy"}),
            ObjDict({"name": "Alice", "age": 80, "gender": "male", "taf": "retraite"}),
            ObjDict({"name": "Bob", "age": 40, "gender": "male", "taf": "cia"}),
            ObjDict({"name": "Charlie", "age": 30, "gender": "male", "taf": "etud"}),
            ObjDict({"name": "Charlie", "age": 30, "gender": "male", "taf": "prof"}),
            ObjDict({"name": "Dave", "age": 30, "gender": "male", "taf": "ing"}),
            ObjDict({"name": "Dave", "age": 31, "gender": "male", "taf": "chomor"}),
        ]
    )


@pytest.fixture
def sample_obj_dict():
    """Fixture that returns a sample ObjDict object."""

    return ObjDict(
        {
            "name": "John",
            "age": 30,
            "address": {"street": "123 Main St", "city": "Anytown", "state": "CA"},
            "scores": [90, 80, 95],
        }
    )


@pytest.fixture(scope="module")
def Person():
    """Fixture that returns a sample Person object."""

    class Person:
        def __init__(self, name, age, salary):
            self.name = name
            self.age = age
            self.salary = salary

        @property
        def ret_name(self):
            return self.name

        def get_name(self):
            return self.name

        def upper_name(self):
            return self.name.upper()

        def get_age(self):
            return self.age

        def change_name(self, new_name):
            self.name = new_name

        def change_age(self, new_age):
            self.age = new_age

        def is_adult(self):
            return self.age >= 18

        def set_name(self, new_name):
            self.name = new_name

        def __repr__(self):
            return f"Person(name='{self.name}', age={self.age}, age={self.salary} )"

    return Person


@pytest.fixture
def person():
    """Fixture that returns a sample Person object."""

    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def __repr__(self):
            return f"Person(name='{self.name}', age={self.age})"

    return Person("zakaria", 33)


@pytest.fixture
def obj(person):
    """Fixture that returns a sample ObjDict object with nested Person object."""

    return ObjDict({"a": 1, "test": {"zak": person}, "b": {"c": 2, "d": [3, 4]}})
