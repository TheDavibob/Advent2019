class FFT:
    def __init__(self, input_signal):
        self.signal = [int(x) for x in input_signal]
        self.base_pattern = [0, 1, 0, -1]
        self.reps = 0

    def determine_pattern(self, n):
        # Note: n is the position index, not the usual index
        pattern = []
        for num in self.base_pattern:
            for _ in range(n):
                pattern.append(num)

        return pattern

    def single_component(self, pattern):
        reps = len(self.signal) // len(pattern) + 1
        pattern = reps*pattern
        pattern.pop(0)

        products = [sig*pattern[n] for n, sig in enumerate(self.signal)]

        return int(str(sum(products))[-1])

    def all_components(self):
        self.signal = [self.single_component(self.determine_pattern(n+1)) for n in range(len(self.signal))]
        self.reps += 1

    def complete_n_loops(self, n):
        while self.reps < n:
            self.all_components()

    def extract_message(self):
        # This is just a demonstration - it blatantly does not work
        n = 100
        message_offset = int(''.join([str(digit) for digit in self.signal[:7]]))

        self.signal = 10000*self.signal

        self.complete_n_loops_fast(n)

        return message_offset, self.signal[message_offset:message_offset+8]

    def fast_transform(self):
        import numpy as np
        # This brutally assumes that we care only about numbers late enough in the sequence that we can utterly trash the algorithm
        signal_reversed = self.signal[-1::-1]
        self.signal = list((np.cumsum(signal_reversed) % 10)[-1::-1])
        self.reps += 1

    def complete_n_loops_fast(self, n):
        while self.reps < n:
            self.fast_transform()
