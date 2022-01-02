from ProfessorKnapsack import Knapsack as ProfessorKnapsack


class Knapsack(ProfessorKnapsack):
    def __init__(self, capacity):
        """
        Initialize the knapsack
        :param capacity: the knapsack's capacity
        """
        super().__init__(capacity)

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


def solve_knapsack_greedy(knapsack, objects_dict) -> Knapsack:
    """
    Resolve the knapsack problem in the greedy way :
    sort the objects according to their values per weight, and add gradually to the bag the
    elements having the greatest value per weight, until the moment when the bag is full.
    :param knapsack: the knapsack to fill
    :param objects_dict: the dictionary used
    :return: KnapsackComplet: the knapsack filled
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
    """
    Resolve the knapsack problem in the best way :
    give the best solution, searching among all the possible solutions.
    :param knapsack: the knapsack to fill
    :param objects_dict: the dictionary used
    :return: KnapsackComplet: the knapsack filled
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


def solve_knapsack_optimal(knapsack, objects_dict) -> Knapsack:
    """
    Resolve the knapsack problem in the optimal way :
    give a solution with the highest value possible,
    searching among all the possible combination.
    :param knapsack: the knapsack to fill
    :param objects_dict: the dictionary used
    :return: KnapsackComplet: the knapsack filled
    """
    # Transform the dictionary into a list
    objects_list = list(objects_dict.items())

    # Get the brute force result
    _, liste = brute_force_research(knapsack.capacity, objects_list, [])

    # Fill the knapsack with the combination given by the brute force algorithm
    for item in liste:
        knapsack.content.append(item[0])

    return knapsack


def brute_force_research(max_weight, data_list, data_content) -> (int, list):
    """
    Search among all the combinations of the data_list to find the one that give the highest value
    :param max_weight: the knapsack's capacity
    :param data_list: item's list
    :param data_content: the current combination
    :return: int: the current combination value
    :return: list: the new combination
    """
    if data_list:
        # Do the "Brute force" algorithm by removing the current item of the data_list
        val_without_item, list_without_item = brute_force_research(max_weight, data_list[1:], data_content)
        # Stock the current item
        item = data_list[0]
        # If the current item can fit in the knapsack
        if item[1][1] <= max_weight:
            # Do the "Brute force" algorithm by adding the current item in the combination
            val_with_item, list_with_item = brute_force_research(max_weight - item[1][1], data_list[1:], data_content + [item])
            # If the value increase with the current items
            if val_without_item < val_with_item:
                return val_with_item, list_with_item

        return val_without_item, list_without_item
    else:
        # Return of the value and the list of the new combination
        return sum([i[1][0] for i in data_content]), data_content
