import argparse
import time

from advanced_triangle_counting.cst import (
    neighborhood_sampling,
    neighborhood_sampling_with_estimators,
)
from advanced_triangle_counting.simple_triangle_counting import count_triangles
from advanced_triangle_counting.utils import load_graph_from_file


def run_neighborhood():
    G = load_graph_from_file("../resources/CA-GrQc.txt")
    start_time = time.time()

    try:
        t, c, m = neighborhood_sampling(G)
    except ValueError as ex:
        end_time = time.time()
        print(f"Neighborhood sampling -> Took {end_time - start_time} seconds")
        raise

    end_time = time.time()
    print(f"Neighborhood sampling -> Took {end_time - start_time} seconds")

    return t, c, m


def run_neighborhood_with_estimators(estimators):
    start_time = time.time()
    G = load_graph_from_file("../resources/CA-GrQc.txt")
    results = neighborhood_sampling_with_estimators(G, estimators)
    found_count = 0

    total = 0
    for estimator in results:
        if not estimator["found"]:
            continue

        estimation = estimator["neighborhood_count"] * estimator["streamed_edges_count"]
        probability = 1 / estimators

        found_count = found_count + 1
        total = total + (estimation * probability)

    print(f"Found a triangle on {found_count} out of {estimators} estimators")
    print(f"Final results is {total} triangles")

    end_time = time.time()
    print(f"Overall sampling -> Took {end_time - start_time} seconds")


def main():
    parser = argparse.ArgumentParser(
        description="Delete non-activated users periodically"
    )
    parser.add_argument(
        "-r",
        "--estimators",
        dest="requested_estimators",
        default=None,
        type=int,
        help="Provide requested number of estimators",
    )
    args = parser.parse_args()

    if args.requested_estimators:
        run_neighborhood_with_estimators(args.requested_estimators)
    else:
        start_time = time.time()
        flag = True
        iterations = 0
        while flag:
            try:
                t, c, m = run_neighborhood()
                flag = False
            except ValueError as ex:
                print(ex)
                iterations = iterations + 1
                print(f"Iterations: {iterations}")

        end_time = time.time()
        print(f"Overall sampling -> Took {end_time - start_time} seconds")


if __name__ == "__main__":
    main()
