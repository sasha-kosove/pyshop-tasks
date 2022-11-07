import math
import random
from pprint import pprint
from typing import Callable

TIMESTAMPS_COUNT = 50000

PROBABILITY_SCORE_CHANGED = 0.0001

PROBABILITY_HOME_SCORE = 0.45

OFFSET_MAX_STEP = 3

INITIAL_STAMP = {"offset": 0, "score": {"home": 0, "away": 0}}


def generate_stamp(previous_value):
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED
    home_score_change = (
        1 if score_changed and random.random() > 1 - PROBABILITY_HOME_SCORE else 0
    )
    away_score_change = 1 if score_changed and not home_score_change else 0
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    return {
        "offset": previous_value["offset"] + offset_change,
        "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change,
        },
    }


def generate_game():
    stamps = [
        INITIAL_STAMP,
    ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps


def rbinsearch(
    left_idx: int,
    right_idx: int,
    check: Callable[[int, tuple], bool],
    *checkparams: tuple
) -> int:
    while left_idx < right_idx:
        middle_idx = (left_idx + right_idx + 1) // 2
        if check(middle_idx, *checkparams):
            left_idx = middle_idx
        else:
            right_idx = middle_idx - 1
    return left_idx


def check_stamp(middle_idx: int, *params: tuple) -> bool:
    game_stamps, offset = params
    return game_stamps[middle_idx]["offset"] <= offset


def get_score(game_stamps: dict, offset: int) -> tuple:
    """
    Поскольку в задании не сказано о том, как обрабатывать различные смещения, мне показалось логичным,
    что отрицательное смещение поднимает ошибку, смещение большее чем последнее сгенерированное возвращает
    счет последнего сгенерированного. При этом, если убрать условие с отрицательным смещением, при любом
    отрицательном будет просто возвращаться счет INITIAL_STAMP. В остальном, любое отсутствующее в списке
    смещение возвращает счет ближайшего слева.
    """
    if offset < 0:
        raise ValueError("Offset cannot be a negative number")

    time_stamp_idx = rbinsearch(
        0, len(game_stamps) - 1, check_stamp, game_stamps, offset
    )
    return (
        game_stamps[time_stamp_idx]["score"]["home"],
        game_stamps[time_stamp_idx]["score"]["away"],
    )


if __name__ == "__main__":
    game_stamps = generate_game()
    pprint(game_stamps)
    print(get_score(game_stamps, 50000))
