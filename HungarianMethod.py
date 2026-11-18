import numpy as np


def hungarian(matrix):
    solution = []
    n = np.min(matrix.shape)
    transformed_matrix = matrix
    while len(solution) < n:
        transformed_matrix = zero_in_matrix(transformed_matrix)
        solution = max_matching(transformed_matrix)
        if len(solution) < n:
            crosses = cross_significant_zeros(transformed_matrix, solution)
            # print(transformed_matrix)
            A = np.min(transformed_matrix[crosses == 0])
            transformed_matrix = np.where(crosses == 0, transformed_matrix - A,
                                          np.where(crosses == 2, transformed_matrix + A, transformed_matrix))
            # print(A)
            # print(transformed_matrix)
            # print(solution)

    return np.sum(matrix[*zip(*solution)])


def zero_in_rows(matrix):
    row_mins = matrix.min(axis=1).reshape(-1, 1)
    transformed_matrix = matrix - row_mins
    return transformed_matrix


def zero_in_columns(matrix):
    col_mins = matrix.min(axis=0).reshape(-1, 1)
    transformed_matrix = (matrix.T - col_mins).T
    return transformed_matrix


def zero_in_matrix(matrix):
    return zero_in_columns(zero_in_rows(matrix))


def max_matching(matrix):
    graph = {
        i: [j for j in range(matrix.shape[1]) if matrix[i, j] == 0]
        for i in range(matrix.shape[0])
    }
    graph_reverse = {
        i: [] for i in range(matrix.shape[0])
    }
    used_enters = []
    used_exits = []
    solutions = []
    matching = find_possible_matching(graph, graph_reverse, used_enters, used_exits)
    while len(matching) > 0:
        used_enters.append(matching[0])
        used_exits.append(matching[len(matching) - 1])
        for i in range(len(matching) - 1):
            if i % 2 == 0:
                graph[matching[i]].remove(matching[i + 1])
                graph_reverse[matching[i + 1]].append(matching[i])
                solutions.append((matching[i], matching[i + 1]))
            else:
                graph_reverse[matching[i]].remove(matching[i + 1])
                graph[matching[i + 1]].append(matching[i])
                solutions.remove((matching[i + 1], matching[i]))

        matching = find_possible_matching(graph, graph_reverse, used_enters, used_exits)
    return solutions


def find_possible_matching(graph, graph_reverse, used_enters, used_exits):
    not_used_enters = [i for i in graph.keys() if i not in used_enters]
    not_used_exits = [i for i in graph.keys() if i not in used_exits]
    stack = [(i, []) for i in not_used_enters]
    result_matching = tuple()
    while len(stack) > 0 and len(result_matching) == 0:
        element = stack.pop()
        current_matching = element[1]
        current_matching.append(element[0])
        state = "enter" if len(element[1]) % 2 == 1 else "exit"
        if state == "enter":
            add_possible_moves(stack, graph[element[0]], current_matching, state)
            # for i in graph[element[0]]:
            #     if check_cycle(i, current_matching, state):
            #         stack.append((i, current_matching))
        else:
            if element[0] in not_used_exits:
                result_matching = tuple(current_matching)
            else:
                add_possible_moves(stack, graph_reverse[element[0]], current_matching, state)
                # for i in graph_reverse[element[0]]:
                #     if check_cycle(i, current_matching, state):
                #         stack.append((i, current_matching))

    return result_matching


def add_possible_moves(stack, next_elements, matching, state):
    for i in next_elements:
        if check_cycle(i, matching, state):
            stack.append((i, matching.copy()))


def check_cycle(element, matching, state):
    if state == "enter":
        required_state = 1
    elif state == "exit":
        required_state = 0
    else:
        raise Exception("Invalid state")
    return element not in matching or matching.index(element) % 2 != required_state


def cross_significant_zeros(matrix, solution):
    marked_rows, marked_cols = mark_zeros(matrix, solution)
    crosses = np.ones(matrix.shape)
    crosses[marked_rows] -= 1
    crosses.T[marked_cols] += 1
    return crosses


def mark_zeros(matrix, solution):
    rows_with_significant_zeros = np.array(solution)[:, 0].reshape(-1)
    rows_without_significant_zeros = np.array([i for i in range(matrix.shape[0])
                                               if i not in rows_with_significant_zeros])
    marked_rows = []
    marked_cols = []
    for i in rows_without_significant_zeros:
        if i not in marked_rows:
            current_number = int(i)
            marked_rows.append(current_number)
            search_column = True
            current_row = matrix[current_number, :].reshape(-1)
            current_col = matrix[:, current_number].reshape(-1)
            stop = False
            while (search_column and 0 in current_row or
                   not search_column and 0 in current_col) and not stop:
                stop = True
                if search_column:
                    for j in range(len(current_row)):
                        if (matrix[current_number, j] == 0 and j not in marked_cols and
                                (current_number, j) not in solution and stop):
                            current_number = j
                            marked_cols.append(current_number)
                            stop = False
                else:
                    for j in range(len(current_col)):
                        if (matrix[j, current_number] == 0 and j not in marked_rows and
                                (j, current_number) in solution and stop):
                            current_number = j
                            marked_rows.append(current_number)
                            stop = False
                search_column = not search_column

    return marked_rows, marked_cols
