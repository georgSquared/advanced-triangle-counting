import random
import pandas as pd
import numpy as np

# User input momery size
FIXED_MEMORY_SIZE = 150000

# Edges
S = pd.read_csv("facebook_combined.txt")

dataset = []

for i in range(len(S)):
    dataset.append(S.iloc[i, 0].split())

new_dataset = []
triangle_dataset = dict()
neighboors_dataset = dict()

# init local triangle counting dictionary
for i in dataset:
    for j in i:
        triangle_dataset[j] = 0
        neighboors_dataset[j] = []

# init neigboor dictionary
for i in dataset:
    neighboors_dataset[i[0]].append(i[1])

triangle_global = 0


def triest():
    global new_dataset
    t = 0

    for i in dataset:
        t += 1
        if sample_edge(i, t):
            new_dataset.append(i)
            update_counters("+", i)

    return 0


def sample_edge(edge, t):
    global dataset, FIXED_MEMORY_SIZE
    if t <= FIXED_MEMORY_SIZE:
        return True
    elif random.random() < FIXED_MEMORY_SIZE / t:
        uniformly_value = int(random.uniform(0, len(dataset) - 1))
        dataset.pop(uniformly_value)
        update_counters("-", i)
        return True
    else:
        return False

    pass


def update_counters(case, i):
    global triangle_dataset, triangle_global
    union = intersection(neighboors_dataset[i[0]], neighboors_dataset[i[1]])
    if case == "+":
        for nodes in union:
            triangle_global += 1
            triangle_dataset[nodes] += 1
            triangle_dataset[i[0]] += 1
            triangle_dataset[i[1]] += 1
    else:
        for nodes in union:
            triangle_global -= 1
            triangle_dataset[nodes] -= 1
            triangle_dataset[i[0]] -= 1
            triangle_dataset[i[1]] -= 1


def intersection(x1, x2):
    return [x for x in x1 if x in x2]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    actual_triangles = 1612010
    triangles = triest()
    print(triangle_global - actual_triangles)
