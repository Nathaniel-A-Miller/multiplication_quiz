import streamlit as st
import random
import time

st.set_page_config(page_title="Hamster Multiplication", page_icon="🐹")
st.title("🐹 Multiplication Practice")

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.update({
        "num_1": None,
        "numbers": [],
        "current_index": 0,
        "correct": 0,
        "start_time": None,
        "finished": False,
        "show_feedback": False,
        "last_feedback": ("", ""),  # (type, message)
        "last_grid_lines": [],
        "final_total": None,
        "final_correct": None,
        "final_elapsed": None
    })
    st.session_state.initialized = True

# Step 1: Choose number
if st.session_state.num_1 is None:
    num = st.number_input(
        "Choose a number between 1 and 12 to practice:", 
        min_value=1, max_value=12, step=1, value=6
    )
    if st.button("Start Practice"):
        st.session_state.num_1 = int(num)
        st.session_state.numbers = list(range(1, 13))
        random.shuffle(st.session_state.numbers)
        st.session_state.current_index = 0
        st.session_state.correct = 0
        st.session_state.start_time = time.time()
        st.session_state.finished = False
        st.session_state.show_feedback = False
        st.rerun()

# Step 2: Quiz
elif not st.session_state.finished:
    num_1 = st.session_state.num_1
    idx = st.session_state.current_index
    total_questions = len(st.session_state.numbers)
    num_2 = st.session_state.numbers[idx]

    st.subheader(f"Question {idx + 1} of {total_questions}")
    st.write(f"What is {num_2} × {num_1}?")

    # Show form for answer submission
    if not st.session_state.show_feedback:
        with st.form(key=f"form_{idx}"):
            ans = st.number_input("Your answer", min_value=0, step=1, key=f"ans_{idx}")
            submitted = st.form_submit_button("Submit")
            if submitted:
                correct_ans = num_1 * num_2
                if ans == correct_ans:
                    st.session_state.correct += 1
                    st.session_state.last_feedback = ("correct", "✅ Correct!")
                else:
                    st.session_state.last_feedback = ("wrong", f"❌ Wrong — the answer was {correct_ans}.")

                # Create hamster grid
                grid = [" ".join(["🐹"] * num_2) for _ in range(num_1)]
                st.session_state.last_grid_lines = grid
                st.session_state.show_feedback = True
                st.rerun()

    # After submission: show feedback + hamster grid + Next button
    else:
        kind, message = st.session_state.last_feedback
        if kind == "correct":
            st.success(message)
        else:
            st.error(message)

        st.markdown("**Hamster grid:**")
        for line in st.session_state.last_grid_lines:
            st.write(line)

        if st.button("Next"):
            st.session_state.show_feedback = False
            st.session_state.current_index += 1
            if st.session_state.current_index >= total_questions:
                st.session_state.finished = True
                # Save final results
                st.session_state.final_total = total_questions
                st.session_state.final_correct = st.session_state.correct
                st.session_state.final_elapsed = round(time.time() - st.session_state.start_time, 2)
            st.rerun()

# Step 3: Results
else:
    total = st.session_state.final_total
    correct = st.session_state.final_correct
    elapsed = st.session_state.final_elapsed
    percent = round(correct / total * 100)

    st.subheader("🎉 Results 🎉")
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
