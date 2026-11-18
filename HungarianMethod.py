import numpy as np


def hungarian(matrix):
    solution = []
    while len(solution) < np.min(matrix.shape):
        transformed_matrix = zero_in_matrix(matrix)
        solution = max_matching(transformed_matrix)

    return solution


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
                graph[matching[i + 1]].remove(matching[i])
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
            stack.append((i, matching))


def check_cycle(element, matching, state):
    if state == "enter":
        required_state = 1
    elif state == "exit":
        required_state = 0
    else:
        raise Exception("Invalid state")
    return element not in matching or matching.index(element) % 2 != required_state
