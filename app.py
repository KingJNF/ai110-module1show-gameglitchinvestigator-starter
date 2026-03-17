import random
import streamlit as st

#FIXME:Should be fixed to be consistent with the difficulty settings, but the glitch is that it isn't.
def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str):
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

    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"
#FIX ME: The hints should be reversed. 
# If the guess is higher than the secret, it should say 
# "Too High" and if it's lower, it should say "Too Low". 
# The glitch is that it's currently reversed.
    try:
        if guess > secret:
            return "Too High", "� Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
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

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)
#FIX ME: This is where it should show the correct amount of attempts for each difficulty, but it doesn't. The glitch is that it shows 1 less the proper amount of attempts selected.
#FIX ME: Each difficulty should also have the proper amount of attempts linked to it.
attempt_limit_map = {
    "Easy": 10,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "last_hint" not in st.session_state:
    st.session_state.last_hint = None

if "show_new_game_message" not in st.session_state:
    st.session_state.show_new_game_message = False
if "should_reset_game" not in st.session_state:
    st.session_state.should_reset_game = False
if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

# Handle game reset if flagged
if st.session_state.should_reset_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.history = []
    st.session_state.last_hint = None
    st.session_state.status = "playing"
    st.session_state.show_new_game_message = True
    st.session_state.should_reset_game = False
    
    # Clear the text input field by setting it to empty string
    st.session_state[f"guess_input_{difficulty}"] = ""
    
    st.rerun()
st.subheader("Make a guess")

# Display new game message if it was triggered
if st.session_state.show_new_game_message:
    st.success("A new game has started.")
    st.session_state.show_new_game_message = False

# Display balloons animation if win was triggered
if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

#FIX ME: It should show the correct amount of attempts for each difficulty, but it doesn't. The glitch is it shows 1 less the proper amount of attempts selected.
#FIX ME: Have it show the correct range underneath the difficulty drop down menu and on the main page.
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

#FIX ME: I have to press the submit button twice to register the guess. 
#  Fixed it so you only have to press it once to register your guess.

with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        value=st.session_state.get(f"guess_input_{difficulty}", ""),
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

# Display any hint message from the previous submission
if st.session_state.last_hint:
    st.warning(st.session_state.last_hint)
    st.session_state.last_hint = None

col1, col2, col3 = st.columns(3)
#FIX ME: The new game button should reset the game immediately, 
# but it doesn't. The glitch is it only resets the amount of attempts
# but doesnt clear the history, the hint prompt or the last submitted 
# guess. I want it so it clears the text field, 
# resets the amount of attempts, 
# clears the history, the hint prompt if already on 
# screen and shows a new secret number. 
# Also show a new game started prompt.
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    st.empty()
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# Check if new game button was clicked
if new_game:
    st.session_state.should_reset_game = True
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.session_state.last_hint = message

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.session_state.show_balloons = True
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
    
    st.rerun()


st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
