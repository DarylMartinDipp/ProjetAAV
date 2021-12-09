class Knapsack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.content = []

    def get_value_and_weight(self, objects_dict) -> (int, int):
        value = 0
        weight = 0
        for self_content in self.content:
            value += objects_dict.get(self_content)[0]
            weight += objects_dict.get(self_content)[1]
        return value, weight

    def print_content(self, objects_dict) -> None:
        print(self.to_string(objects_dict))

    def to_string(self, objects_dict):
        res = ''
        for self_content in self.content:
            res += self_content + ' '
            res += objects_dict.get(self_content)[0].__str__() + ' '
            res += objects_dict.get(self_content)[1].__str__() + '\n'

        res += 'Le sac a ' + len(self.content).__str__() + ' objets,'
        res += ' pour une valeur de ' + self.get_value_and_weight(objects_dict)[0].__str__()
        res += ' et un poids de ' + self.get_value_and_weight(objects_dict)[1].__str__() + '/' + self.capacity.__str__()
        return res


def solve_knapsack_greedy(knapsack, objects_dict) -> Knapsack:
    # TODO
    pass


def solve_knapsack_best(knapsack, objects_dict) -> Knapsack:
    # TODO
    pass


def solve_knapsack_optimal(knapsack, objects_dict) -> Knapsack:
    # TODO
    pass
