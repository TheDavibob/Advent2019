import numpy as np
import matplotlib.pyplot as plt

class Maze:
    def __init__(self, map_string):
        self.map_string = map_string
        self.height = 0
        self.width = 0
        self.create_map_from_string()
        self.flood_map = []
        self.stacked_maps = []

    def surrounding_values(self, idx):
        idx1, idx2 = idx
        adjacent = [
            (idx1 + 1, idx2),
            (idx1 - 1, idx2),
            (idx1, idx2 + 1),
            (idx1, idx2 - 1),
        ]
        return [self.map[adj] for adj in adjacent], adjacent

    def create_map_from_string(self):
        lines = self.map_string.split('\n')
        self.height = len(lines)
        self.width = len(lines[0])

        self.map = np.zeros([self.height, self.width]).astype(complex)

        for row_idx, line in enumerate(lines):
            for col_idx, word in enumerate(line):
                if word == ' ' or word == '#':
                    self.map[row_idx, col_idx] = 0
                elif word == '.':
                    self.map[row_idx, col_idx] = 1
                else:
                    self.map[row_idx, col_idx] = ord(word)

        # The grid is now numeric, though portals are poorly handled
        for row_idx in range(1, self.height-1):
            for col_idx in range(1, self.width-1):
                current_val = self.map[row_idx, col_idx]
                if current_val > 1:
                    surrounding, adjacent = self.surrounding_values((row_idx, col_idx))
                    if surrounding[0] == 1:
                        # Cell beneath is open
                        update_value = surrounding[1] + 1j*current_val
                        wipe_idx = adjacent[1]
                    elif surrounding[1] == 1:
                        # Cell above is open
                        update_value = current_val + 1j*surrounding[0]
                        wipe_idx = adjacent[0]
                    elif surrounding[2] == 1:
                        # Cell to the right is open
                        update_value = surrounding[3] + 1j*current_val
                        wipe_idx = adjacent[3]
                    elif surrounding[3] == 1:
                        # Cell to the left is open
                        update_value = current_val + 1j*surrounding[2]
                        wipe_idx = adjacent[2]
                    else:
                        # This is not a portal - don't change anything
                        update_value = current_val
                        wipe_idx = (0,0)

                    self.map[row_idx, col_idx] = update_value
                    self.map[wipe_idx] = 0


    def flood_and_jump(self, idx):
        # We now flood the map, jumping through portals when relevant
        # This is done from any single given index
        self.flood_map = -(self.map != 0).astype(int)
        # This is -1 for open spaces and portals.
        self.flood_map[idx] = 1
        # Note, as usual, counting from 1. This will make everything a single space too big

        if self.map[idx].imag != 0:
            portal_idxs = (self.map == self.map[idx])
            unmarked_idxs = (self.flood_map == -1)
            other_portal = np.where(np.logical_and(portal_idxs, unmarked_idxs))
            if len(other_portal[0]) > 0:
                portal_idx = (other_portal[0], other_portal[1])
                self.flood_map[portal_idx] = 1
                _, adjacent_portal = self.surrounding_values(portal_idx)
                for adj_port in adjacent_portal:
                    if self.flood_map[adj_port] == -1:
                        self.flood_map[adj_port] = 1

        n = 1

        while (not np.any(self.flood_map) == -1) and np.max(self.flood_map) == n:
            for row_idx in range(1,self.height - 1):
                for col_idx in range(1, self.width - 1):
                    if self.flood_map[row_idx, col_idx] == n:
                        _, adjacent = self.surrounding_values((row_idx, col_idx))
                        for adj in adjacent:
                            if self.flood_map[adj] == -1:
                                self.flood_map[adj] = n+1
                                if self.map[adj].imag != 0:
                                    # This is a portal
                                    # Find corresponding portals
                                    portal_idxs = (self.map == self.map[adj])
                                    unmarked_idxs = (self.flood_map == -1)
                                    other_portal = np.where(np.logical_and(portal_idxs, unmarked_idxs))
                                    if len(other_portal[0]) > 0:
                                        portal_idx = (other_portal[0], other_portal[1])
                                        self.flood_map[portal_idx] = n+1
                                        _, adjacent_portal = self.surrounding_values(portal_idx)
                                        for adj_port in adjacent_portal:
                                            if self.flood_map[adj_port] == -1:
                                                self.flood_map[adj_port] = n+1

            n += 1

    def find_distances(self, idx, idx_list):
        self.flood_and_jump(idx)
        return [self.flood_map[destination] - 1 for destination in idx_list]

    def plot_flood_map(self):
        # Static function, getting lazy
        plt.imshow(self.flood_map)
        plt.show()

    def distance_first_to_last(self):
        # Distance from AA (65+65i) to ZZ (90+90i)
        AA = np.where(self.map == 65+65j)
        ZZ = np.where(self.map == 90+90j)
        idx_AA = (AA[0][0],AA[1][0])
        idx_ZZ = (ZZ[0][0],ZZ[1][0])

        return self.find_distances(idx_AA, [idx_ZZ])[0] - 2

    def distance_first_to_last_stacked(self):
        # Distance from AA (65+65i) to ZZ (90+90i)
        AA = np.where(self.map == 65+65j)
        ZZ = np.where(self.map == 90+90j)
        idx_AA = (AA[0][0],AA[1][0])
        idx_ZZ = (ZZ[0][0],ZZ[1][0])

        self.stacked_flood_and_jump(idx_AA, destination_idx=idx_ZZ, to_print=True)

        # One off for each end point, extra for the extra dist
        return self.stacked_maps[idx_ZZ + (0,)] - 3

    def stacked_flood_and_jump(self, idx, cap=0, destination_idx=[], to_print=False):
        # For the second part of the problem, we need *stacked* flood maps, which might get bigger
        self.flood_map = -(self.map != 0).astype(int)
        rows, cols = self.flood_map.shape
        self.stacked_maps = np.zeros((rows, cols, 1))
        self.stacked_maps[:,:,0] = self.flood_map

        idx = idx + (0,)
        # Fill this as before, except when going through an *inner* portal, add a layer and move up
        self.stacked_maps[idx] = 1

        # Fortunately, don't need the annoying first portal bollocks
        n = 1

        while (not np.any(self.stacked_maps[:,:,0]) == -1) and np.max(self.stacked_maps) == n:
            num_layers = self.stacked_maps.shape[2]
            if cap != 0 and cap == num_layers:
                break
            if len(destination_idx) > 0:
                if self.stacked_maps[destination_idx + (0,)] != -1:
                    break
            for layer in range(num_layers):
                for row_idx in range(1,self.height - 1):
                    for col_idx in range(1, self.width - 1):
                        if self.stacked_maps[row_idx, col_idx, layer] == n:
                            _, adjacent = self.surrounding_values((row_idx, col_idx))
                            for adj in adjacent:
                                adj_ext = adj + (layer,)
                                if self.stacked_maps[adj_ext] == -1:
                                    self.stacked_maps[adj_ext] = n+1
                                    if self.map[adj].imag != 0:
                                        # This is a portal
                                        if adj[0] == 1 or adj[0] == self.height - 2 or adj[1] == 1 or adj[1] == self.width -2:
                                            new_layer = layer - 1
                                            if new_layer < 0:
                                                continue
                                        else:
                                            # New layer above, might need more works
                                            new_layer = layer + 1
                                            if new_layer >= self.stacked_maps.shape[2]:
                                                # Create new layer
                                                new_grid = np.zeros((self.height, self.width, num_layers + 1))
                                                new_grid[:,:,:-1] = self.stacked_maps
                                                new_grid[:,:,-1] = -(self.map != 0).astype(int)
                                                self.stacked_maps = new_grid

                                        # Find corresponding portals
                                        portal_idxs = (self.map == self.map[adj])
                                        portal_idxs[adj] = False
                                        unmarked_idxs = (self.stacked_maps[:,:,new_layer] == -1)
                                        other_portal = np.where(np.logical_and(portal_idxs, unmarked_idxs))
                                        if len(other_portal[0]) > 0:
                                            portal_idx = (other_portal[0][0], other_portal[1][0])
                                            self.stacked_maps[portal_idx + (new_layer,)] = n+1
                                            _, adjacent_portal = self.surrounding_values(portal_idx)
                                            for adj_port in adjacent_portal:
                                                if self.stacked_maps[adj_port + (new_layer,)] == -1:
                                                    self.stacked_maps[adj_port + (new_layer,)] = n+1

            n += 1
            if to_print:
                print(n)