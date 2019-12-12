def rocketfuel(rocket_mass):
    return rocket_mass // 3 - 2


text_file = open('Day1Input.txt')
mass_list = text_file.readlines()
fuel_list = [rocketfuel(int(mass[:-1])) for mass in mass_list]

fuel = sum(fuel_list)

def rocketfuel_recurse(rocket_mass):
    add_fuel = rocketfuel(rocket_mass)
    fuel = add_fuel
    while add_fuel > 0:
        add_fuel = max(0, rocketfuel(add_fuel))
        fuel = fuel + add_fuel

    return fuel

text_file = open('Day1Input.txt')
mass_list = text_file.readlines()
fuel_list = [rocketfuel_recurse(int(mass[:-1])) for mass in mass_list]

fuel = sum(fuel_list)