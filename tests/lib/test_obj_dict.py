import pytest
from src.lib import ObjDict

def test_obj_dict():

    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age
    p = Person("zakaria", 33)
    # initialisation avec un dictionnaire
    obj = ObjDict({"a": 1, "test": {"zak": p}, "b": {"c": 2, "d": [3, 4]}})
    # accès aux éléments avec la notation par point
    assert obj.a == 1
    assert obj.test.zak.age == 33
    assert obj.test.zak.name == "zakaria"
    assert obj.b.c == 2
    assert obj.b.d == [3, 4]

    # ajout d'éléments avec la notation par point 
    obj.x = {"y": 5}
    assert obj.x.y == 5

    # suppression d'éléments avec del 
    del obj.a
    # lève une erreur KeyError lorsqu'un élément n'existe pas
    with pytest.raises(KeyError):
        obj.a

    # delete key not exist
    with pytest.raises(KeyError):
        del obj.a
    # méthode inspect qui affiche joliment l'objet
    obj.inspect  # just check it doesn't raise any error
    # méthode select qui filtre les clés de l'objet.
    assert {'b': {'c': 2, 'd': [3, 4]}} == obj.select(["b"])
