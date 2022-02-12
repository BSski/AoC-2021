"""
2021: Day 14, part two.
https://adventofcode.com/2021/day/14
Finds quantity of the most common element minus the quantity of the least
common element in the result string of 40 steps of polymerization.
"""
import time
from collections import Counter
from functools import lru_cache
from typing import Callable, ParamSpec, TypeVar


P = ParamSpec("P")
R = TypeVar("R")


def time_it(func: Callable[P, R]) -> Callable[P, R]:
    def _wrap(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print("Elapsed time:", round(end_time - start_time, 3))
        return result

    return _wrap


def get_input_list_from_file(input_name: str) -> tuple[str, dict[str, str]]:
    with open(input_name, "r") as input_:
        input_list = list(input_)
        polymer_template = input_list[0].strip("\n")

        input_list = input_list[2:]
        input_list = list(map(lambda a: a.strip("\n"), input_list))
        input_list = list(map(lambda a: a.split(" -> "), input_list))

        insertion_rules = dict(input_list)

        return polymer_template, insertion_rules


@time_it
def calculate_solution(input_name: str) -> int:
    polymer_template, insertion_rules = get_input_list_from_file(input_name)

    @lru_cache(maxsize=None)
    def generate_next_pair_and_count(depth, two_letters) -> str:
        x = insertion_rules[two_letters]
        new_counter = Counter(x)
        if depth == 1:
            return new_counter
        new_counter.update(
            generate_next_pair_and_count(depth - 1, f"{two_letters[0]}{x}")
        )
        new_counter.update(
            generate_next_pair_and_count(depth - 1, f"{x}{two_letters[1]}")
        )
        return new_counter

    result_counter = Counter(polymer_template)
    depth = 40
    for idx, _ in enumerate(polymer_template):
        if idx == len(polymer_template) - 1:
            break
        result_counter.update(
            generate_next_pair_and_count(
                depth, polymer_template[idx] + polymer_template[idx + 1]
            )
        )

    return max(result_counter.values()) - min(result_counter.values())


if __name__ == "__main__":
    print(
        "The most common element minus the least common element: ",
        calculate_solution("14 input.txt"),
    )
