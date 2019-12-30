import numpy as np
import re

class SantaGrid:
    def __init__(self, n):
        self.grid = np.zeros((n,n))

    def parse_claim(self, claim):
        claim_id = int(re.search('#\d+', claim)[0][1:])
        claim_x = int(re.search('\d+,', claim)[0][:-1])
        claim_y = int(re.search(',\d+', claim)[0][1:])
        claim_w = int(re.search('\d+x', claim)[0][:-1])
        claim_h = int(re.search('x\d+', claim)[0][1:])
        return claim_id, claim_x, claim_y, claim_w, claim_h

    def update_grid(self, claim):
        claim_id, claim_x, claim_y, claim_w, claim_h = self.parse_claim(claim)
        claim_mask = np.zeros(self.grid.shape)
        claim_mask[claim_y:claim_y+claim_h, claim_x:claim_x + claim_w] = 1
        claim_mask = claim_mask.astype(bool)

        filled_mask = self.grid > 0

        filled_claim = np.bitwise_and(filled_mask, claim_mask)
        self.grid[filled_claim] = 2

        unfilled_claim = np.bitwise_and(np.bitwise_not(filled_claim), claim_mask)
        self.grid[unfilled_claim] = 1

    def update_grid_with_id(self, claim):
        claim_id, claim_x, claim_y, claim_w, claim_h = self.parse_claim(claim)
        claim_mask = np.zeros(self.grid.shape)
        claim_mask[claim_y:claim_y+claim_h, claim_x:claim_x + claim_w] = 1
        claim_mask = claim_mask.astype(bool)

        filled_mask = self.grid != 0

        filled_claim = np.bitwise_and(filled_mask, claim_mask)
        self.grid[filled_claim] = np.nan

        unfilled_claim = np.bitwise_and(np.bitwise_not(filled_claim), claim_mask)
        self.grid[unfilled_claim] = claim_id

    def process_claims(self, claims, with_id=True):
        for claim in claims.split('\n'):
            if with_id:
                self.update_grid_with_id(claim)
            else:
                self.update_grid(claim)

    def is_unblemished(self, claim):
        claim_id, claim_x, claim_y, claim_w, claim_h = self.parse_claim(claim)
        return np.all(self.grid[claim_y:claim_y+claim_h, claim_x:claim_x + claim_w] == claim_id)

    def check_for_unblemished(self, claims):
        for claim in claims.split('\n'):
            if self.is_unblemished(claim):
                claim_id, claim_x, claim_y, claim_w, claim_h = self.parse_claim(claim)
                print(claim_id)
                return

