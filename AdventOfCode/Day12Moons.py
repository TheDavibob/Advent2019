def extract_pos(pos_string):
    # pos_string of form <x=-1, y=0, z=2>
    pos_string = pos_string[1:-1]
    x,y,z = [int(word.split('=')[1]) for word in pos_string.split(', ')]
    return x, y, z

class Moon:
    def __init__(self, name, pos_string):
        self.name = name
        self.x, self.y, self.z = extract_pos(pos_string)
        self.u, self.v, self.w = [0, 0, 0]

    def move(self):
        self.x = self.x + self.u
        self.y = self.y + self.v
        self.z = self.z + self.w

    def update_vels(self, moons):
        for moon in moons:
            if moon != self:
                if moon.x > self.x:
                    self.u = self.u + 1
                elif moon.x < self.x:
                    self.u = self.u - 1

                if moon.y > self.y:
                    self.v = self.v + 1
                elif moon.y < self.y:
                    self.v = self.v - 1

                if moon.z > self.z:
                    self.w = self.w + 1
                elif moon.z < self.z:
                    self.w = self.w - 1

    def print_position(self):
        print('Position of ' + self.name + ' is ' + str([self.x, self.y, self.z]))

    def print_velocity(self):
        print('Velocity of ' + self.name + ' is ' + str([self.u, self.v, self.w]))

    def get_pot_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def get_kin_energy(self):
        return abs(self.u) + abs(self.v) + abs(self.w)

    def get_energy(self):
        return self.get_kin_energy() * self.get_pot_energy()

    def print_energy(self):
        print('Energy of ' + self.name + ' is ' + self.get_energy())


## The main functions
def create_moons(initial_string):
    each_moon = initial_string.split('\n')
    Io = Moon('Io', each_moon[0])
    Europa = Moon('Europa', each_moon[1])
    Ganymede = Moon('Ganymede', each_moon[2])
    Callisto = Moon('Callisto', each_moon[3])

    return [Io, Europa, Ganymede, Callisto]


def move_moons(moons):
    for moon in moons:
        moon.move()
        moon.print_position()
        moon.print_velocity()

    return moons

def create_and_move_for_n_cycles(initial_string, n):
    moons = create_moons(initial_string)
    for idx in range(n):
        print('Step ' + str(idx))
        move_moons(moons)

        for moon in moons:
            moon.update_vels(moons)

    print('Step ' + str(n))
    move_moons(moons)
    total_energy = sum([moon.get_energy() for moon in moons])
    print('Total energy ' + str(total_energy))

    return moons