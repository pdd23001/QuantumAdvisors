from dimod import ConstrainedQuadraticModel, Binary
from dwave.system import LeapHybridCQMSampler

# ---------------------------
# 1. Define the scheduling data
# ---------------------------
exams = ['Exam1', 'Exam2', 'Exam3']
time_slots = ['Slot1', 'Slot2']
# Define conflicts: each key is a tuple of exams that share students.
# The associated weight can be used to scale the penalty (here, simply 1).
conflicts = {('Exam1', 'Exam2'): 1, ('Exam2', 'Exam3'): 1}

# ---------------------------
# 2. Create the CQM and define variables
# ---------------------------
cqm = ConstrainedQuadraticModel()

# Create a binary variable for each (exam, slot) pair.
# x_{exam,slot} = 1 if the exam is scheduled in that slot, 0 otherwise.
variables = {}
for exam in exams:
    for slot in time_slots:
        var_name = f"{exam}_{slot}"
        variables[(exam, slot)] = Binary(var_name)

# ---------------------------
# 3. Add hard constraints to the CQM
# ---------------------------
# a) Unique scheduling: Each exam must be scheduled in exactly one slot.
for exam in exams:
    # Sum over all time slots for a given exam should equal 1.
    constraint_expr = sum(variables[(exam, slot)] for slot in time_slots)
    cqm.add_constraint(constraint_expr == 1, label=f"One_slot_for_{exam}")

# Note: We no longer add a hard conflict constraint.
# Instead, we will penalize conflicts in the objective function.

# ---------------------------
# 4. Set the objective with soft conflict penalties
# ---------------------------
# Define the penalty coefficient for conflicts.
penalty_conflict = 10.0

# For each conflicting exam pair, add a penalty if both are scheduled in the same slot.
conflict_obj = 0
for (exam1, exam2), weight in conflicts.items():
    for slot in time_slots:
        conflict_obj += penalty_conflict * weight * variables[(exam1, slot)] * variables[(exam2, slot)]

# Set the objective: minimize the total conflict penalty.
cqm.set_objective(conflict_obj)

# ---------------------------
# 5. Solve the CQM using D-Wave’s Leap Hybrid CQM Sampler
# ---------------------------
sampler = LeapHybridCQMSampler()
sampleset = sampler.sample_cqm(cqm, time_limit=5)  # time_limit is in seconds

# Filter for feasible solutions (i.e. solutions that satisfy the hard unique-scheduling constraint)
feasible_samples = sampleset.filter(lambda d: d.is_feasible)

if len(feasible_samples) > 0:
    best_sample = feasible_samples.first.sample
    print("Feasible solution found:")
    for exam in exams:
        for slot in time_slots:
            val = best_sample[f"{exam}_{slot}"]
            if val == 1:
                print(f"  {exam} scheduled in {slot}")
else:
    print("No feasible solution found.")