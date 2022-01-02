def get_value(objects_dict, item) -> int:
    """
    Get the value of the item in the dictionary used
    :param objects_dict: the dictionary used
    :param item: the name of the item whose value is desired
    :return: int: the value of the item
    """
    return objects_dict.get(item)[0]


def get_weight(objects_dict, item) -> int:
    """
    Get the weight of the item in the dictionary used
    :param objects_dict: the dictionary used
    :param item: the name of the item whose weight is desired
    :return: int: the weight of the item
    """
    return objects_dict.get(item)[1]


class Knapsack:
    def __init__(self, capacity):
        """
        Initialize the knapsack
        :param capacity: the knapsack's capacity
        """
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

    for item_name, value_per_weight in sorted_greedy_list:
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
    # Make a list which associate objects names by its value per weight
    greedy_list = []
    for item_name, (value, weight) in objects_dict.items():
        greedy_list.append((item_name, value / weight))
    # Sort the greedy_list by value per weight
    greedy_list.sort(key=lambda item: item[1], reverse=True)
    return greedy_list


def solve_knapsack_best(knapsack, objects_dict) -> Knapsack:
    # TODO
    pass


def solve_knapsack_optimal(knapsack, objects_dict) -> Knapsack:
    """
    Resolve the knapsack problem in the optimal way :
    give the best solution, searching among all the possible solutions.
    :param knapsack: the knapsack to sort
    :param objects_dict: the dictionary used
    :return: Knapsack: the knapsack sorted
    """
    index_weight = knapsack.capacity

    # If the knapsack has zero capacity, return the empty knapsack
    if index_weight == 0:
        return knapsack

    # Transform the dictionary into a list
    objects_list = list(objects_dict.items())
    index_items = len(objects_dict)

    # Build a matrix with the get_dynamic_program_matrix method
    # 1 row per item & 1 column per unit of knapsack's weight
    matrix = get_dynamic_program_matrix(index_weight, index_items, objects_list)

    # Fill the knapsack by using the matrix :

    # If the last value of the last item's row is the same of the before last value,
    # the value does not need to be taken, so it pass to the previous one by decreasing
    index_items -= 1
    while matrix[index_items][index_weight] == matrix[index_items][index_weight - 1]:
        index_weight -= 1

    while index_weight > 0:
        # While the last item have the same value of the before last item for the same knapsack's weight,
        # the item does not need to be taken, so it pass to the previous one by decreasing
        while index_items > 0 and matrix[index_items][index_weight] == matrix[index_items - 1][index_weight]:
            index_items -= 1
        index_weight -= objects_list[index_items][1][1]
        if index_weight >= 0:
            # Adding the item in the knapsack
            knapsack.content.append(objects_list[index_items][0])
        index_items -= 1
    return knapsack


def get_dynamic_program_matrix(weight, data_size, data_list):
    """
    Build a matrix with 1 row per dictionary's item & 1 column per unit of knapsack's weight
    :param weight: the knapsack's capacity
    :param data_size: the length of the dictionary
    :param data_list: the dictionary as a list
    :return: the matrix created
    """
    # Initialization of the matrix
    matrix = [[0 for _ in range(weight + 1)] for _ in range(data_size)]

    # Matrix filling :

    # One loop for the first item
    for i in range(0, weight + 1):
        item_value, item_weight = data_list[0][1]
        # If the column is "heavy" enough to contain the weight of the first item
        if item_weight <= i:
            # The value is put in the matrix, at the right column
            matrix[0][i] = item_value

    # One loop for the other items
    for i in range(1, data_size):
        # One loop per unit of weight + 1
        for j in range(0, weight + 1):
            # If the column is not "heavy" enough to contain the weight of the actual item
            item_value, item_weight = data_list[i][1]
            if item_weight > j:
                # The value of the last item at the same weight's column is put
                matrix[i][j] = matrix[i - 1][j]
            else:
                # The maximum value between the last item at the same weight's column
                # the value in the previous line at weight's column which can contain the actual item
                matrix[i][j] = max(matrix[i - 1][j], matrix[i - 1][j - item_weight] + item_value)
    return matrix


if __name__ == '__main__':
    dico = {
        'Objet0': [15, 5],
        'Objet1': [10, 1],
        'Objet2': [12, 3],
        'Objet3': [4, 17],
        'Objet4': [20, 4],
        'Objet5': [2, 1],
    }
    sac = Knapsack(5)
    solve_knapsack_optimal(sac, dico).print_content(dico)
