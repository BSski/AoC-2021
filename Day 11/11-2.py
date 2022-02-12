"""
2021: Day 11, part two.
https://adventofcode.com/2021/day/11
Finds the number of steps until total flash synchronization.
"""
import time
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


def get_input_list_from_file(input_name: str) -> list[int]:
    with open(input_name, "r") as input_:
        input_list = list(input_)
        input_list = list(map(lambda a: a.strip("\n"), input_list))
        input_list = list(map(lambda a: list(map(int, a)), input_list))
        surrounding_zeros = [0] * (len(input_list) + 2)
        input_list = [[0, *line, 0] for line in input_list]
        input_list = [surrounding_zeros[:], *input_list, surrounding_zeros[:]]
        return input_list


def create_blinked_matrix(input_list: list[int]) -> list[int]:
    return [[0 for _ in range(len(line))] for line in input_list]


def reset_blinked(input_list: list[int]) -> list[int]:
    for line_idx, line in enumerate(input_list):
        for elem_idx, elem in enumerate(line):
            if elem > 9:
                line[elem_idx] = 0
    return input_list


def increase_by_one(input_list: list[int]) -> list[int]:
    for line_idx in range(1, len(input_list) - 1):
        for elem_idx in range(1, len(input_list[line_idx]) - 1):
            input_list[line_idx][elem_idx] += 1
    return input_list


def blink(
    input_list: list[int], blinked_matrix: list[bool]
) -> tuple[list[int], list[bool]]:
    for line_idx in range(1, len(input_list) - 1):
        for elem_idx in range(1, len(input_list[line_idx]) - 1):
            if input_list[line_idx][elem_idx] < 10:
                continue
            if blinked_matrix[line_idx][elem_idx]:
                continue
            for y in range(-1, 2):
                for x in range(-1, 2):
                    input_list[line_idx + y][elem_idx + x] += 1
            blinked_matrix[line_idx][elem_idx] = 1

    return input_list, blinked_matrix


def check_blink_potential(input_list: list[int], blinked_matrix: list[bool]) -> bool:
    tens = 0
    coords = []
    for line_idx in range(1, len(input_list) - 1):
        for elem_idx in range(1, len(input_list[line_idx]) - 1):
            if (
                input_list[line_idx][elem_idx] >= 10
                and not blinked_matrix[line_idx][elem_idx]
            ):
                tens += 1
                coords.append([line_idx, elem_idx])
    return True if tens > 0 else False


def check_if_synchronized(input_list: list[int]) -> bool:
    for line_idx in range(1, len(input_list) - 1):
        for elem_idx in range(1, len(input_list[line_idx]) - 1):
            if input_list[line_idx][elem_idx] != 0:
                return False
    return True


@time_it
def calculate_solution(input_name: str) -> int:
    input_list = get_input_list_from_file(input_name)

    steps = 0
    while not check_if_synchronized(input_list):
        blinked_matrix = create_blinked_matrix(input_list)
        input_list = increase_by_one(input_list)

        while check_blink_potential(input_list, blinked_matrix):
            input_list, blinked_matrix = blink(input_list, blinked_matrix)
        input_list = reset_blinked(input_list)
        steps += 1
    return steps


if __name__ == "__main__":
    print("Score:", calculate_solution("11 input.txt"))
