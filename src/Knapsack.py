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

        res += 'Le sac a ' + len(self.content).__str__() + ' objets, '
        res += 'pour une valeur de ' + str(self.get_value_and_weight(objects_dict)[0])
        res += ' et un poids de ' + str(self.get_value_and_weight(objects_dict)[1]) + '/' + str(self.capacity)
        return res


def solve_knapsack_greedy(knapsack, objects_dict) -> Knapsack:
    # Make a dictionary which associate objects names by objects value by weight
    dict_value_by_weight = {}
    for name in objects_dict.keys():
        dict_value_by_weight[name] = objects_dict[name][0] / objects_dict[name][1]
    # Sort it
    sorted_dict = sorted(dict_value_by_weight.items(), key=lambda dict_content: dict_content[1], reverse=True)

    # Keep adding content to the knapsack until no more content can be added
    knapsack_weight = 0
    for name, weight_by_value in sorted_dict:
        # Stop looping if the knapsack is already full
        if knapsack_weight == knapsack.capacity:
            break
        # Check if the next content will fit in the knapsack
        if knapsack_weight + objects_dict[name][1] <= knapsack.capacity:
            knapsack_weight += objects_dict[name][1]
            knapsack.content.append(name)
    return knapsack


def solve_knapsack_best(knapsack, objects_dict) -> Knapsack:
    # TODO
    pass


def solve_knapsack_optimal(knapsack, objects_dict) -> Knapsack:
    # TODO
    pass
