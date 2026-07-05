import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task, Priority

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+**, a pet care planning assistant. Add your pets and their
care tasks, then build a schedule, spot timing conflicts, and check tasks off as
you go.
"""
)

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

st.divider()

# ---------------------------------------------------------------------------
# Persistent state: one Owner lives across reruns so pets/tasks are not lost.
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan", "owner@info.com")

owner = st.session_state.owner
scheduler = Scheduler()

# --- Owner ------------------------------------------------------------------
st.subheader("Owner")
col_o1, col_o2 = st.columns(2)
with col_o1:
    owner.name = st.text_input("Owner name", value=owner.name)
with col_o2:
    owner.email = st.text_input("Owner email", value=owner.email)

# --- Add a pet --------------------------------------------------------------
st.subheader("Add a pet")
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_p2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col_p3:
    age = st.number_input("Age (years)", min_value=0, max_value=40, value=2)

if st.button("Add pet"):
    if any(p.name.lower() == pet_name.lower() for p in owner.pets):
        st.warning(f"{pet_name} is already in the list.")
    else:
        owner.add_pet(Pet(pet_name, species, int(age)))
        st.success(f"Added {pet_name}.")

if not owner.pets:
    st.info("Add a pet to get started.")
    st.stop()

st.caption("Current pets: " + ", ".join(p.get_details() for p in owner.pets))

st.divider()

# --- Add a task -------------------------------------------------------------
st.subheader("Add a task")
pet_choice = st.selectbox("For which pet?", [p.name for p in owner.pets])

col_t1, col_t2, col_t3 = st.columns(3)
with col_t1:
    task_title = st.text_input("Task title", value="Morning walk")
with col_t2:
    task_type = st.text_input("Task type", value="general")
with col_t3:
    priority = st.selectbox("Priority", [p.name for p in Priority], index=0)

col_t4, col_t5 = st.columns(2)
with col_t4:
    task_time = st.text_input("Time (HH:MM)", value="08:00")
with col_t5:
    frequency = st.selectbox("Frequency", ["Once", "Daily", "Weekly"])

if st.button("Add task"):
    selected_pet = next(p for p in owner.pets if p.name == pet_choice)
    new_task = Task(task_title, task_type, priority, task_time, frequency)
    selected_pet.add_task(new_task)
    st.success(f"Linked '{task_title}' to {selected_pet.name}.")

st.divider()


st.subheader("🗓️ Schedule")
all_tasks = owner.get_all_tasks()

if not all_tasks:
    st.info("No tasks yet. Add one above.")
else:
    sort_mode = st.radio("Sort by", ["Time", "Priority"], horizontal=True)
    if sort_mode == "Time":
        ordered = scheduler.sort_by_time(all_tasks)
    else:
        ordered = scheduler.sort_by_time(all_tasks)
    for i, task in enumerate(ordered):
        cols = st.columns([3, 2, 2, 2, 2])
        cols[0].write(f"**{task.title}**")
        cols[1].write(task.pet.name if task.pet else "Unknown")
        cols[2].write(task.time)
        cols[3].write(task.priority)
        if task.is_completed:
            cols[4].write("✅ done")
        else:
            # Key must be unique and stable per task so clicks map correctly.
            if cols[4].button("Mark done", key=f"done_{i}_{task.title}_{task.time}"):
                task.mark_as_done()
                st.rerun()

    st.divider()

   
    st.subheader("⚠️ Conflicts")
    warnings = scheduler.detect_conflicts(owner)
    if warnings:
        for w in warnings:
            st.warning(w)
    else:
        st.success("No scheduling conflicts detected.")
