import numpy as np

def import_puzzle_input(numstring):
    return [int(x) for x in numstring.split()]

class RecursiveTree:
    def __init__(self, numstring):
        self.code = import_puzzle_input(numstring)
        self.map = -np.ones((1, len(self.code)))

        self.level_counter = 0
        self.index = 0
        self.next_assignment = 1

        self.children_dict = {}
        self.value = []

    def return_pointer(self):
        self.level_counter -= 1
        current_val = self.map[self.level_counter, self.index]
        while self.level_counter >= 0 and self.map[self.level_counter, self.index-1] == current_val:
            self.index -= 1

    def drop_pointer(self):
        current_val = self.map[self.level_counter, self.index]
        while self.map[self.level_counter, self.index] == current_val:
            self.index += 1

        self.level_counter += 1

        if self.level_counter == self.map.shape[0]:
            # Add new row
            new_row = (self.map[-1, :] >= 0) - 1
            self.map = np.vstack([self.map, new_row])

    def count_children(self):
        if self.level_counter + 1 == self.map.shape[0]:
            return 0
        # Counts currently determined children on the level beneath the current pointer
        mask = self.map[self.level_counter, :] == self.map[self.level_counter, self.index]
        values_beneath = set(self.map[self.level_counter+1, mask])
        return len(values_beneath) - 1
        # This will always, if correctly initiated, contain 0, which can be ignored

    def assign_all_in_column(self):
        # Finds the furthest extent of values that are not -1
        furthest_idx = max(np.where(self.map != -1)[1])
        minus_idxs = np.where(self.map == -1)[1]
        if len(minus_idxs) == 0:
            return
        nearest_idx = min(np.where(self.map == -1)[1])

        for row_idx in range(self.map.shape[0]):
            for column_idx in range(nearest_idx,furthest_idx + 1):
                if self.map[row_idx, column_idx] == -1:
                    self.map[row_idx, column_idx] = self.map[row_idx, column_idx-1]

    def assign_header(self):
        # assign spaces for header
        self.map[self.level_counter, self.index:self.index+2] = self.next_assignment
        self.next_assignment += 1
        self.assign_all_in_column()

    def assign_metadata(self, n_metadata):
        # Find last value assigned to this node
        new_pointer = self.index
        current_val = self.map[self.level_counter, self.index]
        while new_pointer < self.map.shape[1] and self.map[self.level_counter, new_pointer] == current_val:
            new_pointer += 1

        self.map[self.level_counter, new_pointer:new_pointer+n_metadata] = current_val
        self.map[self.level_counter+1:, new_pointer:new_pointer+n_metadata] = 0
        self.assign_all_in_column()

        self.return_pointer()

    def step(self):
        if not np.any(self.map == -1):
            return True   # finished

        if self.map[self.level_counter, self.index] == -1:
            self.assign_header()
            return False

        num_children = self.code[self.index]
        created_children = self.count_children()

        if created_children == num_children:
            self.assign_metadata(self.code[self.index + 1])
        else:
            self.drop_pointer()

        return False

    def process(self):
        is_finished = False
        while not is_finished:
            is_finished = self.step()

    def extract_metadata(self, node):
        # Given a node index, extracts the relevant metadata
        indexes = np.where(self.map == node)
        num_metadata = self.code[indexes[1][1]]
        metadata = [self.code[x] for x in indexes[1][-num_metadata:]]
        return metadata

    def sum_all_metadata(self):
        sum_metadata = 0
        for node in range(1,int(np.max(self.map) + 1)):
            metadata = self.extract_metadata(node)
            sum_metadata += sum(metadata)

        return sum_metadata

    def find_children(self, node):
        mask = self.map == node
        mask[1:, :] = mask[:-1, :]
        mask[0, :] = False
        children = list(set(self.map[mask]))
        if 0 in children:
            children.remove(0)

        children.sort()

        return [int(child) for child in children]

    def create_child_dictionary(self):
        for node in range(1, int(np.max(self.map) + 1)):
            self.children_dict[node] = self.find_children(node)

    def assign_value(self):
        self.value = int(np.max(self.map))*[-1]
        # This is off-indexed, so watch out

        self.create_child_dictionary()

        # Assign value to all childfree nodes
        childfree_nodes = [node for node, children in self.children_dict.items() if len(children) == 0]
        for node in childfree_nodes:
            metadata = self.extract_metadata(node)
            self.value[node - 1] = sum(metadata)

        nodes_with_children = [node for node, children in self.children_dict.items() if len(children) > 0]
        nodes_with_children.reverse()

        for node in nodes_with_children:
            metadata = self.extract_metadata(node)
            children = self.children_dict[node]

            value = 0
            for meta in metadata:
                if meta > len(children):
                    pass
                else:
                    value += self.value[children[meta - 1] - 1]

            self.value[node - 1] = value


