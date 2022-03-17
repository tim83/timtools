"""Module containing tools for multithreading"""
from __future__ import annotations  # python -3.9 compatibility

import concurrent.futures
import typing


def mt_filter(
    func: typing.Callable, collection: typing.Iterable, max_workers: int = 20
) -> list:
    """
    Filters a list based on a function, using multithreading
    :param func: The function to be used as a filter,
    must return a boolean value for each element in the collection
    :param collection: The collection to filter
    :param max_workers: The maximum number of threads to use
    :return: A filtered list
    """
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
    """
    Executes a function for every element in a collection, using multithreading
    :param func: The function to execute on every element
    :param collection: The collection of elements
    :param max_workers: The maximum number of threads to use
    :return: The collection of processed elements
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        executor.map(func, collection)

    return collection
