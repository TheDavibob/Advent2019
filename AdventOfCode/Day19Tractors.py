from IntcodeComputer import IntCode
import numpy as np

class TractorBeamRobot:
    def __init__(self, input_string):
        self.grid = np.array([])
        self.input_string = input_string
        self.computer = []
        self.grid_size = 1

    def set_grid_size(self, grid_size):
        self.grid_size = grid_size

    def fill_grid(self):
        # Reset grid
        self.grid = -1*np.ones([self.grid_size, self.grid_size])

        for idx_row in range(self.grid_size):
            for idx_column in range(self.grid_size):
                # Reset computer and provide inputs
                self.computer = IntCode(self.input_string)
                self.computer.inputs.append(idx_column)
                self.computer.inputs.append(idx_row)

                output = self.computer.process_until_output()
                self.grid[idx_row, idx_column] = output

    def expand_and_fill_grid(self, new_size):
        old_size = self.grid_size
        self.set_grid_size(new_size)
        new_grid = -1*np.ones([self.grid_size, self.grid_size])
        new_grid[:old_size, :old_size] = self.grid
        self.grid = new_grid
        self.grid[0,self.grid[0,:] == -1] = 0
        self.grid[self.grid[:, 0] == -1, 0] = 0
        for idx_row in range(1,self.grid_size):
            for idx_column in range(1,self.grid_size):
                if self.grid[idx_row, idx_column] == -1:
                    if self.grid[idx_row, idx_column - 1] == 0 and self.grid[idx_row - 1, idx_column] == 0:
                        self.grid[idx_row, idx_column] = 0
                    elif self.grid[idx_row, idx_column - 1] == 1 and self.grid[idx_row - 1, idx_column] == 1:
                        self.grid[idx_row, idx_column] = 1
                    else:
                        # Reset computer and provide inputs. This should only happen a handful of times for each row
                        print('Running for row {}, column {}'.format(idx_row, idx_column))
                        self.computer = IntCode(self.input_string)
                        self.computer.inputs.append(idx_column)
                        self.computer.inputs.append(idx_row)

                        output = self.computer.process_until_output()
                        self.grid[idx_row, idx_column] = output

