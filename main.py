import numpy as np
from numpy.ma.core import minimum_fill_value

from HungarianMethod import hungarian

if __name__ == '__main__':
    n = 6
    min_value = 1
    max_value = 100
    # test_matrix = np.random.randint(min_value, max_value + 1, (n, n))
    test_matrix = np.array([
        [3, 1, 5, 6, 4, 7],
        [2, 4, 1, 7, 5, 6],
        [6, 5, 3, 1, 7, 4],
        [5, 7, 4, 2, 1, 6],
        [4, 6, 7, 3, 2, 5],
        [7, 3, 6, 5, 4, 2],
    ])
    print(test_matrix)
    print()
    print(hungarian(test_matrix))
