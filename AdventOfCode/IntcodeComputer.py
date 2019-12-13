from itertools import permutations

class IntCode:
    def __init__(self, codestring):
        self.int_string = [int(x) for x in str(codestring).split(',')]
        self.current_idx = 0

        self.rel_base = 0

        # Some addition predefinitions
        self.opcode = 0
        self.mode = 0
        self.inputs = []
        self.outputs = []
        self.input_pointer = 0

        # This allows reset to use the original string
        self.stored_string = self.int_string

        self.is_finished = False

    def process_instruction(self, instruction):
        # Updates instruction from an artibrary index
        instruction_string = str(instruction)
        self.opcode = int(instruction_string[-2:])
        self.mode = [int(letter) for letter in instruction_string[-3::-1]]

    def get_instruction(self):
        self.process_instruction(self.int_string[self.current_idx])

    def update_pointer(self, step):
        self.current_idx = self.current_idx + step
        if self.current_idx > len(self.int_string):
            self.is_finished = True

    def get_params(self, n):
        # Gets the next n parameters according to mode
        params = []
        for idx in range(n):
            string_number = self.int_string[self.current_idx + idx + 1]
            if idx < len(self.mode):
                mode = self.mode[idx]
            else:
                mode = 0

            if mode == 0:
                # position mode
                if string_number >= len(self.int_string):
                    params.append(0)
                else:
                    params.append(self.int_string[string_number])
            elif mode == 1:
                # immediate mode
                params.append(string_number)
            elif mode == 2:
                shifted_number = string_number + self.rel_base
                # relative mode
                if shifted_number >= len(self.int_string):
                    params.append(0)
                else:
                    params.append(self.int_string[shifted_number])
            else:
                raise Exception('Unrecognised mode: {}'.format(mode))

        return params

    def process_opcode(self):
        # Takes instruction, calls relevant method
        if self.opcode == 1:
            self.do_add()
        elif self.opcode == 2:
            self.do_multiply()
        elif self.opcode == 3:
            self.do_input()
        elif self.opcode == 4:
            self.do_output()
        elif self.opcode == 5:
            self.do_jump_if_true()
        elif self.opcode == 6:
            self.do_jump_if_false()
        elif self.opcode == 7:
            self.do_less_than()
        elif self.opcode == 8:
            self.do_equals()
        elif self.opcode == 9:
            self.do_update_base()
        elif self.opcode == 99:
            self.do_terminate()
        else:
            raise Exception('Unrecognised opcode: {}'.format(self.opcode))

    def storage_position(self, n):
        # Finds the position in which to store the result of an instruction
        # If out of range, extends int_str
        idx = self.current_idx + n
        if n-1 < len(self.mode):
            mode = self.mode[n-1]
        else:
            mode = 0

        storage_idx = self.int_string[idx]

        if mode == 0:
            pass
        elif mode == 2:
            storage_idx = storage_idx + self.rel_base
        elif mode == 1:
            raise Exception('Cannot use immediate mode for storing new data')

        if storage_idx >= len(self.int_string):
            self.int_string = self.int_string + (storage_idx + 1 - len(self.int_string))*[0]
        return storage_idx

    def do_add(self):
        # Takes next two parameters, adds them, puts in position of third parameter
        storage_idx = self.storage_position(3)
        params = self.get_params(2)
        self.int_string[storage_idx] = params[0] + params[1]
        self.update_pointer(4)

    def do_multiply(self):
        # Takes next two parameters, multiplies them, puts in position of third parameter
        storage_idx = self.storage_position(3)
        params = self.get_params(2)
        self.int_string[storage_idx] = params[0] * params[1]
        self.update_pointer(4)

    def do_terminate(self):
        self.is_finished = True

    def do_jump_if_true(self):
        params = self.get_params(2)
        if params[0] > 0:
            self.current_idx = params[1]
        else:
            self.update_pointer(3)

    def do_jump_if_false(self):
        params = self.get_params(2)
        if params[0] == 0:
            self.current_idx = params[1]
        else:
            self.update_pointer(3)

    def do_less_than(self):
        params = self.get_params(2)
        storage_idx = self.storage_position(3)
        self.int_string[storage_idx] = int(params[0] < params[1])
        self.update_pointer(4)

    def do_equals(self):
        params = self.get_params(2)
        storage_idx = self.storage_position(3)
        self.int_string[storage_idx] = int(params[0] == params[1])
        self.update_pointer(4)

    def do_input(self):
        storage_idx = self.storage_position(1)
        if self.input_pointer < len(self.inputs):
            input_number = self.inputs[self.input_pointer]
            self.input_pointer += 1
        else:
            print('Enter input:')
            input_string = input()
            input_number = int(input_string)

        self.int_string[storage_idx] = input_number
        self.update_pointer(2)

    def do_output(self):
        params = self.get_params(1)
        print('Output = {}'.format(params[0]))
        self.outputs.append(params[0])
        self.update_pointer(2)

    def do_update_base(self):
        params = self.get_params(1)
        self.rel_base = self.rel_base + params[0]
        self.update_pointer(2)

    def step(self):
        # One step of the loop
        self.get_instruction()
        self.process_opcode()

    def process(self):
        self.reset()
        while not self.is_finished:
            self.step()

    def process_until_output(self):
        # This continues (from any old position) until an output is passed
        current_output_length = len(self.outputs)
        while not self.is_finished:
            self.step()
            if len(self.outputs) > current_output_length:
                break

        if not self.is_finished:
            return self.outputs[-1]

    def reset(self):
        self.is_finished = False
        self.current_idx = 0
        self.int_string = self.stored_string

    def set_inputs(self, inputs):
        # Creates a list of inputs that are automatically read by get_input. If the number of inputs runs out, the user is prompted as usual
        self.inputs = inputs
        self.input_pointer = 0

