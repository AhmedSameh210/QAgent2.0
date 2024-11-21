import math
import random
import copy
from random import randint, choice
import string

rng = random.Random(42)


class FixDataSeries:
    def __init__(self, df,series_name):

        corresponding_index = 32
        fixed_value = []

        for _ in range(10):
            ncoeff = 2 * rng.randint(1, 4)
            coeffs = []
            for _ in range(ncoeff):
                coeff = rng.randint(-10, 10)
                if coeff == 0:
                    coeff = 1
                coeffs.append(coeff)
                fixed_value.append(f"assert math.fabs(poly({coeffs}, sort_third(copy.deepcopy({coeffs})))) < 1e-4")
        df[series_name][corresponding_index] = fixed_value


        corresponding_index = 38
        fixed_value = []

        for _ in range(10):
            fixed_value.append(f"assert decode_cyclic(encode_cyclic(str)) == '{''.join(choice(string.ascii_lowercase) for i in range(randint(10, 20)))}'")
        df[series_name][corresponding_index] = fixed_value

        corresponding_index = 50
        fixed_value = []

        for _ in range(10):
            fixed_value.append(f"assert decode_shift(copy.deepcopy(encode_shift('{''.join(choice(string.ascii_lowercase) for i in range(randint(10, 20)))}'))) == '{''.join(choice(string.ascii_lowercase) for i in range(randint(10, 20)))}'")
        df[series_name][corresponding_index] = fixed_value

        corresponding_index = 87
        fixed_value = [
            'assert get_row([[1,2,3,4,5,6],[1,2,3,4,1,6],[1,2,3,4,5,1]], 1) == [(0, 0), (1, 4), (1, 0), (2, 5), (2, 0)]',
            'assert get_row([[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6],[1,2,3,4,5,6]], 2) == [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1)]',
            'assert get_row([[1,2,3,4,5,6],[1,2,3,4,5,6],[1,1,3,4,5,6],[1,2,1,4,5,6],[1,2,3,1,5,6],[1,2,3,4,1,6],[1,2,3,4,5,1]], 1) == [(0, 0), (1, 0), (2, 1), (2, 0), (3, 2), (3, 0), (4, 3), (4, 0), (5, 4), (5, 0), (6, 5), (6, 0)]',
            'assert get_row([], 1) == []',
            'assert get_row([[1]], 2) == []',
            'assert get_row([[], [1], [1, 2, 3]], 3) == [(2, 2)]',
            'assert True'
        ]
        df[series_name][corresponding_index] = fixed_value
