import numpy as np

class OneDMoonSystem:
    def __init__(self, init_positions):
        # init_x should have length 4
        self.initial_positions = np.array(init_positions)
        self.initial_velocities = np.array(np.array([0, 0, 0, 0]))
        self.positions = self.initial_positions.copy()
        self.velocities = self.initial_velocities.copy()
        self.index = 0

    def step(self):
        self.index += 1
        grid = np.meshgrid(self.positions, self.positions)
        added_velocity = np.sum(grid[0] > grid[1], axis=1) - np.sum(grid[1] > grid[0], axis=1)
        self.velocities += added_velocity
        self.positions += self.velocities

    def step_until_repeat(self):
        while True:
            self.step()
            if np.all(self.positions == self.initial_positions) and np.all(self.velocities == self.initial_velocities):
                break

        print('{} steps until completion'.format(self.index))
        return self.index

# input:
x = [6, -6, -9, -3]
y = [-2, -7, 11, -4]
z = [-7, -4, 0, 6]
cycle = []

for coord in (x,y,z):
    test = OneDMoonSystem(coord)
    cycle.append(test.step_until_repeat())

print(np.lcm(cycle[0], np.lcm(cycle[1],cycle[2])))