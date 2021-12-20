from networkx import gnm_random_graph

from advanced_triangle_counting.simple_triangle_counting import count_triangles


def main():
    random_graph = gnm_random_graph(10, 1000)
    triangles = count_triangles(random_graph)
    print(f"This random graph has {triangles} number of triangles")


if __name__ == "__main__":
    main()
