from logic_utils import check_guess

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