# puzzle_input = '3,225,1,225,6,6,1100,1,238,225,104,0,1101,72,36,225,1101,87,26,225,2,144,13,224,101,-1872,224,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1102,66,61,225,1102,25,49,224,101,-1225,224,224,4,224,1002,223,8,223,1001,224,5,224,1,223,224,223,1101,35,77,224,101,-112,224,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1002,195,30,224,1001,224,-2550,224,4,224,1002,223,8,223,1001,224,1,224,1,224,223,223,1102,30,44,225,1102,24,21,225,1,170,117,224,101,-46,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1102,63,26,225,102,74,114,224,1001,224,-3256,224,4,224,102,8,223,223,1001,224,3,224,1,224,223,223,1101,58,22,225,101,13,17,224,101,-100,224,224,4,224,1002,223,8,223,101,6,224,224,1,224,223,223,1101,85,18,225,1001,44,7,224,101,-68,224,224,4,224,102,8,223,223,1001,224,5,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,7,677,226,224,102,2,223,223,1005,224,329,101,1,223,223,8,677,226,224,1002,223,2,223,1005,224,344,1001,223,1,223,1107,677,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,374,101,1,223,223,7,226,677,224,102,2,223,223,1005,224,389,101,1,223,223,8,226,677,224,1002,223,2,223,1005,224,404,101,1,223,223,1008,226,677,224,1002,223,2,223,1005,224,419,1001,223,1,223,107,677,677,224,102,2,223,223,1005,224,434,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,449,101,1,223,223,1108,677,677,224,102,2,223,223,1006,224,464,101,1,223,223,1007,677,226,224,102,2,223,223,1006,224,479,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,509,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,524,101,1,223,223,1107,677,226,224,102,2,223,223,1005,224,539,1001,223,1,223,108,226,677,224,1002,223,2,223,1005,224,554,101,1,223,223,1007,226,226,224,102,2,223,223,1005,224,569,101,1,223,223,8,226,226,224,102,2,223,223,1006,224,584,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,599,1001,223,1,223,107,226,677,224,1002,223,2,223,1005,224,614,1001,223,1,223,1108,226,677,224,102,2,223,223,1006,224,629,101,1,223,223,7,677,677,224,1002,223,2,223,1005,224,644,1001,223,1,223,108,677,677,224,102,2,223,223,1005,224,659,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,674,101,1,223,223,4,223,99,226'


