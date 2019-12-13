class Amplifiers:
    def __init__(self, codestring, num_amplifiers):
        # Creates num_amplifiers copies of IntCode
        self.amplifiers = [IntCode(codestring) for _ in range(num_amplifiers)]
        self.amp_pointer = 0
        self.is_finished = False
        self.thrust = 0

    def initialise_amplifier(self, command):
        # Sets input of first amplifier
        self.amplifiers[0].set_inputs([command, 0])

    def run_amplifier_single_run(self, next_command):
        self.amplifiers[self.amp_pointer].process()
        output = self.amplifiers[self.amp_pointer].outputs[-1]
        self.amp_pointer += 1
        if self.amp_pointer < len(self.amplifiers):
            self.amplifiers[self.amp_pointer].set_inputs([next_command, output])
        else:
            self.is_finished = True
            self.thrust = output
            print('Final thrust: {}'.format(output))

    def process_single_run(self, command_list):
        self.initialise_amplifier(command_list[0])
        while not self.is_finished:
            command_pointer = self.amp_pointer + 1
            if command_pointer == len(self.amplifiers):
                command_pointer = 0
            self.run_amplifier_single_run(command_list[command_pointer])

    def initialise_all_amplifiers(self, command_list):
        for n, amp in enumerate(self.amplifiers):
            amp.set_inputs([command_list[n]])

    def process_until_completion(self):
        # Assumes all amplifiers have been initialised

        output = 0
        while not self.is_finished:
            for amp in self.amplifiers:
                amp.inputs.append(output)
                output = amp.process_until_output()
                if amp.is_finished:
                    self.is_finished
                    return self.thrust

            self.thrust = output


def iterate_over_phase_sequences(codestring):
    # Create list of all permutations
    thrusts = []
    for permutation in permutations(range(5)):
        list_perm = list(permutation)
        amp = Amplifiers(codestring, 5)
        amp.process(list_perm)
        thrusts.append(amp.thrust)

    max_idx = [n for n, thrust in enumerate(thrusts) if thrust == max(thrusts)][0]
    return thrusts[max_idx]


def iterate_feedback(codestring):
    thrusts = []
    for permutation in permutations(range(5, 10)):
        list_perm = list(permutation)
        amps = Amplifiers(codestring, 5)
        amps.initialise_all_amplifiers(list_perm)
        thrusts.append(amps.process_until_completion())

    max_idx = [n for n, thrust in enumerate(thrusts) if thrust == max(thrusts)][0]
    return thrusts[max_idx]


