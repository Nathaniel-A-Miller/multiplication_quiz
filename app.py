import streamlit as st
import random
import time

st.set_page_config(page_title="Pet Multiplication", page_icon="🐾")
st.title("🐾 Pet Multiplication Practice")

# Available pets
PET_OPTIONS = {
    "Hamster": "🐹",
    "Cat": "🐱",
    "Dog": "🐶",
    "Rabbit": "🐰",
    "Mouse": "🐭",
    "Frog": "🐸",
    "Panda": "🐼",
    "Fox": "🦊",
}

# Initialize session state
if "initialized" not in st.session_state:
    st.session_state.update({
        "pet_name": None,
        "pet_emoji": None,
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

# Step 1: Choose pet and number
if st.session_state.pet_name is None:
    st.subheader("Choose your pet and multiplication number")
    pet_choice = st.selectbox("Select your pet:", list(PET_OPTIONS.keys()))
    num_choice = st.number_input(
        "Choose a number between 1 and 12 to practice:", 
        min_value=1, max_value=12, step=1, value=6
    )
    if st.button("Start Practice"):
        st.session_state.pet_name = pet_choice
        st.session_state.pet_emoji = PET_OPTIONS[pet_choice]
        st.session_state.num_1 = int(num_choice)
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
    pet_name = st.session_state.pet_name
    pet_emoji = st.session_state.pet_emoji
    num_1 = st.session_state.num_1
    idx = st.session_state.current_index
    total_questions = len(st.session_state.numbers)
    num_2 = st.session_state.numbers[idx]

    st.subheader(f"Question {idx + 1} of {total_questions}")
    st.write(f"What is {num_2} × {num_1}?")

    # Form for answer submission
    if not st.session_state.show_feedback:
        with st.form(key=f"form_{idx}"):
            ans = st.number_input("Your answer", min_value=0, step=1, key=f"ans_{idx}")
            submitted = st.form_submit_button("Submit")
            if submitted:
                correct_ans = num_1 * num_2
                if ans == correct_ans:
                    st.session_state.correct += 1
                    st.session_state.last_feedback = ("correct", f"✅ Correct! Your {pet_name} is happy!")
                else:
                    st.session_state.last_feedback = ("wrong", f"❌ Wrong — the answer was {correct_ans}.")

                # Create pet grid
                grid = [" ".join([pet_emoji] * num_2) for _ in range(num_1)]
                st.session_state.last_grid_lines = grid
                st.session_state.show_feedback = True
                st.rerun()

    # After submission: show feedback + pet grid + Next button
    else:
        kind, message = st.session_state.last_feedback
        if kind == "correct":
            st.success(message)
        else:
            st.error(message)

        st.markdown(f"**{pet_name} grid:**")
        for line in st.session_state.last_grid_lines:
            st.write(line)

        if st.button("Next"):
            st.session_state.show_feedback = False
            st.session_state.current_index += 1
            if st.session_state.current_index >= total_questions:
                st.session_state.finished = True
                # Save final results (store raw seconds)
                st.session_state.final_total = total_questions
                st.session_state.final_correct = st.session_state.correct
                st.session_state.final_elapsed = time.time() - st.session_state.start_time
            st.rerun()

# Step 3: Results
else:
    pet_name = st.session_state.pet_name  # Fetch from session_state
    total = st.session_state.final_total
    correct = st.session_state.final_correct
    elapsed_seconds = st.session_state.final_elapsed
    percent = round(correct / total * 100)

    minutes = int(elapsed_seconds // 60)
    seconds = int(elapsed_seconds % 60)

    st.subheader("🎉 Results 🎉")
    st.write(f"You got **{correct}/{total}** correct ({percent}%).")
    st.write(f"⏱️ Time taken: **{minutes} min {seconds} sec**.")

    if percent >= 80:
        st.success(f"🎉 Great job! Your {pet_name} is proud of you!")
    else:
        st.warning(f"💪 You are doing great, but keep practicing! Your {pet_name} is cheering for you!")

    if st.button("Restart"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
