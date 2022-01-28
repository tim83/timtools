from __future__ import annotations  # python -3.9 compatibility

import concurrent.futures
import typing


def mt_filter(
    func: typing.Callable, collection: typing.Iterable, max_workers: int = 20
) -> list:
    filtered_collection = []

    def filter_item(item):
        if func(item) is True:
            filtered_collection.append(item)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(filter_item, collection)

    return filtered_collection


def mt_map(
    func: typing.Callable, collection: typing.Iterable, max_workers: int = 20
) -> typing.Iterable:
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        executor.map(func, collection)

    return collection
