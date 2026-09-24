# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

A normal-looking number-guessing game at first sight. It prompts me to pick a difficulty (I assume most popular answers from social surveys or single digit numbers are easy and higher numbers are more difficult), I get a range of 1 to 100 and attempt limit, type a guess, and get a hint after each try. However, running it, I noticed that the hint is not useful, and I couldn't start a new game.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

1. Clicking "New Game" after winning or losing doesn't actually let you play again — the app still shows "You already won".
2. On some attempts, the "Too High"/"Too Low" hint is backwards relative to the actual secret number in the Developer Debug Info.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Win a round, then click "New Game" | New round starts fresh: status resets to "playing", score/history is cleared, new secret drawn from the selected difficulty's range | App still shows "You already won. Start a new game to play again." and doesn't allow to keep playing; status is never reset back to "playing" | No error — logic bug |
| Guess on an even-numbered attempt | Hint direction should be based on a numeric comparison against the secret | Weirdly, the hint is sometimes backwards; the secret gets cast to a string on even attempts, so the comparison falls back to string ordering instead of numeric ordering | TypeError raised, but not visible because it's under try/except |
| -500 or 999999 as a guess | Guess should be rejected as outside the valid range for the difficulty | Guess is accepted as valid, consumes an attempt, and is scored normally | No error — missing range validation |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
