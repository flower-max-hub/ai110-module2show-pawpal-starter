# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:

pytest test_pawpal.py -v
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
test_pawpal.py::test_add_pet_and_task PASSED                                              [ 11%]
test_pawpal.py::test_scheduler_sorting PASSED                                             [ 22%]
test_pawpal.py::test_priority_string_coerced_to_enum PASSED                               [ 33%]
test_pawpal.py::test_scheduler_sorts_by_priority PASSED                                   [ 44%]
test_pawpal.py::test_mark_as_done_daily_creates_next_day_task PASSED                      [ 55%]
test_pawpal.py::test_mark_as_done_once_does_not_recur PASSED                              [ 66%]
test_pawpal.py::test_mark_as_done_is_idempotent PASSED                                    [ 77%]
test_pawpal.py::test_filter_tasks_by_pet_and_status PASSED                                [ 88%]
test_pawpal.py::test_detect_conflicts_flags_same_time_slot PASSED                         [100%]

======================================= 9 passed in 0.02s =======================================


```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts all tasks chronologically using their time attribute. |
| Filtering | `Scheduler.filter_tasks()` | Filters tasks dynamically by pet name or completion status. |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags duplicate time slots for the same pet and raises a warning in the UI. |
| Recurring tasks | `Task.mark_as_done()` | Automatically schedules a new task instance for the next day if the task is "Daily". |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
Enter owner information at the top 
2. <!-- Describe this step -->
Add a new pet by entering their information specifying the age the species and click add
3. <!-- Describe this step -->
Assign a task to Mochi and metion the priorities 
4. <!-- Describe this step -->
view the automatic generated schedule
5. <!-- Add more steps as needed -->
Click the bouton done 

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
