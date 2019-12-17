import random as rand

class FuelComputer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.chemicals = {}
        self.extract_all_chemicals()

    def extract_all_chemicals(self):
        # Extracts all possible chemicals avaliable in the input
        for line in self.input_string.split('\n'):
            split_line = line.split(' ')
            chemical_name = split_line[-1]
            chemical_number = int(split_line[-2])

            chem_dict = {}
            for n in range((len(split_line) - 3)//2):
                chem_dict[split_line[2*n+1].replace(',', '')] = int(split_line[2*n])

            self.chemicals[chemical_name] = (chemical_number, chem_dict)

    def simple_extraction(self, product, reagant):
        '''
        If a product has an exact multiple of the number of a
        reagant created in one batch as an input, we can replace
        this reagent with its own reagents, then consolidate
        '''
        # number of the reagant needed to make product
        number_reag_needed = self.chemicals[product][1][reagant]

        # number of regants produced in its reaction
        number_reag_produced = self.chemicals[reagant][0]

        if number_reag_needed % number_reag_produced != 0:
            raise Exception('NotSimple', number_reag_needed, number_reag_produced, product, reagant)

        # The multiple of the reagants required
        multiple_reags = number_reag_needed//number_reag_produced

        for k in self.chemicals[reagant][1]:
            if k in self.chemicals[product][1]:
                self.chemicals[product][1][k] = self.chemicals[product][1][k] + multiple_reags*self.chemicals[reagant][1][k]
            else:
                self.chemicals[product][1][k] = multiple_reags*self.chemicals[reagant][1][k]

        # Remove reagant from list
        self.chemicals[product][1].pop(reagant)

    def simple_loop(self, product):
        # Loops simple_extraction over all current elements of reaction
        old_dict = self.chemicals[product][1].copy()
        for reagant in old_dict:
            try:
                #self.simple_extraction(product, reagant)
                self.reduce_what_we_can(product, reagant)
            except:
                pass

        # Returns true if the dictionary has not been updated
        return old_dict == self.chemicals[product][1]

    def all_simple_loops(self, product):
        is_static = self.simple_loop(product)
        while not is_static:
            is_static = self.simple_loop(product)

    def non_simple_extraction(self, product, reagant):
        # For a given reagant, finds the first number of reagants that can be produced
        # number of the reagant needed to make product
        number_reag_needed = self.chemicals[product][1][reagant]

        # number of regants produced in its reaction
        number_reag_produced = self.chemicals[reagant][0]

        new_num_reag_needed = (number_reag_needed // number_reag_produced + 1)*number_reag_produced

        # Overwrite this value in the dictionary
        self.chemicals[product][1][reagant] = new_num_reag_needed
        # Run simple extraction
        self.simple_extraction(product, reagant)

    def reduce_what_we_can(self, product, reagant):
        # For a given reagant, reduces its number by as much as possible
        # This is 'safe' so can replace simple extraction
        number_reag_needed = self.chemicals[product][1][reagant]

        # number of regants produced in its reaction
        number_reag_produced = self.chemicals[reagant][0]

        new_num_reag_needed = (number_reag_needed // number_reag_produced)*number_reag_produced
        remaining_reag = number_reag_needed - new_num_reag_needed

        # Overwrite this value in the dictionary
        self.chemicals[product][1][reagant] = new_num_reag_needed
        # Run simple extraction
        self.simple_extraction(product, reagant)

        # Readd if there are any remaining things
        if remaining_reag > 0:
            self.chemicals[product][1][reagant] = remaining_reag

    def all_loops(self, product):
        old_dict = {}
        while old_dict != self.chemicals[product][1]:
            old_dict = self.chemicals[product][1].copy()
            self.all_simple_loops(product)
            if len(self.chemicals[product][1]) > 1:
                # More than just ore, extract on first non-ore element
                # THIS IS NON-OPTIMAL
                chemicals = self.chemicals[product][1]
                chem_list = [chemical for chemical in chemicals if chemical != 'ORE']
                rand.shuffle(chem_list)
                reagent = chem_list[0]
                self.non_simple_extraction(product, reagent)

        print('Ore required for {}: {}'.format(product, self.chemicals[product][1]['ORE']))
        return self.chemicals[product][1]['ORE']

    def many_random_shuffles(self, n):
        many_guesses = []
        for _ in range(n):
            self.chemicals = {}
            self.extract_all_chemicals()
            many_guesses.append(self.all_loops('FUEL'))

        return min(many_guesses), many_guesses

    def reduce_ore_only(self, product, reagant):
        # Reduces a product if the only component is ore, by rounding up
        # This is 'safe' as there is no other way to obtain this chemical
        if reagant != 'ORE' and len(self.chemicals[reagant][1]) == 1:
            self.non_simple_extraction(product, reagant)

    def all_loops_all_products(self):
        # This is a 'safe' loop, it doesn't necessarily finish
        old_chems = {}
        while self.chemicals != old_chems:
            old_chems = self.chemicals.copy()
            for product in self.chemicals.copy():
                self.all_simple_loops(product)
            for product in self.chemicals.copy():
                for reagant in self.chemicals[product][1].copy():
                    self.reduce_ore_only(product, reagant)

