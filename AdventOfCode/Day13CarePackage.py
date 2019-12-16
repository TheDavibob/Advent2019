import numpy as np
import IntcodeComputer as ic
import matplotlib.pyplot as plt

class ArcadeGame:
    def __init__(self, codestring):
        # Initialises the grid, which will be extended as and when it is required
        self.grid = np.zeros([1,1])
        self.computer = ic.IntCode(codestring)
        self.score = 0

        self.ball_traj = []
        self.ball_traj_y = []
        self.paddle_traj = []


    def paint_tile(self, output1, output2, output3):
        # First up, extend grid to the size we actually want
        max_y, max_x = self.grid.shape
        if output1 >= max_x:
            max_x = output1 + 1

        if output2 >= max_y:
            max_y = output2 + 1

        grid = np.zeros([max_y, max_x])
        grid[:self.grid.shape[0], :self.grid.shape[1]] = self.grid
        self.grid = grid

        self.grid[output2, output1] = output3

    def paint_full_grid(self):
        while not self.computer.is_finished:


            # Extract the relevant outputs
            output1 = self.computer.process_until_output()
            if self.computer.is_finished:
                break

            output2 = self.computer.process_until_output()
            output3 = self.computer.process_until_output()

            self.paint_tile(output1, output2, output3)

            plt.imshow(self.grid)
            plt.show()

    def set_score(self, output3):
        self.score = output3
        print('Current score: {}'.format(self.score))

    def paint_and_play(self):
        while not self.computer.is_finished:
            # Follow the ball

            if self.computer.input_pointer >= len(self.computer.inputs):
                self.computer.inputs.append(0)

            if isinstance(self.get_ball_x(), int) and isinstance(self.get_paddle(), int):
                # This always updates the final input call, even if it's already been set
                self.ball_traj.append(self.get_ball_x())
                self.ball_traj_y.append(self.get_ball_y())
                self.paddle_traj.append(self.get_paddle())

                print('Ball at ({}, {}), paddle at ({},{})'.format(
                    self.get_ball_x(),
                    self.get_ball_y(),
                    self.get_paddle(),
                    20) )

                # One step behind is fine, so if ball left or right of ball move towards it, otherwise stay still
                if self.paddle_traj[-1] < self.ball_traj[-1]:
                    self.computer.inputs[-1] = 1
                    print('Moving right')
                elif self.paddle_traj[-1] > self.ball_traj[-1]:
                    self.computer.inputs[-1] = -1
                    print('Moving left')
                else:
                    self.computer.inputs[-1] = 0
                    print('Not moving')

            # if isinstance(self.get_ball_x(), int) and isinstance(self.get_paddle(), int):
            #     if not isistance
            #     plt.close('all')
            #     plt.imshow(self.grid)
            #     plt.show(block=True)
            #     plt.pause(0.1)


            # Extract the relevant outputs
            output1 = self.computer.process_until_output()
            if self.computer.is_finished:
                break

            output2 = self.computer.process_until_output()
            output3 = self.computer.process_until_output()

            if output1 == -1 and output2 == 0:
                self.set_score(output3)
            else:
                self.paint_tile(output1, output2, output3)

        print('Final score: {}'.format(self.score))

    def get_paddle(self):
        try:
            return int(np.where(self.grid == 3)[1])
        except TypeError:
            return []

    def get_ball_x(self):
        try:
            return int(np.where(self.grid == 4)[1])
        except TypeError:
            return []

    def get_ball_y(self):
        try:
            return int(np.where(self.grid == 4)[0])
        except TypeError:
            return []