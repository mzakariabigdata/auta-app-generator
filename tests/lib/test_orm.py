import pytest
import re
from src.lib import OrmCollection, ObjDict, BaseMultipleFound, BaseNotFound


@pytest.fixture
def my_orm_collection():
    return OrmCollection(
        [
            ObjDict({"name": "Alice", "age": 25, "gender": "female"}),
            ObjDict({"name": "Bob", "age": 40, "gender": "male"}),
            ObjDict({"name": "Charlie", "age": 30, "gender": "male"}),
            ObjDict({"name": "Dave", "age": 30, "gender": "male"}),
        ]
    )


@pytest.mark.parametrize(
    "query, expected_names",
    [
        ({"age": 25}, {"Alice"}),  # Test finding all elements with age equal to 25
        (
            {"gender": "male", "age": 30},
            {"Charlie", "Dave"},
        ),  # Test finding all elements with gender equal to male and age equal to 30
        (
            {"name": ".*a.*"},
            {"Charlie", "Dave"},
        ),  # Test finding all elements with name containing the letter "a"
        (
            {"age__gt": 25, "name__contains": "v"},
            {"Dave"},
        ),  # Test all objects where age is greater than 25 and name contains "v" (test two conditions)
        (
            {"age__gt": "25"},
            TypeError,
        ),  # Test TypeError
        (
            {"name": re.compile(r".*z.*", re.IGNORECASE)},
            set(),
        ),  # Test finding all elements with name containing the letter "z"
        (
            {"name": ".*a.*|.*e.*"},
            {"Alice", "Charlie", "Dave"},
        ),  # Test finding all elements with name containing the letter "a" or "e"
        (
            {"name": re.compile(r".*ie$", re.IGNORECASE)},
            {"Charlie"},
        ),  # Test finding all elements with name ending with "ie"
        (
            {"name": ""},
            {"Alice", "Bob", "Charlie", "Dave"},
        ),  # Test finding all elements with an empty name (should return all elements)
        (
            {},
            {"Alice", "Bob", "Charlie", "Dave"},
        ),  # Test finding all elements with no params (should return all elements)
        (
            {},
            re.error,
        ),  # Test if an invalid regular expression is used.
        (
            {"age": 100},
            set(),
        ),  # Test finding all elements with age equal to 100 (should return an empty set)
        (
            {"name": "^A.*"},
            {"Alice"},
        ),  # Test finding all elements with name starting with "A"
        (
            {"name": ".*e$"},
            {"Alice", "Charlie", "Dave"},
        ),  # Test finding all elements with name ending with "e"
        (
            {"name": "^A.*|.*e$"},
            {"Alice", "Dave", "Charlie"},
        ),  # Test finding all elements with name starting with "A" or ending with "e"
    ],
)
def test_where(my_orm_collection, query, expected_names):
    # Test finding elements with a regular expression that raises a re.error
    if expected_names == re.error:
        with pytest.raises(re.error):
            my_orm_collection.where(name=re.compile("["))
    elif expected_names == TypeError:
        with pytest.raises(TypeError):
            my_orm_collection.where(**query)
    else:
        # Test finding elements with the given query
        results = my_orm_collection.where(**query)
        assert len(results) == len(expected_names)
        assert set([result["name"] for result in results]) == expected_names

        # Test that where function returns a new OrmCollection instance
        results = my_orm_collection.where(age=25)
        assert my_orm_collection != results


@pytest.mark.parametrize(
    "query, expected_result",
    [
        (
            {"name": "Bob"},
            {"name": "Bob", "age": 40, "gender": "male"},
        ),  # Test finding the element with name equal to "Bob"
        (
            {"name": "Alice", "age": 25},
            {"age": 25, "gender": "female", "name": "Alice"},
        ),  # Test finding the element with name equal to "Alice" and age equal to 25
        (
            {"name": ".*a.*"},
            BaseMultipleFound,
        ),  # Test finding the element with name equal to "Charlie" (not unique)
        (
            {"name": "Eve"},
            BaseNotFound,
        ),  # Test finding the element with name equal to "Eve" (not found)
        (
            {"age": 20},
            BaseNotFound,
        ),  # Test finding the element with age equal to 20 (not found)
        (
            {"email": "alice@example.com"},
            KeyError,
        ),  # Test calling the function with a key that doesn't exist in the collection
        (
            {"age__lt": 30},
            {"age": 25, "gender": "female", "name": "Alice"},
        ),  # Test finding the element with age less than 30
        (
            {"gender__in": ["female", "nonbinary"]},
            {"age": 25, "gender": "female", "name": "Alice"},
        ),  # Test finding the element with gender in ["female", "nonbinary"]
        (
            {"name__startswith": "C"},
            {"name": "Charlie", "age": 30, "gender": "male"},
        ),  # Test finding the element with name starting with "C"
        (
            {"gender__not": "male"},
            {"age": 25, "gender": "female", "name": "Alice"},
        ),  # Test finding the element with gender not equal to "male"
        (
            {"name__endswith": "b"},
            {"name": "Bob", "age": 40, "gender": "male"},
        ),  # Test finding all elements with name ending with "e"
        (
            {"age__lte": 25},
            {"name": "Alice", "age": 25, "gender": "female"},
        ),  # Test finding all elements with age less than or equal to 30
        (
            {"age__gte": 40},
            {"name": "Bob", "age": 40, "gender": "male"},
        ),  # Test finding all elements with age less than or equal to 30
        (
            {"age__gt": 39},
            {"name": "Bob", "age": 40, "gender": "male"},
        ),  # Test finding all elements with age less than or equal to 30
        (
            {"age__nin": [25, 30]},
            {"name": "Bob", "age": 40, "gender": "male"},
        ),  # Test finding all elements with age not equal to 25 or 30
        (
            {"name__contains": "v"},
            {"name": "Dave", "age": 30, "gender": "male"},
        ),  # Test finding all elements with name containing the letter "v"
        (
            {"name__contains": "i"},
            BaseMultipleFound,
        ),  # Test finding all elements with name containing the letter "i"
        ({"name__notValid": "i"}, ValueError),  # Test not valid operator
    ],
)
def test_find_by(my_orm_collection, query, expected_result):
    if expected_result == BaseMultipleFound:
        with pytest.raises(BaseMultipleFound):
            my_orm_collection.find_by(**query)
    elif expected_result == BaseNotFound:
        with pytest.raises(BaseNotFound):
            my_orm_collection.find_by(**query)
    elif expected_result == KeyError:
        with pytest.raises(KeyError):
            my_orm_collection.find_by(**query)
    elif expected_result == ValueError:
        with pytest.raises(ValueError):
            my_orm_collection.find_by(**query)
    else:
        result = my_orm_collection.find_by(**query)
        assert result == expected_result


