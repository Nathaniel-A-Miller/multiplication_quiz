import streamlit as st
import random
import time

st.set_page_config(page_title="Hamster Multiplication", page_icon="🐹")
st.title("🐹 Multiplication Practice")

# Initialize session state once
if "initialized" not in st.session_state:
    st.session_state.update({
        "num_1": None,
        "numbers": [],
        "current_index": 0,
        "correct": 0,
        "start_time": None,
        "finished": False,
        "show_feedback": False,
        "last_feedback": ("", ""),         # (kind, message)
        "last_grid_lines": [],             # list of strings (rows)
        "last_user_answer": None,
        "last_correct_answer": None,
    })
    st.session_state.initialized = True

# Start screen
if st.session_state.num_1 is None:
    start_num = st.number_input(
        "Choose a number between 1 and 12 to practice:", 
        min_value=1, max_value=12, step=1, value=6, key="start_num"
    )
    if st.button("Start Practice"):
        st.session_state.num_1 = int(start_num)
        st.session_state.numbers = list(range(1, 13))
        random.shuffle(st.session_state.numbers)
        st.session_state.current_index = 0
        st.session_state.correct = 0
        st.session_state.start_time = time.time()
        st.session_state.finished = False
        st.session_state.show_feedback = False
        st.rerun()

# Quiz screen
elif not st.session_state.finished:
    num_1 = st.session_state.num_1
    idx = st.session_state.current_index
    total = len(st.session_state.numbers)
    num_2 = st.session_state.numbers[idx]

    st.subheader(f"Question {idx + 1} of {total}")
    st.write(f"What is {num_2} × {num_1}?")

    # If we haven't submitted this question yet, show a form to submit
    if not st.session_state.show_feedback:
        with st.form(key=f"form_{idx}"):
            # store answer in a keyed widget so it doesn't clash between questions
            ans = st.number_input("Your answer", min_value=0, step=1, format="%d", key=f"ans_{idx}")
            submitted = st.form_submit_button("Submit")
            if submitted:
                user_ans = int(ans)
                correct_ans = num_1 * num_2
                is_correct = (user_ans == correct_ans)

                if is_correct:
                    st.session_state.correct += 1
                    st.session_state.last_feedback = ("correct", "✅ Correct!")
                else:
                    st.session_state.last_feedback = ("wrong", f"❌ Wrong — the answer was {correct_ans}.")

                st.session_state.last_user_answer = user_ans
                st.session_state.last_correct_answer = correct_ans

                # create hamster grid as list of rows (each row is its own line)
                rows = []
                for _ in range(num_1):
                    # Use join for consistent spacing
                    rows.append(" ".join(["🐹"] * num_2))
                st.session_state.last_grid_lines = rows

                st.session_state.show_feedback = True
                st.rerun()

    # After submission: show preserved feedback + hamster grid and a Next button
    else:
        kind, message = st.session_state.last_feedback
        if kind == "correct":
            st.success(message)
        else:
            st.error(message)

        st.markdown("**Hamster grid:**")
        for line in st.session_state.last_grid_lines:
            st.write(line)   # each line printed separately so emojis appear on their own rows

        # Next / Finish button
        if st.button("Next"):
            st.session_state.show_feedback = False
            st.session_state.current_index += 1
            if st.session_state.current_index >= len(st.session_state.numbers):
                st.session_state.finished = True
            st.rerun()

# Results screen
else:
    total = len(st.session_state.numbers)
    correct = st.session_state.correct
    percent = round(correct / total * 100)
    elapsed = round(time.time() - st.session_state.start_time, 2)

    st.subheader("🎉 Results")
    st.write(f"You got **{correct}/{total}** correct ({percent}%).")
    st.write(f"⏱️ Time taken: **{elapsed} seconds**.")

    if percent >= 80:
        st.success("🎉 Great job!")
    else:
        st.warning("💪 You are doing great, but keep practicing!")

    if st.button("Restart"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
