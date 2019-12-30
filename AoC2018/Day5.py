class Polymer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.string = []
        self.new_string(self.input_string)

    def new_string(self, input_string):
        self.string = [letter for letter in input_string]

    def do_reaction(self, start):
        for n in range(start, len(self.string)):
            letter = self.string[n]
            prev_letter = self.string[n-1]
            if prev_letter.lower() == letter.lower() and prev_letter != letter:
                self.string[n-1:n+1] = []
                return n

        return -1

    def do_until_complete(self):
        start = 2
        while start != -1:
            start = self.do_reaction(start-1)
            print(start)

    def remove_element(self, element):
        # Reset
        self.new_string(self.input_string)
        self.string = [letter for letter in self.string if letter not in [element.upper(), element.lower()]]

    def remove_and_do(self, element):
        self.remove_element(element)
        self.do_until_complete()
        return len(self.string)

    def remove_all_letters(self):
        letters = 'ABCDEFGHIJKLMNOPQRSTUWXYZ'
        # WHY DOES 'V' FAIL?
        self.letter_dict = {}
        for letter in letters:
            self.letter_dict[letter] = self.remove_and_do(letter)
            print('Letter {}: {}'.format(letter, self.letter_dict[letter]))
