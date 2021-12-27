def get_value(objects_dict, item) -> int:
    """
    Get the value of the item in the dictionary used
    :param objects_dict: the dictionary used
    :param item: the name of the item we want the value
    :return: int: the value of the item
    """
    return objects_dict.get(item)[0]


def get_weight(objects_dict, item) -> int:
    """
    Get the weight of the item in the dictionary used
    :param objects_dict: the dictionary used
    :param item: the name of the item we want the weight
    :return: int: the weight of the item
    """
    return objects_dict.get(item)[1]


class Knapsack:
    def __init__(self, capacity):
        self.capacity = capacity
        self.content = []

    def get_value_and_weight(self, objects_dict) -> (int, int):
        """
        Get the value and the weight of a knapsack in the dictionary used
        :param objects_dict: the dictionary used
        :return: (int,int): the value & the weight
        """
        value = 0
        weight = 0
        for self_content in self.content:
            value += get_value(objects_dict, self_content)
            weight += get_weight(objects_dict, self_content)
        return value, weight

    def print_content(self, objects_dict) -> None:
        """
        Print the content of the knapsack using the two to_string methods
        :param objects_dict: the dictionary used
        """
        print(self.items_to_string(objects_dict),
              self.info_to_string(objects_dict),
              sep='')

    def items_to_string(self, objects_dict) -> str:
        """
        Get the name, the value and the weight of the content of the knapsack as a string using the dictionary
        :param objects_dict: the dictionary used
        :return: str: the name, the value and the weight of the content of the knapsack as a string
        """
        items_string = ''
        for item in self.content:
            items_string += item + ' '
            items_string += objects_dict.get(item)[0].__str__() + ' '
            items_string += objects_dict.get(item)[1].__str__() + '\n'
        return items_string

    def info_to_string(self, objects_dict) -> str:
        """
        Get the information of the knapsack as a string using the dictionary
        :param objects_dict: the dictionary used
        :return: str: the information of the knapsack as a string
        """
        knapsack_value_and_weight = self.get_value_and_weight(objects_dict)
        info_string = 'Le sac a ' + len(self.content).__str__()
        info_string += ' objets, pour une valeur de '
        info_string += knapsack_value_and_weight[0].__str__()
        info_string += ' et un poids de '
        info_string += knapsack_value_and_weight[1].__str__()
        info_string += '/' + self.capacity.__str__()
        return info_string


def solve_knapsack_greedy(knapsack, objects_dict) -> Knapsack:
    """
    Resolve the knapsack problem in the greedy way :
    sort the objects according to their values per weight, and add gradually to the bag the
    elements having the greatest value per weight, until the moment when the bag is full.
    :param knapsack: the knapsack to sort
    :param objects_dict: the dictionary used
    :return: Knapsack: the knapsack sorted
    """
    # Fill the knapsack with objects which have the best value per weight
    sorted_greedy_list = get_sorted_greedy_list(objects_dict)

    # Keep adding content to the knapsack until no more content can be added
    knapsack_weight = knapsack.get_value_and_weight(objects_dict)[1]

    for item_name, useless in sorted_greedy_list:
        # Check if the next content will fit in the knapsack
        if knapsack_weight + objects_dict[item_name][1] <= knapsack.capacity:
            knapsack_weight += objects_dict[item_name][1]
            knapsack.content.append(item_name)

            # Stop looping if the knapsack is full
            if knapsack_weight == knapsack.capacity:
                break
    return knapsack


def get_sorted_greedy_list(objects_dict) -> list:
    """
    Create a list associating the name of each item in the dictionary by its value per weight
    :param objects_dict: the dictionary used
    :return: list: list with the name of each item in the dictionary and its value per weight
    """
    # Make a dictionary which associate objects names by its value per weight
    greedy_dict = {}
    for item in objects_dict.keys():
        greedy_dict[item] = objects_dict[item][0] / objects_dict[item][1]
    # Make a sorted list by value per weight with the greedy_dict content
    sorted_greedy_list = sorted(greedy_dict.items(),
                                key=lambda content: content[1],
                                reverse=True)
    return sorted_greedy_list


def solve_knapsack_best(knapsack, objects_dict) -> Knapsack:
    # TODO
    pass


def solve_knapsack_optimal(knapsack, objects_dict) -> Knapsack:
    # TODO
    pass
