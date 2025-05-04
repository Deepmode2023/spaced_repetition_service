ONE_DAY_IN_SECONDS = 24 * 60 * 60
FORTY_MINUTES_IN_SECONDS = 40 * 60

REPETITION_RATE = 2.5
REPETITION_POST_RATE = 1


def repetition_formula(count_repetition: int) -> int:
    """
    Calculates time in seconds based on the number of repetitions.
    Args:
        count_repetition (int): The number of repetitions. If equal to 0, returns a fixed value.
    Returns:
        int: The calculated time in seconds.
    Raises:
        ValueError: If the passed argument is not an integer.
    """
    if not isinstance(count_repetition, int) or count_repetition < 0:
        raise ValueError("Attr count_repetition must be a non-negative integer!")

    if count_repetition == 0:
        return FORTY_MINUTES_IN_SECONDS

    return int(
        (REPETITION_RATE * count_repetition + REPETITION_POST_RATE) * ONE_DAY_IN_SECONDS
    )
