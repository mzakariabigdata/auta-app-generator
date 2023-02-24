import pytest
from src.lib import ObjDict


@pytest.fixture
def person():
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def __repr__(self):
            return f"Person(name='{self.name}', age={self.age})"

    return Person("zakaria", 33)


@pytest.fixture
def obj(person):
    return ObjDict({"a": 1, "test": {"zak": person}, "b": {"c": 2, "d": [3, 4]}})


def describe_objdict():
    @pytest.mark.parametrize(
        "select_keys, expected",
        [
            (["c"], pytest.raises(KeyError)),
            (["b", "c", "d"], pytest.raises(KeyError)),
            (None, pytest.raises(TypeError)),
            ("b", pytest.raises(TypeError)),
            (["b", 1], pytest.raises(TypeError)),
        ],
        ids=[
            "Test with non-existent key in select",
            "Test with non-existent key in nested select",
            "Test with None argument for select",
            "Test with non-list argument for select",
            "Test with non-string element in select",
        ],
    )
    def test_obj_with_errors(obj, select_keys, expected):
        with expected:
            obj.select(select_keys)

    @pytest.mark.parametrize(
        "select_keys, expected",
        [
            pytest.param(["b"], {"b": {"c": 2, "d": [3, 4]}}, id="select_existing_key"),
            pytest.param([], {}, id="select_empty_list"),
        ],
    )
    def test_obj_dict(obj, select_keys, expected):
        # initialisation avec un dictionnaire
        # vérifier que l'objet initialisé est bien une instance de ObjDict
        assert isinstance(obj, ObjDict)
        # accès aux éléments avec la notation par point
        obj.a == 1
        obj.test.zak.age == 33
        obj.test.zak.name == "zakaria"
        assert obj.b.c == 2
        obj.b.d == [3, 4]
        obj.ka = "12"

        # s'assurer que la valeur assignée est toujours un dictionnaire
        # with pytest.raises(TypeError):
        #     ObjDict("a")
        # ajout d'éléments avec la notation par point
        obj.x = {"y": 5}
        assert obj.x.y == 5

        # méthode select qui filtre les clés de l'objet.
        assert expected == obj.select(select_keys)

    def test_inspect_success(capsys):
        obj = ObjDict({"a": 1, "b": 2})
        obj.inspect
        captured = capsys.readouterr()
        assert captured.out == "{'a': 1, 'b': 2}\n"
        assert captured.err == ""

    def test_delattr(obj):
        # suppression d'éléments avec del
        del obj.a
        # lève une erreur KeyError lorsqu'un élément n'existe pas
        with pytest.raises(AttributeError):
            obj.a

        with pytest.raises(AttributeError):
            del obj.non_existent_attribute
