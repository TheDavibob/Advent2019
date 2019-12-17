import IntcodeComputer as ic
import matplotlib.pyplot as plt
import copy

intcode = '3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,101,0,1034,1039,101,0,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1105,1,124,102,1,1034,1039,101,0,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,1002,1035,1,1040,1002,1038,1,1043,1001,1037,0,1042,1105,1,124,1001,1034,1,1039,1008,1036,0,1041,1002,1035,1,1040,101,0,1038,1043,101,0,1037,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,35,1032,1006,1032,165,1008,1040,33,1032,1006,1032,165,1102,2,1,1044,1106,0,224,2,1041,1043,1032,1006,1032,179,1101,1,0,1044,1106,0,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,27,1044,1105,1,224,1101,0,0,1044,1105,1,224,1006,1044,247,101,0,1039,1034,1002,1040,1,1035,101,0,1041,1036,1001,1043,0,1038,101,0,1042,1037,4,1044,1106,0,0,8,86,20,11,8,18,84,20,96,25,15,28,96,20,74,24,7,5,77,6,77,6,23,74,3,23,93,21,72,23,1,57,87,10,17,9,23,48,16,9,32,11,62,73,5,70,2,10,77,23,16,76,24,28,13,46,92,26,15,10,87,13,28,54,10,50,4,16,47,75,24,55,4,99,92,17,66,24,7,13,33,43,21,65,24,4,74,40,8,28,25,5,72,25,5,54,19,72,6,44,49,3,65,11,24,85,39,11,5,77,15,6,65,12,66,66,14,8,88,81,2,8,99,7,54,70,2,97,69,9,17,51,47,1,56,88,81,41,10,98,16,23,35,24,82,24,5,99,39,67,8,14,46,56,5,8,59,9,53,9,21,95,6,95,7,12,85,26,79,82,19,21,62,99,5,13,81,19,31,15,29,67,45,22,75,84,14,25,83,33,97,4,85,15,17,25,21,51,55,11,76,32,15,43,60,13,13,11,65,65,16,9,96,26,17,10,94,23,12,37,16,49,2,81,17,11,20,17,16,37,87,16,12,96,23,10,68,22,75,34,4,22,14,34,14,62,8,34,12,72,7,40,5,54,10,89,7,96,1,14,72,7,11,60,93,68,51,21,86,25,34,26,20,38,7,21,94,78,10,8,46,4,81,12,84,30,11,9,48,12,83,73,42,83,26,26,40,22,91,6,38,99,2,40,24,93,10,22,84,22,19,94,8,6,42,33,11,15,31,66,33,2,65,39,67,26,5,67,19,86,1,12,20,28,54,80,84,3,17,32,26,51,8,6,20,67,15,54,30,5,31,97,9,10,29,18,45,8,23,69,18,61,11,4,73,5,46,13,96,16,80,66,17,1,11,50,37,4,34,94,15,32,77,5,93,69,12,66,6,24,18,84,26,42,5,78,74,22,82,15,23,60,11,64,61,59,48,11,99,49,3,68,2,16,14,99,7,94,9,22,75,20,30,21,17,91,20,41,21,26,42,44,19,18,85,17,96,21,2,88,62,69,8,39,3,11,62,12,25,29,69,79,52,56,6,52,22,78,42,8,18,22,59,91,13,94,89,10,16,73,11,17,80,81,26,36,26,55,16,13,30,6,6,43,1,43,83,21,69,11,42,8,77,21,31,25,24,99,26,56,85,15,74,1,88,13,3,18,42,14,54,13,6,91,49,7,36,42,2,8,67,55,14,35,5,33,6,96,24,94,24,59,46,18,4,61,95,2,33,33,2,31,24,97,1,91,15,52,15,53,44,10,20,47,93,8,1,48,80,22,80,23,15,92,18,18,59,19,69,17,8,55,38,26,9,68,23,85,2,12,23,77,4,21,16,6,90,45,17,61,16,28,22,24,58,30,26,2,85,1,53,29,18,37,30,38,4,12,92,60,19,13,56,19,85,7,66,19,73,39,9,90,81,3,8,9,72,25,37,24,5,96,25,13,81,92,34,19,95,3,26,36,25,25,25,15,95,6,35,43,92,10,79,70,8,30,18,96,75,1,5,76,17,86,3,46,22,11,50,96,1,56,43,2,23,53,7,71,20,61,73,34,31,57,24,69,4,24,6,25,98,50,21,63,12,97,11,9,72,19,40,21,7,2,18,77,83,16,1,82,24,25,57,72,25,9,15,76,21,14,71,16,94,7,64,21,69,87,18,65,1,21,20,61,91,10,86,7,55,36,1,40,99,39,8,41,5,92,76,33,20,40,15,81,76,48,5,35,64,59,6,30,13,52,19,84,21,58,1,89,29,53,10,76,22,33,26,65,3,96,0,0,21,21,1,10,1,0,0,0,0,0,0'

