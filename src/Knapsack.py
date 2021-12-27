def get_value_content(objects_dict, self_content):
    return objects_dict.get(self_content)[0]


def get_weight_content(objects_dict, self_content):
    return objects_dict.get(self_content)[1]


class Knapsack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.content = []

    def get_value_and_weight(self, objects_dict) -> (int, int):
        """
        Return the value and the weight of a knapsack
        :param objects_dict: the dictionary used
        :return: the value & the weight
        """
        value = 0
        weight = 0
        for self_content in self.content:
            value += get_value_content(objects_dict, self_content)
            weight += get_weight_content(objects_dict, self_content)
        return value, weight

    def print_content(self, objects_dict) -> None:
        """
        Print the content of the knapsack using the to_string method
        :param objects_dict: the dictionary used
        """
        print(self.to_string(objects_dict))

    def to_string(self, objects_dict):
        """
        Return the content of knapsack as a string
        :param objects_dict: the dictionary used
        :return: the content of knapsack as a string
        """
        string = ''
        for self_content in self.content:
            string += self_content + ' '
            string += get_value_content(objects_dict, self_content).__str__() + ' '
            string += get_weight_content(objects_dict, self_content).__str__() + '\n'

        string += 'Le sac a ' + len(self.content).__str__() + ' objets, '
        string += 'pour une valeur de ' + str(self.get_value_and_weight(objects_dict)[0])
        string += ' et un poids de ' + str(self.get_value_and_weight(objects_dict)[1]) + '/' + str(self.capacity)
        return string


def solve_knapsack_greedy(knapsack, objects_dict) -> Knapsack:
    """
    Resolve the knapsack problem in the greedy way :
    sort the objects according to their values per weight, and add gradually to the bag the
    elements having the greatest value per weight, until the moment when the bag is full.

    :param knapsack: the knapsack to sort
    :param objects_dict: the dictionary used
    :return: the knapsack sorted
    """
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
