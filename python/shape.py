import json as js
from multiprocessing.dummy import Pool as ThreadPool
from time import time

import numpy as np
from shapely.geometry import Point, Polygon

THREAD_COUNT = 8


def generate_polygons_raw(n=10, r=10, min_s=3, max_s=20):
    return [(r * np.random.randn(np.random.randint(min_s, max_s), 2)).tolist() for _ in range(n)]


def generate_polygons(n=10, r=10, min_s=3, max_s=20):
    return [Polygon(r * np.random.randn(np.random.randint(min_s, max_s), 2)) for _ in range(n)]


def generate_points_raw(n=10, r=10):
    return (r * np.random.randn(n, 2)).tolist()


def generate_points(n=10, r=10):
    return [Point(crd) for crd in r * np.random.randn(n, 2)]


def find_ids(input_data):
    polygons, point = input_data
    all_polys = []
    for index, polygon in enumerate(polygons):
        if polygon.contains(point):
            all_polys.append(index)
    return all_polys


def generate_file(poly_size=1300, point_size=1000):
    polygons = generate_polygons_raw(n=poly_size)
    points = generate_points_raw(n=point_size)
    js.dump({"points": points, "polygons": polygons}, open("result.json", "w"))


def generate_data(poly_size=1300, point_size=1000):
    print("> generating polygons")
    polygons = generate_polygons(n=poly_size)
    print("> generating points")
    points = generate_points(n=point_size)
    return polygons, points


def load_from_file(file="result.json"):
    data = js.load(open(file))
    polygons = [Polygon(poly) for poly in data["polygons"]]
    points = [Point(point) for point in data["points"]]
    return polygons, points


if __name__ == "__main__":
    from_file = True
    if from_file:
        polygons, points = load_from_file()
    else:
        polygons, points = generate_data()
    pool = ThreadPool(THREAD_COUNT)
    print("> data preprocessing")
    data = ((polygons, point) for point in points)
    print("> calculating")
    start = time()
    result = pool.map(find_ids, data)
    stop = time()
    print(f"--- DONE ---\ntime elapsed: {stop - start:.4f} seconds")

    with open("result-python.txt", "w") as f:
        for index, item in enumerate(result):
            f.write(f"{index}: {item}\n")
