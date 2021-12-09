import json

import pytest

from Knapsack import (
    Knapsack, solve_knapsack_greedy
)


def get_small_objects_dict(capacity=60):
    small_objects_dict = {
        "Épée de lumière lunaire": [909, 6],
        "Flèche incassable": [697, 5],
        "Grimoire résistant": [878, 6],
        "Armure rutilante": [349, 14],
        "Baguette du grincheux": [871, 8],
        "Bâton des chants d'oiseaux": [646, 6],
        "Bottes d'empreintes factices": [646, 1],
        "Bouclier expressif": [316, 13],
        "Bourse à épices magique d'Heward": [198, 2],
        "Cadenas sournois": [362, 6],
        "Canne de vétéran": [9, 2],
        "Cape virevoltante": [420, 6],
        "Chandelle des profondeurs": [177, 3],
        "Chapeau de magicien": [349, 4],
        "Chope de sobriété": [382, 4],
        "Clé mystérieuse": [76, 8],
    }
    return Knapsack(capacity), small_objects_dict


def get_medium_objects_dict():
    with open("stuff_dd.json") as file:
        data = json.load(file)
    return data["stuff_dd"]


class TestUtils:
    def test_print(self, capsys):
        sack, objects_dict = get_small_objects_dict()
        sack.content = [
            "Cape virevoltante",
            "Chapeau de magicien",
            "Bâton des chants d'oiseaux",
            "Grimoire résistant"
        ]
        sack.print_content(objects_dict)

        captured = capsys.readouterr()
        assert captured.out == "Cape virevoltante 420 6\n" \
                               "Chapeau de magicien 349 4\n" \
                               "Bâton des chants d'oiseaux 646 6\n" \
                               "Grimoire résistant 878 6\n" \
                               "Le sac a 4 objets, pour une valeur de 2293 et un poids de 22/60\n"

    def test_print_empty(self, capsys):
        sack, objects_dict = get_small_objects_dict()
        sack.print_content(objects_dict)

        captured = capsys.readouterr()
        assert captured.out == "Le sac a 0 objets, pour une valeur de 0 et un poids de 0/60\n"

    def test_get_value_and_weight(self):
        sack, objects_dict = get_small_objects_dict()
        sack.content = [
            "Cape virevoltante",
            "Chapeau de magicien",
            "Bâton des chants d'oiseaux",
            "Grimoire résistant"
        ]
        assert sack.get_value_and_weight(objects_dict) == (2293, 22)

    def test_get_value_and_weight_empty(self):
        sack, objects_dict = get_small_objects_dict()
        assert sack.get_value_and_weight(objects_dict) == (0, 0)


class TestGreedySmall:
    def test_solve(self):
        sack, objects_dict = get_small_objects_dict()
        filled_sack = solve_knapsack_greedy(knapsack=sack, objects_dict=objects_dict)
        assert filled_sack.get_value_and_weight(objects_dict) == (6544, 59)

    @pytest.mark.parametrize(
        "capacity, weight, value",
        [
            (1000, 7285, 94),
            (100, 7285, 94),
            (50, 6005, 50),
            (10, 1753, 9),
            (5, 853, 5),
            (0, 0, 0),
        ])
    def test_solve_bigger(self, capacity, weight, value):
        sack, objects_dict = get_small_objects_dict(capacity)
        filled_sack = solve_knapsack_greedy(knapsack=sack, objects_dict=objects_dict)
        assert filled_sack.get_value_and_weight(objects_dict) == (weight, value)


class TestGreedyMedium:
    def test_solve(self):
        sack = Knapsack(100)
        objects_dict = get_medium_objects_dict()
        filled_sack = solve_knapsack_greedy(knapsack=sack, objects_dict=objects_dict)
        assert filled_sack.get_value_and_weight(objects_dict) == (118000455, 100)

    @pytest.mark.parametrize(
        "capacity, weight, value",
        [
            (10000, 203583402, 9723),
            (1000, 163881015, 1000),
            (100, 118000455, 100),
            (50, 84260426, 50),
            (10, 18220131, 10),
            (5, 260148, 5),
            (3, 180019, 3),
            (1, 40081, 1),
        ])
    def test_solve_medium(self, capacity, weight, value):
        sack = Knapsack(capacity)
        objects_dict = get_medium_objects_dict()
        filled_sack = solve_knapsack_greedy(knapsack=sack, objects_dict=objects_dict)
        assert filled_sack.get_value_and_weight(objects_dict) == (weight, value)
        if capacity > 5:
            assert "Oeil et Main de Vecna" in sack.content

    @pytest.mark.parametrize(
        "capacity, weight, value",
        [(1000000, 203653539, 20737), (100000000, 203671588, 1020746)])
    def test_solve_big(self, capacity, weight, value):
        sack = Knapsack(capacity)
        objects_dict = get_medium_objects_dict()
        filled_sack = solve_knapsack_greedy(knapsack=sack, objects_dict=objects_dict)
        assert filled_sack.get_value_and_weight(objects_dict) == (weight, value)
        if capacity > 5:
            assert "Oeil et Main de Vecna" in sack.content
