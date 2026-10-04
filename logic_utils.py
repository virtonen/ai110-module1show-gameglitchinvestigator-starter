def get_range_for_difficulty(difficulty: str):
    """
    Return the inclusive (low, high) guessing range for a difficulty.

    Args:
        difficulty: One of "Easy", "Normal", "Hard". Any other value
            (including unrecognized or misspelled difficulties) falls
            back to the "Normal" range rather than raising.

    Returns:
        A tuple (low, high) of ints, where low <= high.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Nightmare")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int, high: int):
    """
    Parse and validate a raw text guess against the allowed range.

    Accepts plain integers ("42") and decimal strings ("42.9", truncated
    via int(float(...))). Rejects missing/empty input, non-numeric input,
    and any value outside the inclusive [low, high] range.

    Args:
        raw: The raw text entered by the player (may be None or "").
        low: Inclusive lower bound of the valid guess range.
        high: Inclusive upper bound of the valid guess range.

    Returns:
        A tuple (ok, guess_int, error_message):
            - (True, int, None) if raw parsed to a valid in-range guess.
            - (False, None, str) with a user-facing error message otherwise.

    Examples:
        >>> parse_guess("42", 1, 100)
        (True, 42, None)
        >>> parse_guess("banana", 1, 100)
        (False, None, 'That is not a number.')
        >>> parse_guess("999", 1, 100)
        (False, None, 'Enter a number between 1 and 100.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: reject guesses outside the difficulty's range, which
    # previously had no validation at all (manual mode, per my
    # instruction to Claude Sonnet 5)
    if value < low or value > high:
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def _warmth_hint(guess: int, secret: int, low: int, high: int):
    """
    Return a distance-based "warmer/colder" hint for a guess.

    The guess-to-secret distance is expressed as a fraction of the full
    guessing range (high - low), then bucketed into a tier so the hint
    scales consistently across difficulties with different range sizes.

    Args:
        guess: The player's (already int-coerced) guess.
        secret: The secret number (already int-coerced).
        low: Inclusive lower bound of the guessing range.
        high: Inclusive upper bound of the guessing range.

    Returns:
        A short emoji + text hint string, or "" if the range is degenerate
        (high <= low, so a distance ratio can't be computed).
    """
    span = high - low
    if span <= 0:
        return ""

    distance_ratio = abs(guess - secret) / span

    if distance_ratio <= 0.05:
        return "🔥🔥 Very close!"
    if distance_ratio <= 0.15:
        return "🔥 Warm!"
    if distance_ratio <= 0.35:
        return "🙂 Getting warmer"
    return "❄️ Way off"


def check_guess(guess, secret, low=None, high=None):
    """
    Compare a guess to the secret number and return the outcome and hint.

    Both guess and secret are coerced to int before comparing, so this is
    safe to call even if a caller accidentally passes a numeric string.

    Args:
        guess: The player's guess (int or numeric string/value).
        secret: The secret number (int or numeric string/value).
        low: Optional inclusive lower bound of the guessing range. When
            given together with high, the message includes a distance-based
            "warmer/colder" hint (see _warmth_hint) alongside the direction.
        high: Optional inclusive upper bound of the guessing range.

    Returns:
        A tuple (outcome, message):
            - outcome is one of "Win", "Too High", "Too Low".
            - message is the user-facing hint text to display.

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct, you won!')
        >>> check_guess(60, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(52, 50, 1, 100)
        ('Too High', '📉 Go LOWER! 🔥🔥 Very close!')
    """
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct, you won!"

    if guess > secret:
        outcome, message = "Too High", "📉 Go LOWER!"
    else:
        outcome, message = "Too Low", "📈 Go HIGHER!"

    if low is not None and high is not None:
        message = f"{message} {_warmth_hint(guess, secret, low, high)}"

    return outcome, message


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Apply the score delta for one guess's outcome.

    Scoring rules:
        - "Win": awards (100 - 10 * (attempt_number + 1)) points, floored
          at 10 so a very late win still scores something.
        - "Too High": +5 points on an even attempt_number, -5 otherwise
          (an intentional quirk of this game's scoring, not a typo).
        - "Too Low": always -5 points.
        - Any other outcome: score is returned unchanged.

    Args:
        current_score: The player's score before this guess.
        outcome: The result of check_guess, e.g. "Win", "Too High", "Too Low".
        attempt_number: The 1-based count of guesses made so far, used to
            scale the win bonus and to pick the Too-High branch.

    Returns:
        The updated integer score.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(0, "Win", 50)
        10
        >>> update_score(50, "Too Low", 1)
        45
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
