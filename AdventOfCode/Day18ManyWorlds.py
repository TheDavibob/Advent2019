import numpy as np
import matplotlib.pyplot as plt
import copy

class TheVault:
    def __init__(self):
        self.map = np.array([])
        self.map2 = np.array([])
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

    def plot_walls(self):
        logical_map = (self.map != 0)
        plt.imshow(logical_map)
        plt.show()

    def plot_walls_and_keys(self):
        logical_map = (self.map != 0)
        key_map = (self.map != 0) * (self.map != 1) * (self.map != 2)
        location_map = (self.map == 2)
        plt.imshow(key_map.astype(int) + logical_map.astype(int) + 2*location_map)
        plt.show()

    def plot_flood_block(self, *args):
        self.flood_block(*args)
        plt.imshow(self.flood_map)
        plt.show()

    def plot_flood_block_and_keys(self, *args):
        self.flood_block(*args)
        key_map = (self.map != 0) * (self.map != 1) * (self.map != 2)
        plt.imshow(self.flood_map*key_map)
        plt.show()

    def flood_block(self, reset=True, *args):
        if len(args) == 1:
            current_idx = args[0]
        else:
            current_idx = self.get_current_position()
        if reset:
            # reset rewrites the flood map every time. We don't necessarily want this
            self.flood_map = (self.map != 0).astype(int) - 1
            self.flood_map[current_idx] = 1
        is_finished = False
        n = 1
        while not is_finished:
            if n >= np.max(self.flood_map):
                is_finished = True
            i, j = np.where(self.flood_map == n)
            for idx1, idx2 in zip(i,j):
                adjacent = [
                            (idx1 + 1, idx2),
                            (idx1 - 1, idx2),
                            (idx1, idx2 + 1),
                            (idx1, idx2 - 1)
                            ]
                for cell in adjacent:
                    if self.flood_map[cell] == 0:
                        self.flood_map[cell] = n+1
                        is_finished = False

            n += 1

    def find_all_keys(self, final_key=False):
        if final_key:
            keys = np.logical_or(self.map.imag != 0, self.map == 3)
        else:
            keys = self.map.imag != 0

        return np.where(keys)

    def find_keys(self, final_key=False, reset=True, *args):
        # Finds all accessible keys, returns distance and index
        self.flood_block(*args, reset=reset)

        # Find array of keys
        if final_key:
            keys = np.logical_or(self.map.imag != 0, self.map == 3)
        else:
            keys = self.map.imag != 0

        # Find array of local block
        block = (self.flood_map > 0)

        # Find intersection
        valid_keys = (keys*block)

        key_idx = np.where(valid_keys)
        key_distance = self.flood_map[key_idx]

        return key_idx, key_distance

    def find_doors(self):
        self.assign_doors()
        door_idxs = np.where(self.map2.real < 0)
        return [(door_idxs[0][n], door_idxs[1][n]) for n, _ in enumerate(door_idxs[0])]

    def get_current_position(self):
        # Returns the index of the location of the agent
        return np.where(self.map == 2)

    def pick_up_key(self, key_idx):
        # moves user to key, picks it up, opens door (if relevant)
        # key_idx a tuple, (row, column)

        key = self.map[key_idx].copy()
        if key.imag == 0 and key != 3:
            print('This is not a key')
            return

        agent_idx = self.get_current_position()
        self.map[agent_idx] = 1
        self.map[key_idx] = 2

        if key == 3:
            # This should always be the last key to be picked up
            return

        # key is a complex number
        self.map[int(key.real), int(key.imag)] = 1

    def process_until_multiple_keys(self):
        while True:
            keys, distances = self.find_keys(final_key=True)
            if len(keys[0]) == 0:
                # No keys found on block. Check whether all keys in total have been found
                if len(self.find_all_keys(final_key=True)[0]) == 0:
                    # print('No more keys to be found. Travelled {} steps'.format(self.distance_travelled))
                    return 'route_successful'
                else:
                    print('Not all keys found with this route')
                    return 'route_failed'

            elif len(keys[0]) > 1:
                # print('Multiple keys found, stopping')
                return len(keys[0])

            self.pick_up_key(keys)
            self.distance_travelled += int(distances - 1)

    def assign_doors(self):
        # This soups up the map to actually include doors
        # Doors are negative complex numbers, refering back to the location of the key
        self.map2 = self.map.copy()
        key_idxs = self.find_all_keys(final_key=False)
        for n, _ in enumerate(key_idxs[0]):
            key = self.map[key_idxs[0][n], key_idxs[1][n]]
            self.map2[int(key.real), int(key.imag)] = -key_idxs[0][n] - 1j*key_idxs[1][n] # This gives a link between the key and the wall, and vice versa

    def flood_blocks_through_door(self):
        # Find all keys
        all_keys_np = self.find_all_keys()
        all_keys_idxs = [(all_keys_np[0][n], all_keys_np[1][n]) for n, _ in enumerate(all_keys_np[0])]

        keys_idx_np, distances = self.find_keys(reset=True)

        # Converts this to a bunch of useful things
        keys_idxs = [(keys_idx_np[0][n], keys_idx_np[1][n]) for n, _ in enumerate(keys_idx_np[0])]

        while len(keys_idxs) < len(all_keys_idxs):
            # Finds all visible keys
            keys_idx_np, distances = self.find_keys(reset=False)

            # Converts this to a bunch of useful things
            new_keys_idxs = [(keys_idx_np[0][n], keys_idx_np[1][n]) for n, _ in enumerate(keys_idx_np[0])]
            keys_idxs = keys_idxs + [key for key in new_keys_idxs if key not in keys_idxs]

            # List of doors than can currently be opened
            key_unlock = [(int(self.map[key].real), int(self.map[key].imag)) for key in keys_idxs]
            for n, door in enumerate(key_unlock):
                if self.flood_map[door] == -1:
                    # Distance to door: distance to key, distance from key to door
                    distance_to_key = distances[n]

                    # Find the square next to the door closest to the source
                    idx1, idx2 = door
                    adjacent = [
                        (idx1 + 1, idx2),
                        (idx1 - 1, idx2),
                        (idx1, idx2 + 1),
                        (idx1, idx2 - 1)
                    ]
                    surrounding_floods = [self.flood_map[position] for position in adjacent]
                    good_values = [i for i in surrounding_floods if i > 0]
                    if len(good_values) > 0:
                        best_case = min(i for i in surrounding_floods if i > 0)
                        adj_idx = next(n for n, i in enumerate(adjacent) if surrounding_floods[n] == best_case)
                        idx_door = adjacent[adj_idx]

                        # Find the path from this point to the source, and the path from the key to the doro
                        distance_to_door = self.estimate_distance(idx_door, keys_idxs[n])
                        self.flood_map[door] = distance_to_key + distance_to_door + 1

            self.flood_block(reset=False)

    def trace_path_to_source(self, idx):
        # Traces the path to the 'centre' of the floodmap from some idx
        if self.flood_map[idx] <= 0:
            return

        history = [idx]
        distance = [self.flood_map[idx]]
        while distance[-1] > 1:
            idx1, idx2 = idx
            adjacent = [
                (idx1 + 1, idx2),
                (idx1 - 1, idx2),
                (idx1, idx2 + 1),
                (idx1, idx2 - 1)
            ]
            surrounding_floods = [self.flood_map[position] for position in adjacent]
            best_case = min(i for i in surrounding_floods if i > 0)
            adj_idx = next(n for n, i in enumerate(adjacent) if surrounding_floods[n] == best_case)
            idx = adjacent[adj_idx]
            history.append(idx)
            distance.append(self.flood_map[idx])

        return history, distance

    def estimate_distance(self, idx1, idx2):
        # Estimates the distance between two points via magic
        hist1, dist1 = self.trace_path_to_source(idx1)
        hist2, dist2 = self.trace_path_to_source(idx2)

        first_link = next(i for i in hist2 if i in hist1)
        idx1 = next(n for n, i in enumerate(hist1) if i == first_link)
        idx2 = next(n for n, i in enumerate(hist2) if i == first_link)

        tot_dist1 = dist1[0] - dist1[idx1]
        tot_dist2 = dist2[0] - dist2[idx2]
        return tot_dist1 + tot_dist2

    def distance_to_all_keys(self):
        # Flood map of total grid, taking into account doors
        self.flood_blocks_through_door()

        # Find all keys
        all_keys_np = self.find_all_keys(final_key=True)

        # Determine distance to all keys via the new floodmap
        all_keys = [(all_keys_np[0][n], all_keys_np[1][n]) for n, _ in enumerate(all_keys_np[0])]
        distances = [self.flood_map[key] for key in all_keys]

        return all_keys, distances

    def modified_dijkstra(self):
        current_position_np = self.get_current_position()
        current_position = (int(current_position_np[0]), int(current_position_np[1]))
        all_keys, starting_distances = self.distance_to_all_keys()

        nodes = [current_position_np] + all_keys

        labels = np.array([0 for key in nodes])
        labels[0] = 1

        distances = np.array([0 for key in nodes])
        distances[1:] = starting_distances

        ## TO BE FINISHED
        # Idea: for each node, have a minimum path to this node, and a resulting collection of keys which should be stored

        while not all(labels):
            current_distances = distances.copy()
            current_distances[labels == 1] = np.inf

            move_to = np.argmin(current_distances)
            labels[move_to] = 1

            # Find the node with the minimum distance that has not been visited