def test_orm_collection_group_by():
    # TODO : group by name
    # Test group_by() function with a simple list of integers
    lst = OrmCollection([1, 2, 3, 4])
    grouped_lst = lst.group_by(lambda x: x % 2 == 0)
    assert grouped_lst == {True: [2, 4], False: [1, 3]}

    # Test group_by() function with a list of strings
    lst = OrmCollection(["apple", "banana", "orange", "pear", "bouger"])
    grouped_lst = lst.group_by(lambda x: x[0])
    assert grouped_lst == {
        "a": ["apple"],
        "b": ["banana", "bouger"],
        "o": ["orange"],
        "p": ["pear"],
    }


def test_order_by_with_string_key(my_orm_collection):
    ordered_lst = my_orm_collection.order_by("age")
    expected_lst = [
        {"name": "Alice", "age": 25, "gender": "female"},
        {"name": "Charlie", "age": 30, "gender": "male"},
        {"name": "Dave", "age": 30, "gender": "male"},
        {"name": "Bob", "age": 40, "gender": "male"},
    ]
    assert ordered_lst == expected_lst


def test_order_by_with_callable_key(my_orm_collection):
    ordered_lst = my_orm_collection.order_by(lambda x: x["name"])
    expected_lst = [
        {"name": "Alice", "age": 25, "gender": "female"},
        {"name": "Bob", "age": 40, "gender": "male"},
        {"name": "Charlie", "age": 30, "gender": "male"},
        {"name": "Dave", "age": 30, "gender": "male"},
    ]
    assert ordered_lst == expected_lst


def test_order_by_with_invalid_key_type(my_orm_collection):
    with pytest.raises(TypeError):
        my_orm_collection.order_by(123)


def test_orm_collection_order_by():
    # Test order_by() function with a simple list of integers
    lst = OrmCollection([4, 2, 1, 3])
    ordered_lst = lst.order_by()
    assert ordered_lst == [1, 2, 3, 4]

    lst = OrmCollection([4, 2, 1, "3"])
    with pytest.raises(ValueError):
        lst.order_by()

    # Test order_by() function with a list of strings
    lst = OrmCollection(["apple", "banana", "orange", "f", "pear", "c'est encore moi"])
    ordered_lst = lst.order_by(lambda x: len(x))
    assert ordered_lst == ["f", "pear", "apple", "banana", "orange", "c'est encore moi"]


def test_orm_collection_all(my_orm_collection):
    lst = my_orm_collection.all()

    assert len(lst) == 4
    assert all(x.name and x.age and x.gender for x in lst)


def test_orm_collection_offset(my_orm_collection):
    result = my_orm_collection.offset(2)

    assert len(result) == 2
    assert result[0].name == "Charlie"
    assert result[1].name == "Dave"


def test_orm_collection_limit(my_orm_collection):
    result = my_orm_collection.limit(2)

    assert len(result) == 2
    assert result[0].name == "Alice"
    assert result[1].name == "Bob"


def test_orm_collection_distinct():
    # Test distinct() function with non-duplicate values
    lst = OrmCollection([1, 2, 3, 4])
    distinct_lst = lst.distinct()
    assert distinct_lst == [1, 2, 3, 4]

    lst = OrmCollection(["apple", "banana", "orange", "f", "pear", "orange"])
    distinct_lst = lst.distinct()
    assert len(distinct_lst) == 5
    assert distinct_lst == ["apple", "banana", "orange", "f", "pear"]

    # Test distinct() function with duplicate values
    lst = OrmCollection([1, 2, 2, 3, 4, 4])
    distinct_lst = lst.distinct()
    assert distinct_lst == [1, 2, 3, 4]


def test_distinct():
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    persons = OrmCollection(
        [
            Person("John", 25),
            Person("Jane", 30),
            Person("Bob", 25),
            Person("Alice", 35),
            Person("John", 25),
        ]
    )

    # Test with one field
    distinct_persons = persons.distinct("name")
    assert len(distinct_persons) == 4
    assert all(
        person.name in {"John", "Jane", "Bob", "Alice"} for person in distinct_persons
    )

    # Test with two fields
    distinct_persons = persons.distinct("name", "age")
    assert len(distinct_persons) == 4
    assert all(
        (person.name, person.age)
        in {("John", 25), ("Jane", 30), ("Bob", 25), ("Alice", 35)}
        for person in distinct_persons
    )

    # Test with missing argument
    try:
        persons.distinct()
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"

    # Test with non-existent field
    try:
        persons.distinct("non_existent_field")
    except AttributeError:
        pass
    else:
        assert False, "Expected AttributeError"
