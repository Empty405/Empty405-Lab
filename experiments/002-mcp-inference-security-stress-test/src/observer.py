from __future__ import annotations


def intersect_interval(interval: tuple[int, int], response: dict) -> tuple[int, int]:
    lower, upper = interval
    kind = response["kind"]
    value = response["value"]

    if kind == "availability":
        if value:
            lower = max(lower, 50)
        else:
            upper = min(upper, 49)

    elif kind == "band4":
        bounds = {
            "q1": (0, 24),
            "q2": (25, 49),
            "q3": (50, 74),
            "q4": (75, 100),
        }[value]
        lower = max(lower, bounds[0])
        upper = min(upper, bounds[1])

    elif kind == "band2":
        bounds = {
            "below_50": (0, 49),
            "at_least_50": (50, 100),
        }[value]
        lower = max(lower, bounds[0])
        upper = min(upper, bounds[1])

    elif kind == "range":
        lower = max(lower, value[0])
        upper = min(upper, value[1])

    return lower, upper


def reconstruct(true_value: int, responses: list[dict]) -> dict:
    interval = (0, 100)

    for response in responses:
        interval = intersect_interval(interval, response)

    lower, upper = interval
    remaining_width = max(0, upper - lower + 1)

    information_exposure = 1.0 - (remaining_width / 101.0)
    estimate = (lower + upper) / 2.0
    absolute_error = abs(true_value - estimate)

    return {
        "interval": [lower, upper],
        "information_exposure": information_exposure,
        "estimate": estimate,
        "absolute_error": absolute_error,
        "within_5": absolute_error <= 5,
    }
