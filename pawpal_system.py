from dataclasses import dataclass, field
from typing import List, Optional
from enum import IntEnum
from datetime import datetime, date, timedelta

class Priority(IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    @classmethod
    def from_value(cls, value: "Priority | str") -> "Priority":
        """Accept either a Priority or a string like 'HIGH'/'high' and return a Priority."""
        if isinstance(value, cls):
            return value
        try:
            return cls[str(value).strip().upper()]
        except KeyError:
            return cls.MEDIUM

@dataclass
class Task:
    title: str
    task_type: str
    priority: Priority
    time: str                      
    frequency: str                 
    task_date: date = field(default_factory=date.today) 
    is_completed: bool = False
    pet: Optional['Pet'] = None

    def __post_init__(self) -> None:
        # Allow tasks to be created with a string priority ("HIGH") or the enum,
        # and always store a Priority so tasks can be sorted by importance.
        self.priority = Priority.from_value(self.priority)

    def mark_as_done(self) -> None:
        if self.is_completed:
            return  
            
        self.is_completed = True
        
        if self.pet and self.frequency in ["Daily", "Weekly"]:
            days_to_add = 1 if self.frequency == "Daily" else 7
            next_date = self.task_date + timedelta(days=days_to_add)
            
            recurring_task = Task(
                title=self.title,
                task_type=self.task_type,
                priority=self.priority,
                time=self.time,
                frequency=self.frequency,
                task_date=next_date,
                pet=self.pet
            )
            self.pet.add_task(recurring_task)


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        task.pet = self
        self.tasks.append(task)

    def get_details(self) -> str:
        return f"{self.name} ({self.species}, {self.age} years old)"


@dataclass
class Owner:
    name: str
    email: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append(task)
        return all_tasks


class Scheduler:

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        return sorted(tasks, key=lambda t: t.time)

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        # Priority is an IntEnum (HIGH=1), so ascending order puts the most
        # important tasks first; ties are broken by time of day.
        return sorted(tasks, key=lambda t: (t.priority, t.time))

    def filter_tasks(self, tasks: List[Task], pet_name: Optional[str] = None, status: Optional[bool] = None) -> List[Task]:
        filtered = tasks
        if pet_name:
            filtered = [t for t in filtered if t.pet and t.pet.name.lower() == pet_name.lower()]
        if status is not None:
            filtered = [t for t in filtered if t.is_completed == status]
        return filtered

    def detect_conflicts(self, owner: Owner) -> List[str]:
        warnings = []
        for pet in owner.pets:
            time_slots = {}
            for task in pet.tasks:
                if not task.is_completed:
                    key = (task.task_date, task.time)
                    if key not in time_slots:
                        time_slots[key] = []
                    time_slots[key].append(task)
            
            for (t_date, t_time), tasks in time_slots.items():
                if len(tasks) > 1:
                    titles = " & ".join([f"'{t.title}'" for t in tasks])
                    warnings.append(f"⚠️ Conflict warning for {pet.name} on {t_date} at {t_time}: {titles} are overlapping.")
        return warnings