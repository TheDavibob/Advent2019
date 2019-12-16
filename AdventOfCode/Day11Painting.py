import numpy as np
import IntcodeComputer as ic

class PaintingRobot:
    def __init__(self, dim_grid = 5, start_pos = [2,2], start_dir = [-1,0]):
        # A note on coordinates: they are row/column, *not* x, y. Therefore, 'up' is -1, 0
        if isinstance(dim_grid, int):
            self.width = dim_grid
            self.height = dim_grid
        else:
            self.height = dim_grid[0]
            self.width = dim_grid[1]

        self.grid = np.zeros([self.height, self.width])
        #Black panels are 0s, white panels are 1s

        self.position = start_pos
        self.direction = start_dir

        self.clockwise = np.array([[0 , 1],
                               [-1, 0]])
        self.anticlock = np.array([[0 , -1],
                              [1, 0]])

        self.position_list = []

    def provide_color(self):
        # outputs 1 if white, 0 if black
        return self.grid[tuple(self.position)]

    def paint_square(self, output):
        self.grid[tuple(self.position)] = output
        # Store position
        position = list(self.position)
        if position not in self.position_list:
            self.position_list.append(position)

    def move_forward(self, output):
        # Update direction
        if output == 0:
            self.direction = np.dot(self.anticlock, self.direction)
        elif output == 1:
            self.direction = np.dot(self.clockwise, self.direction)
        else:
            raise Exception('Direction could not be understood: {}'.format(self.direction))
        self.position = self.position + self.direction


    def initialise_computer(self, codestring):
        self.computer = ic.IntCode(codestring)

    def input_to_output(self, input):
        # Takes an input, processes it, and waits for outputs
        self.computer.inputs.append(input)

        # Paint square
        output1 = self.computer.process_until_output()
        if self.computer.is_finished:
            return

        self.paint_square(output1)

        # Move
        output2 = self.computer.process_until_output()
        if self.computer.is_finished:
            return
        self.move_forward(output2)

    def process_until_complete(self, codestring, start_with_white = False):
        self.initialise_computer(codestring)

        if start_with_white:
            self.paint_square(1)

        while not self.computer.is_finished:
            input = self.provide_color()
            self.input_to_output(input)

        print('Painting complete')