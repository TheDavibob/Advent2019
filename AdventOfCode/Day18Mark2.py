import numpy as np:

class TheVault:
    def __init__(self):
        self.map = np.array([])
        self.flood_map = self.map
        self.distance_travelled = 0

    def create_map_from_string(self, map_string):
        lines = map_string.split('\n')
        width = len(lines[0])
        height = len(lines)
        self.map = np.zeros([height, width])

        list_map = []
        # First up, create a list array
        for line in lines:
            list_map.append([letter for letter in line])

        # Convert all walls and open spaces to 1s and 0s
        # Real numbers are always fine, as the bounding edges are walls

        for m, line in enumerate(list_map):
            for n, letter in enumerate(line):
                if letter == '#':
                    list_map[m][n] = 0
                elif letter == '.':
                    list_map[m][n] = 1
                elif letter == '@':
                    list_map[m][n] = 2

        # Do some clever stuff with keys and doors
        for m, line in enumerate(list_map):
            for n, letter in enumerate(line):
                if isinstance(letter, str) and letter.lower() == letter:
                    # Have found a key
                    for p, _ in enumerate(list_map):
                        for q, _ in enumerate(list_map[p]):
                            if letter.upper() == list_map[p][q]:
                                list_map[m][n] = p + 1j*q

                    if list_map[m][n] == letter:
                        # No corresponding door
                        list_map[m][n] = 3

        # Make any remaining doors look like walls
        for m, line in enumerate(list_map):
            for n, letter in enumerate(line):
                if isinstance(letter, str) and letter.upper() == letter:
                    list_map[m][n] = 0

        self.map = np.array(list_map)