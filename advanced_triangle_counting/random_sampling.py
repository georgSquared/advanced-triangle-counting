import random


class RandomSampling:
    verticesNames: []
    verticesPointers: []
    edgesArray: []

    def __init__(self, n, edges):
        self.n = n
        self.verticesNames = list(range(0, n))
        neighbour_list = [[] for x in range(n)]
        m = 0
        for (u, v) in edges:
            neighbour_list[u - 1].append(v)
            neighbour_list[v - 1].append(u)
            m += 1
        self.m = m
        vertices_pointers = []
        edges_array = []
        for vertex, neighbours in enumerate(neighbour_list):
            neighbours.sort()
            vertices_pointers.append(len(edges_array))
            for v in neighbours:
                edges_array.append(v)
        self.verticesPointers = vertices_pointers
        self.edgesArray = edges_array

    def random_sample(self, amount):
        if amount is None or amount == 0:
            return [random.randint(0, self.n - 1)]
        elif amount < 0:
            print("Please give a valid number")
        elif amount < 1:
            number_of_vertices = int(self.n * amount) + 1
            return random.sample(self.verticesNames, number_of_vertices)
        elif amount > self.n:
            amount = self.n
        return random.sample(self.verticesNames, amount)

    def get_neighbours(self, u):
        index = self.verticesPointers[u]
        length = self.verticesPointers[u + 1] if len(self.verticesPointers) - 1 != u else len(self.edgesArray)
        return self.edgesArray[index:length]

    def get_common_neighbours(self, u, v):
        n_u = self.get_neighbours(u)
        n_v = self.get_neighbours(v)
        return list(set(n_u).intersection(n_v))

    def vertex_sampling(self, amount=0):
        t = 0
        samples = self.random_sample(amount)
        for v in samples:
            for v_i in self.get_neighbours(v):
                t = t + len(self.get_common_neighbours(v, v_i - 1))
        return t * self.n / (6 * len(samples))

    def edge_sampling(self, amount=0):
        total_l = 0
        samples = self.random_sample(amount)
        for u in samples:
            n_u = self.get_neighbours(u)
            if len(n_u) == 0:
                continue
            v = random.choice(n_u) - 1
            l_e = len(self.get_common_neighbours(u, v))
            total_l += l_e
        return total_l * len(self.edgesArray) / (3 * len(samples))

    def triangle_sampling(self, amount=0):
        score = 0
        samples = self.random_sample(amount)
        for u in samples:
            n_u = self.get_neighbours(u)
            if len(n_u) == 0:
                continue
            v = random.choice(n_u) - 1
            n_v = self.get_neighbours(v)
            i = random.randint(0, len(n_u) + len(n_v) - 1)
            t = 0
            if i < len(n_u):
                w = n_u[i]
                if w in n_v:
                    t += 1
            else:
                w = n_v[i - len(n_u)]
                if w in n_u:
                    t += 1
            score += t * len(n_u) * len(n_v) * len(self.edgesArray) / 6
        return score / len(samples)

