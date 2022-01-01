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
    index_weight = knapsack.capacity
    # si le sac a une capacité = 0 on le retourne directement
    if index_weight == 0:
        return knapsack
    index_items = len(objects_dict)
    # transforme le dictionnaire en liste
    objects_list = list(objects_dict.items())
    # initialise la matrice (1 ligne par item et 1 colonne par poids (avec 0))
    matrice = get_dynamic_program_matrice(index_weight, index_items, objects_list)

    # afin d'eviter d'avoir une erreur d'index
    index_items -= 1

    while matrice[index_items][index_weight] == matrice[index_items][index_weight - 1]:
        index_weight -= 1

    while index_weight > 0:
        while index_items > 0 and matrice[index_items][index_weight] == matrice[index_items - 1][index_weight]:
            index_items -= 1
        index_weight = index_weight - objects_list[index_items][1][1]
        if index_weight >= 0:
            knapsack.content.append(objects_list[index_items][0])
        index_items -= 1
    return knapsack


def get_dynamic_program_matrice(weight, data_size, data_list):
    matrice = [[0 for _ in range(weight + 1)] for _ in range(data_size)]
    # programmation dynamique
    # pour le premier objet (pb d'index sinon)
    for i in range(0, weight + 1):
        # [0] objet 0, [1] tableau, [1] poids
        # si le poids de la colonne est assez grand pour contenir l'objet
        if not data_list[0][1][1] > i:
            matrice[0][i] = data_list[0][1][0]
    # pour le reste des objets
    for i in range(1, data_size):  # fait le tour des objets
        for j in range(0, weight + 1):  # fait le tour des poids
            if data_list[i][1][1] > j:
                matrice[i][j] = matrice[i - 1][j]
            else:  # on prend le max entre la ligne du dessus a la même colonne et la valeur optimisé a la ligne du dessus pour un poids pouvant contenir le dernier objet
                matrice[i][j] = max(matrice[i - 1][j], matrice[i - 1][j - data_list[i][1][1]] + data_list[i][1][0])
    return matrice


if __name__ == '__main__':
    # dico = {
    #     'Objet0': [15, 5],
    #     'Objet1': [10, 1],
    #     'Objet2': [12, 3],
    #     'Objet3': [4, 17],
    #     'Objet4': [20, 4],
    #     'Objet5': [2, 1],
    # }
    # sac = Knapsack(5)
    # solve_knapsack_optimal(sac, dico).print_content(dico)
