# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design are: 'owner' , 'pet', 'Task' and 'Scheduler'. 
- What classes did you include, and what responsibilities did you assign to each?
I assigned **Owner** to be the manager, who will be managing contact info and list of pets. **Pets** for species, age, name. **Task** is assigned to activity data (title, time,priority and frequency), **Scheduler** acts as the central engine to sort and organize all the tasks.

**b. Design changes**

- Did your design change during implementation?
Yes my design changed during the implementation for the core to be robust and more profesional
- If yes, describe at least one change and why you made it.
I removed the raw numbers for the task priorities and replaced them with a 'priority', Enum 'IntEnum' linked 'Pet' object directly inside the 'Task' class. To make sure every task knows which animal the data belongs to. 
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The scheduler considers two main rules priority level ( HIGH, MEDIUM, LOW) and Time. 
- How did you decide which constraints mattered most?
I decided that priority matters the most because of needs like giving the pet their medication are matters that are important and can not wait. Time is the second main rules because it used to organize the rest of the day and the different tasks. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
A major tradeoff in my scheduler is that it only detects conflicts for exact time matches. If two tasks are scheduled at the same date and time (like 08:00), it flags a conflict, but it does not account for task duration, so a 20-minute task at 08:00 and another task at 08:10 would not be flagged as overlapping.
- Why is that tradeoff reasonable for this scenario?
This tradeoff is reasonnable because it keeps the code very simple and easy, while still catching the most common case of two tasks booked at the same moment.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI as an aarchitectural co pilot during for the project. 
- What kinds of prompts or questions were most helpful?
The most helpful prompt was the prompt that asked for specific Python design patterns, setting up edge case testing structures.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
Once AI suggested creating a huge and single list inside the scheduler to hold every at one place.
- How did you evaluate or verify what the AI suggested?
I did not accept the AI suggestion because the tasks are not directed to the right assigner.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I built an automated tests to verify the task completion status switching from task, days, and weeks 
- Why were these tests important?
Yes these tests were important to prove that the backend logic functions correctly.

**b. Confidence**

- How confident are you that your scheduler works correctly?
I am confident at 3 out of 5 about my scheduler.
- What edge cases would you test next if you had more time?
If i had more time i would test how the scheduler handles a pending tasks

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
Seeing that the projrct is working well made me so happy.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
if i had another chance i wwould redesign the time conflict detector.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
 I learned that planning your system architecture and testing the backend via a CLI structure before building the user interfaces makes the process much smoother and organized.
