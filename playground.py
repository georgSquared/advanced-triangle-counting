from networkx import gnm_random_graph, nx
import pandas as pd

from advanced_triangle_counting.doulion import doulion_node_iterator, doulion_nx
from advanced_triangle_counting.simple_triangle_counting import count_triangles


def main():

    df1 = pd.read_csv("../CA-GrQc2-small.csv")
    G = nx.from_pandas_edgelist(df1, source="FromNodeId", target="ToNodeId")
    print(f'number of triangles according to doulion: {doulion_node_iterator(G, p=0.3)}')


if __name__ == "__main__":
    main()