class OxygenSystem:
    def __init__(self, intcode):
        self.positions = [0]  # Initialise with a single position, which we know is fine and takes zero steps
        self.status = [0]
        self.current_position_idx = 0  # Index of current robot position
        self.computer = ic.IntCode(intcode)
        self.computer_history = [copy.deepcopy(self.computer)]
        self.ox_location = []
        self.ox_idx = []

        self.flood_map = self.status

    def get_current_position(self):
        return self.positions[self.current_position_idx], self.status[self.current_position_idx]

    def movement_command(self, command):
        # This command is rejected if a space has already been visited
        current_position, current_status = self.get_current_position()
        if command == 1:
            new_position = current_position + 1j
        elif command == 2:
            new_position = current_position - 1j
        elif command == 3:
            new_position = current_position - 1
        elif command == 4:
            new_position = current_position + 1
        else:
            error_message = ('Command not understood', command)
            return error_message

        if new_position in self.positions:
            error_message = ('Space already visited', new_position)
            return error_message

        # Add new position to position list
        self.positions.append(new_position)

        # Pass input to computer
        self.computer.inputs.append(command)

        # Run computer until output
        output = self.computer.process_until_output()
        if output == 0:
            # Hit a wall. Do not update position
            position_value = -1
        elif output == 1:
            position_value = current_status + 1
            self.current_position_idx = len(self.positions) - 1
        elif output == 2:
            # Treat as the same
            position_value = current_status + 1
            self.current_position_idx = len(self.positions) - 1
            self.ox_location = new_position
            self.ox_idx = self.current_position_idx
        else:
            error_message = ('Output not understood', output)
            return error_message

        self.status.append(position_value)
        self.store_computer()

        error_message = ('Success', output)
        return error_message

    def try_all_movements(self):
        # Tries all possible movements
        for command in [1,2,3,4]:
            error_message = self.movement_command(command)
            if error_message[0] == 'Success':
                if error_message[1] == 1:
                    # print('Moved with command {}'.format(command))
                    return 'success'
                elif error_message[1] == 2:
                    print('Moved to oxygen system with command {}'.format(command))
                    return 'finished'

        return 'stuck'

    def store_computer(self):
        self.computer_history.append(copy.deepcopy(self.computer))

    def plot_grid(self):
        real_parts = [complex(position).real for position in self.positions]
        imag_parts = [complex(position).imag for position in self.positions]
        plt.scatter(real_parts, imag_parts, c=self.status)
        plt.show()

    def plot_flood(self):
        real_parts = [complex(position).real for position in self.positions]
        imag_parts = [complex(position).imag for position in self.positions]
        plt.scatter(real_parts, imag_parts, c=self.flood_map)
        plt.show()

    def plot_grid_2(self):
        real_parts = [complex(position).real for position in self.positions]
        imag_parts = [complex(position).imag for position in self.positions]
        colors = [statuses > -1 for statuses in self.status]
        plt.scatter(real_parts, imag_parts, c=colors)
        plt.show()

    def plot_grid_3(self):
        real_parts = [complex(position).real for position in self.positions]
        imag_parts = [complex(position).imag for position in self.positions]
        colors = [statuses > -1 for statuses in self.status]
        colors[self.ox_idx] = 2
        plt.scatter(real_parts, imag_parts, c=colors)
        plt.show()

    def run_until_stuck(self):
        status = 'go'
        while status != 'stuck' and status != 'finished':
            status = self.try_all_movements()
        return status

    def find_unsurrounded_location(self):
        # Finds the first location that has not been surrounded by other points, and returns to that location
        for n, position in enumerate(self.positions):
            if self.status[n] != -1:
                points = [position + 1, position - 1, position + 1j,position - 1j]
                if len([point for point in points if point not in self.positions]) != 0:
                    self.current_position_idx = n
                    return 'found'

        return 'notfound'

    def exhaustive_search(self):
        status = 'start'
        while status != 'finished':
            error_message = self.find_unsurrounded_location()
            if error_message == 'notfound':
                self.plot_grid_2()
                print('Gone bad again')
                return

            # Reset computer to the state it was at at that point
            self.computer = copy.deepcopy(self.computer_history[self.current_position_idx])

            status = self.run_until_stuck()

        self.plot_grid_2()
        return self.get_current_position()


    def complete_map(self):
        status = 'finding'
        while status != 'notfound':
            status = self.find_unsurrounded_location()
            self.computer = copy.deepcopy(self.computer_history[self.current_position_idx])
            runner = self.run_until_stuck()

        self.plot_grid_3()

    def flood_the_map(self):
        if self.ox_idx == []:
            disp('Not yet found oxygen')
            return

        self.flood_map = [(statuses > -1) -1 for statuses in self.status]
        # Either zeros for corridors, or -1 for walls

        self.flood_map[self.ox_idx] = 1 # This is the distance from the flood point, + 1

        pointer = self.ox_idx - 1
        while 0 in self.flood_map:
            self.flood_square(pointer)
            pointer -= 1
            if pointer < 0:
                pointer = len(self.flood_map) -1

    def flood_square(self, idx):
        # Assumes flood_map is initialised
        flood_stat = self.flood_map[idx]

        if flood_stat != 0:
            return

        position = self.positions[idx]
        surrounding_positions = [position + 1, position - 1, position + 1j, position - 1j]
        surrounding_indices = [n for n, pos in enumerate(self.positions) if pos in surrounding_positions]
        surrounding_floods = [self.flood_map[idx] for idx in surrounding_indices]
        flooded = [point for point in surrounding_floods if point > 0]
        if len(flooded) > 0:
            self.flood_map[idx] = min(flooded) + 1