class BranchCollection:
    def __init__(self, map_string):
        self.branches = [] # This contains a historical record at any branching points
        self.branch_status = [] # '-1' if does not work, '0' if unfinished, otherwise the length of the branch
        self.next_key = [] # -1 if branch already done, index of which key to use otherwise
        self.map_string = map_string
        self.branch_distance = []

    def process_first_branch(self):
        test_branch = TheVault()
        test_branch.create_map_from_string(self.map_string)

        # Check if there are multiple keys to pick up, even off the start
        keys, distances = test_branch.find_keys(final_key=True)
        for idx in range(len(keys[0])):
            self.next_key.append(idx)
            self.branches.append(TheVault())
            self.branches[-1].create_map_from_string(self.map_string)
            self.branch_status.append(0)
            self.branch_distance.append(0)

    def process_next_branch(self, plot_map = False):
        # Finds first unfinished branch
        branch_idx = next(n for n, branch_stat in enumerate(self.branch_status) if branch_stat == 0)
        branch = self.branches[branch_idx]

        if plot_map:
            branch.plot_walls_and_keys()

        key_idx = self.next_key[branch_idx]

        keys, distances = branch.find_keys(final_key=True)
        key_to_use = (keys[0][key_idx], keys[1][key_idx])
        branch.pick_up_key(key_to_use)
        branch.distance_travelled += int(distances[key_idx] - 1)

        # Proceed until next branch
        message = branch.process_until_multiple_keys()

        if message == 'route_successful':
            self.branch_status[branch_idx] = branch.distance_travelled
        elif message == 'route_failed':
            self.branch_status[branch_idx] = -1
        else:
            # Branch status stays 0
            self.next_key[branch_idx] = 0
            self.branch_distance[branch_idx] = branch.distance_travelled
            # Create lots of new branches
            for idx in range(1,message):
                self.branches.append(copy.deepcopy(branch))
                self.next_key.append(idx)
                self.branch_status.append(0)
                self.branch_status[branch_idx] = branch.distance_travelled

    def investigate_all_branches(self):
        self.process_first_branch()
        min_so_far = []
        while len([branch for branch in self.branch_status if branch == 0]) > 0:
            self.process_next_branch(plot_map=True)
            valid_distances = [branch for branch in self.branch_status if branch > 0]
            if len(valid_distances) > 0:
                if not isinstance(min_so_far, int):
                    min_so_far = min(valid_distances)
                    print(min_so_far)
                elif min(valid_distances) < min_so_far:
                    min_so_far = min(valid_distances)
                    print(min_so_far)

        return min([branch for branch in self.branch_status if branch > 0])


