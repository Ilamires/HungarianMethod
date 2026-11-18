import numpy as np
from HungarianMethod import hungarian

if __name__ == '__main__':
    test_matrix = np.random.randint(1, 101, (6, 6))
    print(test_matrix)
    print()
    print(hungarian(test_matrix))