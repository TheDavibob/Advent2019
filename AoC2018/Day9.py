class MarbleGame:
    def __init__(self, n_players, n_turns):
        self.n_players = n_players
        self.n_turns = n_turns
        self.scores = n_players*[0]

        self.current_idx = 0
        self.marbles = [0]
        self.next_marble = 1
        self.score_history = []

        self.player = 0
        self.turn = 0

        self.index_history = [0]

    def normal_turn(self):
        self.current_idx = (self.current_idx + 2) % len(self.marbles)
        self.marbles = (self.marbles[:self.current_idx]
                        + [self.next_marble]
                        + self.marbles[self.current_idx:]
                        )
        self.next_marble += 1

    def funkeh_turn(self, player):
        self.scores[player] += self.next_marble
        self.current_idx = (self.current_idx - 7) % len(self.marbles)

        self.scores[player] += self.marbles[self.current_idx]
        self.score_history.append(self.marbles[self.current_idx])
        self.marbles = self.marbles[:self.current_idx] + self.marbles[self.current_idx+1:]

        self.next_marble += 1

    def play_game(self):
        self.player = 0
        self.turn = 1
        while self.turn <= self.n_turns:
            if self.turn % 23 == 0:
                self.funkeh_turn(self.player)
            else:
                self.normal_turn()

            self.index_history.append(self.current_idx)

            self.turn += 1
            self.player += 1
            self.player = self.player % self.n_players

        print('High score = {}'.format(max(self.scores)))

    def resort(self):
        # Once a game has been completed, after some point any additional numbers do not matter
        self.marbles = self.marbles[self.current_idx:] + self.marbles[:self.current_idx]
        self.current_idx = 0

    def continue_playing(self, new_turns):
        # BAAAAD
        self.resort()
        self.current_idx -= 7
        self.scores[self.player] += self.marbles[self.current_idx] + self.turn
        self.score_history.append(self.marbles[self.current_idx])

        self.player += 23
        self.player = self.player % self.n_players
        self.turn += 23

        n = 0

        while self.turn < new_turns:
            if n == 0:
                self.current_idx += 20
            else:
                self.current_idx += 16

            self.current_idx %= len(self.marbles)

            self.scores[self.player] += self.marbles[self.current_idx] + self.turn
            self.score_history.append(self.marbles[self.current_idx])

            self.player += 23
            self.player = self.player % self.n_players
            self.turn += 23
            n += 1

