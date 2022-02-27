import numpy as np

from advanced_triangle_counting.utils import stream_edge


def is_triangle(edge_a, edge_b, edge_c):
    not_connected_nodes = set(edge_a) ^ set(edge_b)
    return sorted(edge_c) == sorted(not_connected_nodes)


def neighborhood_sampling(G):
    first_level_edge = ()
    second_level_edge = ()
    sampled_triangle = ()
    neighborhood_count = 0
    streamed_edges_count = 0
    while True:
        G, edge = stream_edge(G)
        if not G or not edge:
            raise ValueError("No triangles found")

        streamed_edges_count = streamed_edges_count + 1
        p = float(1 / streamed_edges_count)
        coin = np.random.choice([True, False], p=[p, 1 - p])
        if coin:
            first_level_edge = edge if coin else ()
            print(f"Got r1: {first_level_edge}")
        else:
            # Check adjacency of edges
            if (edge[0] in first_level_edge) or (edge[1] in first_level_edge):
                neighborhood_count += 1
                p = float(1 / neighborhood_count)
                coin = np.random.choice([True, False], p=[p, 1 - p])
                if coin:
                    second_level_edge = edge
                    print(f"Got r2: {second_level_edge}")
                else:
                    if is_triangle(first_level_edge, second_level_edge, edge):
                        sampled_triangle = set(
                            first_level_edge + second_level_edge + edge
                        )
                        print(f"Got triangle: {sampled_triangle}")
                        print(
                            f"With streamed edges {streamed_edges_count} and neighborhood length {neighborhood_count}"
                        )

                        return (
                            sampled_triangle,
                            neighborhood_count,
                            streamed_edges_count,
                        )


def neighborhood_sampling_with_estimators(G, num_of_estimators):
    estimators = []
    for i in range(num_of_estimators):
        estimators.append(
            {
                "first_level_edge": (),
                "second_level_edge": (),
                "sampled_triangle": set(),
                "neighborhood_count": 0,
                "streamed_edges_count": 0,
                "found": False,
            }
        )

    while True:
        G, edge = stream_edge(G)
        if not G or not edge:
            return estimators

        for r in estimators:
            if r["found"]:
                continue

            r["streamed_edges_count"] = r["streamed_edges_count"] + 1
            p = float(1 / r["streamed_edges_count"])
            coin = np.random.choice([True, False], p=[p, 1 - p])
            if coin:
                r["first_level_edge"] = edge if coin else ()
            else:
                # Check adjacency of edges
                if (edge[0] in r["first_level_edge"]) or (
                    edge[1] in r["first_level_edge"]
                ):
                    r["neighborhood_count"] += 1
                    p = float(1 / r["neighborhood_count"])
                    coin = np.random.choice([True, False], p=[p, 1 - p])
                    if coin:
                        r["second_level_edge"] = edge
                        # print(f"Got r2: {second_level_edge}")
                    else:
                        if is_triangle(
                            r["first_level_edge"], r["second_level_edge"], edge
                        ):
                            r["sampled_triangle"] = set(
                                r["first_level_edge"] + r["second_level_edge"] + edge
                            )
                            print(
                                f"An estimator got a triangle: {r['sampled_triangle']}"
                            )
                            print(
                                f"With streamed edges {r['streamed_edges_count']} and neighborhood length {r['neighborhood_count']}"
                            )

                            r["found"] = True
