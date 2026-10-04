# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

A normal-looking number-guessing game at first sight. It prompts me to pick a difficulty (I assume most popular answers from social surveys or single digit numbers are easy and higher numbers are more difficult), I get a range of 1 to 100 and attempt limit, type a guess, and get a hint after each try. However, running it, I noticed that the hint is not useful, and I couldn't start a new game.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

1. Clicking "New Game" after winning or losing doesn't actually let you play again — the app still shows "You already won".
2. On some attempts, the "Too High"/"Too Low" hint is backwards relative to the actual secret number in the Developer Debug Info.
3. The guess prompt always said "Guess a number between 1 and 100" even on Easy/Hard difficulty (where the real range is 1-20 or 1-50), and the "Attempts left" counter started one attempt short before I had even made a guess.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Win a round, then click "New Game" | New round starts fresh: status resets to "playing", score/history is cleared, new secret drawn from the selected difficulty's range | App still shows "You already won. Start a new game to play again." and doesn't allow to keep playing; status is never reset back to "playing" | No error; logic bug |
| Guess on an even-numbered attempt | Hint direction should be based on a numeric comparison against the secret | Weirdly, the hint is sometimes backwards; the secret gets cast to a string on even attempts, so the comparison falls back to string ordering instead of numeric ordering | TypeError raised, but not visible because it's under try/except |
| -500 or 999999 as a guess | Guess should be rejected as outside the valid range for the difficulty | Guess is accepted as valid, consumes an attempt, and is scored normally | No error; missing range validation |
| Select "Easy" or "Hard" difficulty and read the guess prompt | Prompt should show the actual range for that difficulty (e.g. 1-20 or 1-50) | Prompt always said "Guess a number between 1 and 100", regardless of selected difficulty | No error; hardcoded text bug |
| Load the app fresh (no guesses made yet) on any difficulty | "Attempts left" should show the full attempt_limit (e.g. 8 on Normal) | Showed one less than the real limit (e.g. 7), because `attempts` was initialized to 1 instead of 0 | No error |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

Claude Sonnet 5 Medium.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

Claude suggested moving get_range_for_difficulty, parse_guess, and update_score out of app.py and into logic_utils.py (alongside check_guess), and importing all four back into app.py. I ran python -m pytest tests/test_game_logic.py -v and confirmed all tests still passed (21/21). I also ran the app itself and played a full round to confirm nothing broke.

Claude also caught two smaller flaws I hadn't flagged: the guess prompt hardcoding "1 and 100" instead of using the difficulty's actual low/high, and attempts being initialized to 1 instead of 0 (making "Attempts left" undercount by one before any guess was made). It fixed the st.info text to {low}/{high} and changed the initial attempts value to 0 in app.py. I verified by running the app on Easy and Hard difficulty and confirming the prompt text now matches the sidebar's stated range, and that "Attempts left" shows the full attempt limit on a fresh load.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

Claude Sonnet 5 recommended fixing the string-coercing bug (cast to str on even attepmts) after I requested to "update the logic to fix the high/low bug". I rejected and changed it because the real defect was that the hint messages were swapped relative to their outcome labels. I verified it by inspecting the code myself and a test that asserts the message text on top of checking the outcome label. Claude wasn't wrong, it just fixed a different, intermittent case.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

Using extra tests in test_game_logic.py, like test_guess_too_low_regression_for_string_comparison_bug() and test_guess_handles_string_secret(). I also cleared streamlit localhost cookies, restarted the app, and verified all the fixes manually, testing on a variety of inputs from the tests and beyond.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

I ran pytest test_game_logic.py, and when I updated the tests to assert the actual hint message text (not just the outcome label), it would have caught the swapped "Go HIGHER"/"Go LOWER" output bug that Claude's outcome-only assertions had missed.


- Did AI help you design or understand any tests? How?

Yes, Claude Sonnet 5 Medium helped draft some tests for check_guess, get_range_for_difficulty, parse_guess, and update_score. I was confused about test_parse_guess_none_rejected(), and it helped me understand that the test checks the runtime guard for parse_guess so it's correctly rejected with an error message.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit re-executes your entire script top to bottom every time you interact with a widget (click a button, type in a box, change a dropdown). It's not like a regular app you might be used to where only the part you touched updates. That means any plain Python variable resets to its initial value on every single interaction unless you explicitly store it in `st.session_state`, which is a dict-like object that is retained across reruns for that browser session. My takeaway best practice is: find the event that should change state, and explicitly write to `st.session_state` in that branch so nothing persists by accident, and nothing resets by accident either.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

  - This could be a testing habit, a prompting strategy, or a way you used Git.

    Writing tests that assert the output content and thinking about my test coverage more in-depth. I feel like I should not be afraid of generating new tests I do not yet understand to cover more failure modes and then attempt to understand them all. Going forward, I want to focus on what my tests miss instead of trusting a green checkmark.

- What is one thing you would do differently next time you work with AI on a coding task?

  I'd push back earlier and more specifically on AI claims of "fixed." Claude confidently said the high/low bug was resolved after only fixing the intermittent string-coercion issue, and I caught the bug (swapped messages) myself by playing the game. Next time I'd verify behavior against a real example before accepting a fix as done.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  AI-written code can look complete and pass a superficial read while hiding bugs that only show up when you actually exercise the logic with real inputs — confidence in an explanation is not the same as verification, and I now trust "it's fixed" less than I trust a comprehensive set of pytests.
