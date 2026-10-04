# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Add a progressive "warmer/colder" hint to the game, based on how close the guess is to the secret, on top of the existing Too High/Too Low hint.

**What did the agent do?**

Added a `_warmth_hint` helper in `logic_utils.py` that compares `abs(guess - secret)` to the range size and picks a tier (Very close / Warm / Getting warmer / Way off). Changed `check_guess` to take optional `low`/`high` and append the warmth tier to the message. Added 4 new tests, ran the full suite (25 passed), and launched the app headless.

**What did you have to verify or fix manually?**

I played a full round myself to check the hint tiers actually feel right at different distances. I also checked that old calls to `check_guess` without a range (plain `check_guess(guess, secret)`) still work with no warmth text, since other code and tests rely on that.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Guess equals secret | "Move the check_guess function to logic_utils.py, update the logic to fix the high/low bug, and update the import in app.py. Confirm that it still works fine with a simple test..." | `test_winning_guess` | Yes | Check that a win is detected at all. |
| Guess above secret | (same prompt as above) | `test_guess_too_high` | Yes | Check for the "too high" branch before testing edge cases. |
| Guess below secret | (same prompt as above) | `test_guess_too_low` | Yes | Check for the "too low" branch before testing edge cases. |
| Two-digit numbers where string comparison would misorder them (guess=9, secret=80) | (same prompt as above) | `test_guess_too_low_regression_for_string_comparison_bug` | Yes | "9" > "80" as strings but not as numbers. Catches the old bug coming back. |
| Secret passed in as a string instead of int | (same prompt as above) | `test_guess_handles_string_secret` | Yes | Secret used to get cast to a string sometimes. Make sure that can't break it anymore. |
| Valid integer / float-string guess | (same prompt as above) | `test_parse_guess_valid_integer`, `test_parse_guess_valid_float_truncates` | Yes | Basic happy-path input, including decimals like "42.9". |
| Empty string / `None` input | (same prompt as above) | `test_parse_guess_empty_string_rejected`, `test_parse_guess_none_rejected` | Yes | Streamlit can hand back "" or None, both need to be rejected. |
| Non-numeric input | (same prompt as above) | `test_parse_guess_non_numeric_rejected` | Yes | Typos like "banana" should be rejected, not crash. |
| Below/above the difficulty's range | (same prompt as above) | `test_parse_guess_below_range_rejected`, `test_parse_guess_above_range_rejected` | Yes | These used to be accepted with no range check at all. |
| Exact boundary values (`low` and `high` themselves) | (same prompt as above) | `test_parse_guess_boundary_values_accepted` | Yes | Off-by-one is easy to get wrong, make sure the edges still count as valid. |
| Win scoring decreases with later attempts | (same prompt as above) | `test_update_score_win_awards_points` | Yes | Winning early should score more than winning late. |
| Win scoring floor | (same prompt as above) | `test_update_score_win_never_drops_below_floor` | Yes | Score shouldn't go below the 10-point floor on a very late win. |
| "Too Low" scoring | (same prompt as above) | `test_update_score_too_low_subtracts_points` | Yes | Simple check that guessing too low deducts points. |
| Unrecognized outcome string | (same prompt as above) | `test_update_score_unknown_outcome_leaves_score_unchanged` | Yes | An outcome that isn't Win/Too High/Too Low shouldn't change the score. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
