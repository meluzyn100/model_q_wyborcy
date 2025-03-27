import numpy as np
import random as r
import networkx as nx


def loopinf(n, _index, _model, q, type_of_choosing, independene, p, f):
    """Główna pętla symulacji."""
    N_plus = np.sum(_model == 1)
    while True:
        i, j = np.random.randint(0, n, size=2)
        Sij = _model[i, j]

        persons = [
            _model[_index[i], j],
            _model[i, _index[j]],
            _model[i, _index[j + 2]],
            _model[_index[i + 2], j],
        ]
        if type_of_choosing:
            neighbors = np.random.choice(persons, q)
        else:
            neighbors = r.sample(persons, q)

        if independene:
            rnd = r.random()
            if rnd < p:
                if r.random() < f:
                    _model[i, j] = -1
                    if Sij == 1:
                        N_plus -= 1
                else:
                    _model[i, j] = 1
                    if Sij == -1:
                        N_plus += 1
            else:
                sum_neighbors = np.sum(neighbors)
                if sum_neighbors == q:
                    _model[i, j] = 1
                    if Sij == -1:
                        N_plus += 1
                elif sum_neighbors == -q:
                    _model[i, j] = -1
                    if Sij == 1:
                        N_plus -= 1
        else:
            rnd = r.random()
            sum_neighbors = np.sum(neighbors)
            if rnd < p:
                if sum_neighbors == q:
                    _model[i, j] = -1
                    if Sij == 1:
                        N_plus -= 1
                elif sum_neighbors == -q:
                    _model[i, j] = 1
                    if Sij == -1:
                        N_plus += 1
            else:
                if sum_neighbors == q:
                    _model[i, j] = 1
                    if Sij == -1:
                        N_plus += 1
                elif sum_neighbors == -q:
                    _model[i, j] = -1
                    if Sij == 1:
                        N_plus -= 1
        yield _model, N_plus


def gen(N, N_plus, N_minus, p, q, f, type_of_choosing, independene):
    """Generowanie grafu i symulacja."""
    data = np.array([1] * N_plus + [-1] * N_minus)
    np.random.shuffle(data)
    red_green = {-1: "red", 1: "green"}
    color_map = [red_green[i] for i in data]

    G = nx.Graph()
    for i in range(N):
        G.add_node(i)
    persons = [i for i in range(N)]
    while True:
        person = persons.pop(np.random.randint(len(persons)))
        if type_of_choosing:
            neighbors = np.random.choice(persons, q)
        else:
            neighbors = r.sample(persons, q)

        for i in neighbors:
            G.add_edge(person, i)

        if independene:
            rnd = r.random()
            if rnd < p:
                if r.random() < f:
                    data[person] = -1
                else:
                    data[person] = 1
            else:
                sum_neighbors = np.sum([data[i] for i in neighbors])
                if sum_neighbors == q:
                    data[person] = 1
                elif sum_neighbors == -q:
                    data[person] = -1
        else:
            rnd = r.random()
            sum_neighbors = np.sum([data[i] for i in neighbors])
            if rnd < p:
                if sum_neighbors == q:
                    data[person] = -1
                elif sum_neighbors == -q:
                    data[person] = 1
            else:
                if sum_neighbors == q:
                    data[person] = 1
                elif sum_neighbors == -q:
                    data[person] = -1

        N_plus = np.sum(data == 1)
        yield G, color_map, N_plus / N
        G.remove_edges_from(G.edges())
        persons = [i for i in range(N)]
        color_map = [red_green[i] for i in data]
