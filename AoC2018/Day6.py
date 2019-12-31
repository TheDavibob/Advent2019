import numpy as np
import CommonTools as ct
import matplotlib.pyplot as plt

class BadMapGoodMap:
    def __init__(self):
        self.coordinates = []
        self.map = []

    def import_coordinates(self, input_string):
        lines = ct.string_to_lines(input_string)
        listlines = [line.split(', ') for line in lines]
        self.coordinates = [tuple([int(letter) for letter in line]) for line in listlines]

    def initialize_grid(self):
        # Assumes coordinates have been imported
        x_list = [x for (x,y) in self.coordinates]
        y_list = [y for (x,y) in self.coordinates]
        x_max = max(x_list)
        y_max = max(y_list)

        self.map = np.zeros((y_max+10, x_max+10))

    def plot_coordinates(self):
        for n, coord in enumerate(self.coordinates):
            self.map[coord[::-1]] = n + 1

    def iterate_flood(self):
        height, width = self.map.shape
        temp_map = self.map.copy()
        for row_idx in range(height):
            for col_idx in range(width):
                if self.map[(row_idx, col_idx)] == 0:
                    # Determine adjacent values
                    if row_idx > 0:
                        up = self.map[(row_idx - 1, col_idx)]
                    else:
                        up = 0

                    if row_idx + 1 < height:
                        down = self.map[(row_idx + 1, col_idx)]
                    else:
                        down = 0

                    if col_idx > 0:
                        left = self.map[(row_idx, col_idx - 1)]
                    else:
                        left = 0

                    if col_idx + 1 < width:
                        right = self.map[(row_idx, col_idx + 1)]
                    else:
                        right = 0

                    adjacent_vals = list(set([int(up), int(down), int(left), int(right)]))
                    if len(adjacent_vals) == 1:
                        if 0 in adjacent_vals:
                            # Surrounded by zeros, skip
                            pass
                        else:
                            temp_map[(row_idx, col_idx)] = adjacent_vals[0]

                    elif len(adjacent_vals) == 2 and 0 in adjacent_vals:
                        temp_map[(row_idx, col_idx)] = next(x for x in adjacent_vals if x != 0)
                    else:
                        temp_map[row_idx, col_idx] = -1

        self.map = temp_map
        self.plot_flood_map()

    def run_flood_iterations(self):
        while np.any(self.map == 0):
            self.iterate_flood()

    def plot_flood_map(self):
        plt.imshow(self.map)
        plt.show()

    def find_edge_sets(self):
        top = set(self.map[0, :])
        bottom = set(self.map[-1, :])
        left = set(self.map[:, 0])
        right = set(self.map[:, -1])
        edge_sets = list(top.union(bottom).union(left).union(right))
        self.edge_sets = [int(x) for x in edge_sets]
        if -1 in self.edge_sets:
            self.edge_sets.remove(-1)

    def find_set_sizes(self):
        self.set_sizes = [0 for _ in self.coordinates]
        for idx in range(len(self.coordinates)):
            set_no = idx + 1
            self.set_sizes[idx] = np.sum(self.map == set_no)

    def find_set_sizes_exclude_edge(self):
        self.find_set_sizes()
        self.find_edge_sets()
        for set_no in self.edge_sets:
            self.set_sizes[set_no - 1] = 0

    def find_distance_to_all_coordinates(self, idx):
        # Finds distance from given index to all coordinates, and sums
        x, y = idx
        dist = [abs(x - c_x) + abs(y - c_y) for c_x, c_y in self.coordinates]
        return sum(dist)

    def make_distance_map(self):
        height, width = self.map.shape
        self.dist = np.zeros((height, width))
        for row_idx in range(height):
            for col_idx in range(width):
                self.dist[row_idx, col_idx] = self.find_distance_to_all_coordinates((row_idx, col_idx))

        plt.imshow(self.dist)
        plt.show()

    def distance_region_size(self, size):
        # Finds size of region with total distance to all points less than size
        self.make_distance_map()
        return np.sum(self.dist < size)


test_string = '''1, 1
1, 6
8, 3
3, 4
5, 5
8, 9'''
test = BadMapGoodMap()
test.import_coordinates(test_string)
test.initialize_grid()
test.plot_coordinates()
# test.run_flood_iterations()

