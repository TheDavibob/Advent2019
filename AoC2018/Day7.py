import re

def parse_line(line):
    p = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin.')
    output = p.findall(line)
    if len(output) > 0:
        return output[0]
    else:
        return None


def parse_many_lines(lines):
    return [parse_line(line) for line in lines.split('\n') if len(line) > 0]


class FindSequence:
    def __init__(self, lines):
        self.sequence_string = ''
        self.blockers = parse_many_lines(lines)
        self.blocked_elements = list(set([y for x, y in self.blockers]))

    def find_open_steps(self):
        inputs = [x for x, y in self.blockers] + [z for z in self.blocked_elements if z not in self.sequence_string]
        outputs = [y for x, y in self.blockers]
        return list(set(inputs).difference(set(outputs)))

    def remove_first_step(self):
        open_steps = self.find_open_steps()
        if len(open_steps) == 0:
            return True   # finished
        open_steps.sort()
        element = open_steps[0]
        self.sequence_string += element

        # Remove blocking elements
        self.blockers = [(x,y) for x,y in self.blockers if x != element]

        return False   # not finished

    def process(self):
        is_finished = False
        while not is_finished:
            is_finished = self.remove_first_step()

        print(self.sequence_string)

    @staticmethod
    def determine_job_time(letter):
        return ord(letter) - 4

    def initialize_workers(self, n):
        self.workers_busy = n*[0]
        self.current_job = n*['']

    def workers_step(self, subtract_min=False):
        for idx, worker in enumerate(self.workers_busy):
            if worker == 1:
                # Remove blocking elements
                self.blockers = [(x,y) for x,y in self.blockers if x != self.current_job[idx]]
                self.workers_busy[idx] = 0
                worker = 0
                self.sequence_string += self.current_job[idx]
                self.current_job[idx] = ''

            if worker == 0:
                # Find next available job
                open_steps = self.find_open_steps()
                if len(open_steps) == 0:
                    return True  # finished
                open_steps = [step for step in open_steps if step not in self.current_job]
                if len(open_steps) == 0:
                    continue   # no available jobs
                open_steps.sort()
                element = open_steps[0]
                time = self.determine_job_time(element)
                if subtract_min:
                    time = time - 60
                self.workers_busy[idx] += time
                self.current_job[idx] = element
            else:
                self.workers_busy[idx] -= 1

        return False   # not finished

    def run_all_workers(self, n, subtract_min=False):
        self.initialize_workers(n)
        is_finished = False
        time = 0
        while not is_finished:
            is_finished = self.workers_step(subtract_min=subtract_min)
            time += 1

        return time - 1
