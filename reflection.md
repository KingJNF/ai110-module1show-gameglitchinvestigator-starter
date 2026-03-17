# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

1) The different modes start with one less attempt than stated in the left column.
    - Easy mode starts with 5 attempts instead of 6.
    - Normal mode starts with 7 attempts instead of 8.
    - Hard mode starts with 4 attempts instead of 5.
    Each mode should show the correct number of attempts, and the harder the difficulty, the fewer attempts the player should have.

2) Hard currently shows a range of 1-50 while Normal mode shows a range of 1-100. Normal and hard should have the ranges reversed.

3) In its current state, Hard mode shouldn't recognize a number above 50, yet if I put in, for example, the number 75, I get the prompt to Go HIGHER!

4) The secret number as shown in the Debug Info section might be a number out of the range of the current difficulty. For example, on Hard mode, the max number is 50, yet it showed me on separate occasions, 51, 75, and 89 as the secret number. The difficulty chosen should limit the secret number to whatever its range consists of.

5) Also, the secret number should change when the difficulty is changed. It currently stays the same.

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  I used CoPilot and Claude Code.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  When I highlighted the "check_guess" function and asked CoPilot to explain the logic, it correctly identified that the hint messages were swapped. "Go HIGHER" was paired with the "guess > secret" condition when it should have said, "Go LOWER". I fixed the messages. I verified it was correct by playing the game and confirming the hints now showed the correct message.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  Initially, when I put into CoPilot to fix the "update_score" function, it initially suggested removing the penalty entirely for wrong guesses instead of making it consistent. This would have made it not match the intended game design. I asked it again, but this time had it provide a more targeted fix and the -5 penalty for all wrong guesses while only fixing the inconsistent +5 on even attempts.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
    I tested it using a test script added to the code and checked the website itself. I also manually tested, from the user/player's point of view, that the code was running correctly.

-Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
  I wrote a test for the reversed hints bug: The test was called "check_guess(60, 50)". It showed the outcome was "Too High" and the message contained "LOWER (not HIGHER) ". I also tested "check_guess (30, 50)" to confirm it returned "Too Low" with a "HIGHER" message. Both tests passed after my fix, confirming the hint logic was corrected.

- Did AI help you design or understand any tests? How?
  AI helped me design edge-case tests I hadn't thought of, passing a string-type secret to "check_guess" to verify the type coercion bug was resolved. This helped me understand that the original code had a fallback path for TypeError that was masking the real issue.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
  In the original app, the secret number was generated using "random.randint()" at the top level of the script. Since Streamlit reruns the entire script from top to bottom every time the user interacts with any widget, a new random number is generated on every single click. Every time you pressed "Submit Guess", the secret number you were trying to guess silently changed to a completely different number, making the game nearly impossible to win.

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  Imagine every time you click a button on a webpage, the entire app resets and rebuilds itself from scratch. That is what Streamlit does on every interaction. Any normal variable you created gets wiped out and recreated, as if it never existed. Session states are like a special storage locker that survives these resets, so you can use them to save important info like scores, game data, or user inputs, and they'll still be there after the page rebuilds. Without it, the app would forget everything the user did after a single click.

- What change did you make that finally gave the game a stable secret number?
    The change was done by wrapping the secret number generation inside a session state check. This ensures the secret number is generated only once when the app runs for the first time. On every other run, the "if" check sees "secret" already exists in the session state and skips a generation, keeping the number stable throughout the entire game session.

---

## 5. Looking ahead: your developer habits DONE

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
    One habit would be to test the code I've used so far. Also, to see if there is a more efficient or less memory-intensive way to structure the code so it's less demanding on the end user's device and/or browser.


- What is one thing you would do differently next time you work with AI on a coding task?
 I would use it more frequently from the beginning of a coding task during the planning phase. Currently, I only use it when there is an error or I am uncertain how to continue.


- In one or two sentences, describe how this project changed the way you think about AI-generated code.
AI-generated code works and gets the task done, but it might not always do so in the most efficient manner possible, much like code written by an actual programmer. Also, the more detailed you are in your prompt, the more likely it is that the AI will give you what you're looking for.