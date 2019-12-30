import re
import CommonTools as ct
from operator import itemgetter
import numpy as np

def process_instruction(input_string):
    ymd = int(''.join(re.search('\d+-\d+-\d+', input_string)[0].split('-')))
    # Can merge together as sort correctly

    mh = int(''.join(re.search('\d+:\d+', input_string)[0].split(':')))

    guard_number_string = re.search('#\d+', input_string)
    if guard_number_string is None:
        if re.search('wakes up', input_string):
            state = 0
        elif re.search('falls asleep', input_string):
            state = -1

    else:
        state = int(guard_number_string[0][1:])

    return ymd, mh, state


def process_all_instructions(input_string):
    lines = ct.string_to_lines(input_string)
    return [process_instruction(line) for line in lines]


class RecordContainer:
    def __init__(self, input_string):
        self.instructions = process_all_instructions(input_string)
        # Sort into chronological order
        self.instructions.sort(key=itemgetter(0, 1))

        # Create list of relevant guard for each tuple
        self.guard = [0 for sample in self.instructions]
        new_guard = 0
        for n, tup in enumerate(self.instructions):
            if tup[2] > 0:
                new_guard = tup[2]
            self.guard[n] = new_guard

        self.guard_list = list(set(self.guard))
        self.sleep_time = np.zeros((len(self.guard_list), 60))
        self.update_sleep_calendar()

    def update_sleep_calendar(self):
        for n, tup in enumerate(self.instructions):
            if tup[2] == 0:
                # Guard wakes up
                sleep = self.instructions[n-1][1]
                wake = tup[1]

                # Find which row of sleep time array we want
                row = self.guard_list.index(self.guard[n])
                self.sleep_time[row, sleep:wake] += 1

    def find_laziest_guard(self):
        sum_by_guard = np.sum(self.sleep_time, axis=1)
        idx = np.argmax(sum_by_guard)
        max_min = np.argmax(self.sleep_time[idx,:])
        return self.guard_list[idx], max_min

    def find_laziest_minute(self):
        guard_no, min = np.unravel_index(np.argmax(self.sleep_time), self.sleep_time.shape)
        return self.guard_list[guard_no], min
