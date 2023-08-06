import random
import time


def sleep_random(min_s: int, max_s: int, unit: int = 1) -> None:
    seconds = random.randint(min_s, max_s)
    time.sleep(seconds * unit)


def find_or_steal_money(initial, target):
    current = initial
    loop = 0
    while current < target:
        sleep_random(1, 3, 0.1)
        current += 1
        loop += 1
        if loop > 50:
            return current
    return current


def build_boat() -> None:
    sleep_random(4, 14)


def steal_boat() -> None:
    sleep_random(8, 19)


def find_crew() -> None:
    sleep_random(4, 10)


def find_parrot() -> None:
    if random.randint(1, 2) == 1:
        raise ValueError("Failed!")
    sleep_random(1, 25)
