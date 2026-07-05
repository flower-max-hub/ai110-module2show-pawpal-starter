from datetime import date, timedelta

from pawpal_system import Owner, Pet, Task, Scheduler, Priority

def test_add_pet_and_task():
    owner = Owner("Test Owner", "test@example.com")
    pet = Pet("Mochi", "Dog", 2)
    owner.add_pet(pet)
    
    assert len(owner.pets) == 1
    
    task = Task("Morning Walk", "General", "HIGH", "08:00", "Once")
    pet.add_task(task)
    
    assert len(pet.tasks) == 1
    assert task.pet == pet

def test_scheduler_sorting():
    scheduler = Scheduler()
    task1 = Task("Late Walk", "General", "LOW", "18:00", "Once")
    task2 = Task("Early Breakfast", "General", "HIGH", "07:30", "Once")
    
    sorted_tasks = scheduler.sort_by_time([task1, task2])

    assert sorted_tasks[0].time == "07:30"
    assert sorted_tasks[1].time == "18:00"


def test_priority_string_coerced_to_enum():
    task = Task("Meds", "health", "high", "09:00", "Once")
    assert task.priority is Priority.HIGH

    # An unknown priority falls back to MEDIUM rather than crashing.
    fallback = Task("Play", "general", "whenever", "10:00", "Once")
    assert fallback.priority is Priority.MEDIUM


def test_scheduler_sorts_by_priority():
    scheduler = Scheduler()
    low = Task("Evening walk", "general", "LOW", "18:00", "Once")
    high = Task("Medication", "health", "HIGH", "20:00", "Once")
    medium = Task("Feed", "general", "MEDIUM", "12:00", "Once")

    ordered = scheduler.sort_by_priority([low, high, medium])

    assert [t.priority for t in ordered] == [Priority.HIGH, Priority.MEDIUM, Priority.LOW]


def test_mark_as_done_daily_creates_next_day_task():
    pet = Pet("Mochi", "dog", 2)
    task = Task("Walk", "general", "HIGH", "08:00", "Daily", task_date=date(2026, 7, 5))
    pet.add_task(task)

    task.mark_as_done()

    assert task.is_completed is True
    assert len(pet.tasks) == 2
    recurring = pet.tasks[1]
    assert recurring.is_completed is False
    assert recurring.task_date == date(2026, 7, 5) + timedelta(days=1)


def test_mark_as_done_once_does_not_recur():
    pet = Pet("Mochi", "dog", 2)
    task = Task("Vet visit", "health", "HIGH", "08:00", "Once")
    pet.add_task(task)

    task.mark_as_done()

    assert task.is_completed is True
    assert len(pet.tasks) == 1


def test_mark_as_done_is_idempotent():
    pet = Pet("Mochi", "dog", 2)
    task = Task("Walk", "general", "HIGH", "08:00", "Daily")
    pet.add_task(task)

    task.mark_as_done()
    task.mark_as_done()  # second call should not spawn another recurring task

    assert len(pet.tasks) == 2


def test_filter_tasks_by_pet_and_status():
    owner = Owner("Jordan", "j@example.com")
    dog = Pet("Rex", "dog", 4)
    cat = Pet("Milo", "cat", 3)
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Walk", "general", "HIGH", "08:00", "Once"))
    dog.add_task(Task("Feed", "general", "MEDIUM", "09:00", "Once"))
    cat.add_task(Task("Litter", "general", "LOW", "10:00", "Once"))

    scheduler = Scheduler()
    all_tasks = owner.get_all_tasks()

    rex_tasks = scheduler.filter_tasks(all_tasks, pet_name="rex")
    assert len(rex_tasks) == 2

    dog.tasks[0].is_completed = True
    pending = scheduler.filter_tasks(all_tasks, status=False)
    assert len(pending) == 2


def test_detect_conflicts_flags_same_time_slot():
    owner = Owner("Jordan", "j@example.com")
    pet = Pet("Mochi", "dog", 2)
    owner.add_pet(pet)

    d = date(2026, 7, 5)
    pet.add_task(Task("Walk", "general", "HIGH", "08:00", "Once", task_date=d))
    pet.add_task(Task("Meds", "health", "HIGH", "08:00", "Once", task_date=d))
    pet.add_task(Task("Nap", "general", "LOW", "13:00", "Once", task_date=d))

    scheduler = Scheduler()
    warnings = scheduler.detect_conflicts(owner)

    assert len(warnings) == 1
    assert "08:00" in warnings[0]