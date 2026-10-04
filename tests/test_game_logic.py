from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win with a
    # popup message announcing the win.
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "won" in message.lower()


def test_guess_too_high():
    # If secret is 50 and guess is 60, the guess overshot, so the hint
    # must tell the player to go LOWER.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_guess_too_low():
    # If secret is 50 and guess is 40, the guess undershot, so the hint
    # must tell the player to go HIGHER.
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_guess_too_low_regression_for_string_comparison_bug():
    # Regression test: secret=80, guess=9 used to be compared as strings
    # ("9" > "80" is True lexicographically), giving the wrong "Too High"
    # hint. Numerically, 9 < 80, so this must be "Too Low".
    outcome, _ = check_guess(9, 80)
    assert outcome == "Too Low"


def test_guess_handles_string_secret():
    # check_guess should coerce secret to int even if a string sneaks in,
    # instead of falling back to lexicographic comparison.
    outcome, _ = check_guess(9, "80")
    assert outcome == "Too Low"


# --- check_guess warmth hint -------------------------------------------

def test_check_guess_without_range_has_no_warmth_hint():
    # Without low/high, the message should be unchanged (backwards compatible).
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "🔥" not in message and "❄️" not in message


def test_check_guess_very_close_guess_is_hot():
    # Range 1-100, secret 50, guess 52: distance 2 is within 5% of the span.
    outcome, message = check_guess(52, 50, 1, 100)
    assert outcome == "Too High"
    assert "Very close" in message


def test_check_guess_far_guess_is_cold():
    # Range 1-100, secret 50, guess 95: distance 45 is way more than 35% of the span.
    outcome, message = check_guess(95, 50, 1, 100)
    assert outcome == "Too High"
    assert "Way off" in message


def test_check_guess_mid_distance_guess_is_warm():
    # Range 1-100, secret 50, guess 60: distance 10 is within 15% of the span.
    outcome, message = check_guess(60, 50, 1, 100)
    assert outcome == "Too High"
    assert "Warm" in message


# --- get_range_for_difficulty ---------------------------------------------

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)


def test_range_unknown_difficulty_falls_back_to_normal():
    # An unrecognized difficulty string should not crash the game; it
    # should fall back to the Normal range.
    assert get_range_for_difficulty("Nightmare") == (1, 100)


# --- parse_guess ------------------------------------------------------------

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42", 1, 100)
    assert ok is True
    assert value == 42
    assert err is None


def test_parse_guess_valid_float_truncates():
    # A decimal entry like "42.9" should parse to an int via float().
    ok, value, err = parse_guess("42.9", 1, 100)
    assert ok is True
    assert value == 42


def test_parse_guess_empty_string_rejected():
    ok, value, err = parse_guess("", 1, 100)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_none_rejected():
    ok, value, err = parse_guess(None, 1, 100)
    assert ok is False
    assert err is not None


def test_parse_guess_non_numeric_rejected():
    ok, value, err = parse_guess("banana", 1, 100)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_below_range_rejected():
    ok, value, err = parse_guess("-5", 1, 100)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_above_range_rejected():
    ok, value, err = parse_guess("999999", 1, 100)
    assert ok is False
    assert value is None
    assert err is not None


def test_parse_guess_boundary_values_accepted():
    # The low and high bounds themselves should be valid guesses, not
    # off-by-one rejected.
    ok_low, value_low, _ = parse_guess("1", 1, 100)
    ok_high, value_high, _ = parse_guess("100", 1, 100)
    assert ok_low is True and value_low == 1
    assert ok_high is True and value_high == 100


# --- update_score -------------------------------------------------------

def test_update_score_win_awards_points():
    # Winning on attempt 1 should score higher than winning on attempt 5.
    early_win = update_score(current_score=0, outcome="Win", attempt_number=1)
    late_win = update_score(current_score=0, outcome="Win", attempt_number=5)
    assert early_win > late_win


def test_update_score_win_never_drops_below_floor():
    # Even on a very late attempt, winning should never score below the
    # 10-point floor.
    score = update_score(current_score=0, outcome="Win", attempt_number=50)
    assert score == 10


def test_update_score_too_low_subtracts_points():
    score = update_score(current_score=50, outcome="Too Low", attempt_number=1)
    assert score == 45


def test_update_score_unknown_outcome_leaves_score_unchanged():
    score = update_score(current_score=50, outcome="Unknown", attempt_number=1)
    assert score == 50
