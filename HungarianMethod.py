import numpy as np

def hungarian(matrix):
    row_mins = matrix.min(axis=1).reshape(-1, 1)
    transformed_matrix = matrix - row_mins

    col_mins = transformed_matrix.min(axis=0).reshape(-1, 1)
    transformed_matrix = (transformed_matrix.T - col_mins).T
    return transformed_matrix