from advanced_triangle_counting.random_sampling import RandomSampling


def test_initialize():
    random_sampling = RandomSampling(8, [(1, 2), (1, 6), (7, 2), (6, 7), (3, 8), (4, 8), (3, 4), (5, 8), (8, 7), (7, 5), (3, 2), (5, 4), (5, 6)])
    print(random_sampling.get_neighbours(0))
    print(random_sampling.get_common_neighbours(1, 7))
    print(random_sampling.vertex_sampling())
    print(random_sampling.edge_sampling())
    print(random_sampling.triangle_sampling())


if __name__ == '__main__':
    test_initialize()
