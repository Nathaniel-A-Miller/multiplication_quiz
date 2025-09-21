import streamlit as st
import random
import time

st.title("🐹 Multiplication Practice")

# Initialize session state variables
if "num_1" not in st.session_state:
    st.session_state.num_1 = None
if "numbers" not in st.session_state:
    st.session_state.numbers = []
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "finished" not in st.session_state:
    st.session_state.finished = False

# Step 1: Choose the multiplication number
if st.session_state.num_1 is None:
    num_1 = st.number_input("What number between 1 and 12 do you want to practice multiplying?", 
                            min_value=1, max_value=12, step=1)
    if st.button("Start Practice"):
        st.session_state.num_1 = num_1
        st.session_state.numbers = list(range(1, 13))
        random.shuffle(st.session_state.numbers)
        st.session_state.current_index = 0
        st.session_state.correct = 0
        st.session_state.start_time = time.time()
        st.rerun()

# Step 2: Show one question at a time
elif not st.session_state.finished:
    num_1 = st.session_state.num_1
    num_2 = st.session_state.numbers[st.session_state.current_index]

    st.subheader(f"Question {st.session_state.current_index + 1} of {len(st.session_state.numbers)}")
    st.write(f"What is {num_2} × {num_1}?")

    answer = st.number_input("Your answer:", step=1, key=f"answer_{st.session_state.current_index}")
    if st.button("Submit"):
        if answer == num_1 * num_2:
            st.success("✅ Correct!")
            st.session_state.correct += 1
        else:
            st.error(f"❌ Wrong! The answer was {num_1 * num_2}.")

        # Show hamsters grid
        for _ in range(num_1):
            st.write("🐹 " * num_2)

        # Move to next question
        st.session_state.current_index += 1

        if st.session_state.current_index >= len(st.session_state.numbers):
            st.session_state.finished = True

        st.rerun()

# Step 3: Final results
else:
    total = len(st.session_state.numbers)
    correct = st.session_state.correct
    percent = round(correct / total * 100)
    elapsed_time = round(time.time() - st.session_state.start_time, 2)

    st.subheader("🎉 Results 🎉")
    st.write(f"You got {correct}/{total} answers correct ({percent}%).")
    st.write(f"⏱️ Time taken: {elapsed_time} seconds.")

    if percent >= 80:
        st.success("🎉🎉🎉 Good job!")
    else:
        st.warning("💪 You are doing great, but you need to keep trying!")

    if st.button("Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
