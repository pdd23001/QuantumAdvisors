import numpy as np
from qiskit_aer import Aer
from qiskit.quantum_info import SparsePauliOp
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA, SPSA
from qiskit.primitives import Sampler
import random
# ------------------------------------------------------------------------------
# 1. Define Problem Data
# ------------------------------------------------------------------------------
def func(num_exams, num_slots):
    exams = [f'Exam{i+1}' for i in range(num_exams)]
    time_slots = [f'Slot{i+1}' for i in range(num_slots)]

    # Conflict dictionary: Generate random conflicts between exams
    conflicts = {}
    for i in range(num_exams):
        for j in range(i+1, num_exams):
                conflicts[(f'Exam{i+1}', f'Exam{j+1}')] = random.randint(1, 10)

    # ------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------
    # 2. Map (exam, slot) pairs to binary variable labels
    # ------------------------------------------------------------------------------
    # For each exam and time slot, create a binary variable label.
    # A variable is 1 if the exam is scheduled in that time slot, 0 otherwise.
    variables = {}
    for exam in exams:
        for slot in time_slots:
            var_label = f"{exam}_{slot}"
            variables[(exam, slot)] = var_label

    # ------------------------------------------------------------------------------
    # 3. Construct the QUBO Dictionary
    # ------------------------------------------------------------------------------
    # Our QUBO will include:
    # - A heavy penalty for violating the unique scheduling constraint for each exam.
    # - A soft penalty for exam conflicts if two conflicting exams occur in the same slot.
    Q = {}

    # Penalty coefficients:
    penalty_unique = 50.0     # Heavy penalty to enforce that each exam is in exactly one slot.
    penalty_conflict = 10.0   # Penalty for scheduling conflicting exams in the same slot.

    # (A) Unique Scheduling Constraint:
    for exam in exams:
        vars_exam = [variables[(exam, slot)] for slot in time_slots]
        for var in vars_exam:
            Q[(var, var)] = Q.get((var, var), 0) - penalty_unique
        for i in range(len(vars_exam)):
            for j in range(i+1, len(vars_exam)):
                var_i, var_j = vars_exam[i], vars_exam[j]
                Q[(var_i, var_j)] = Q.get((var_i, var_j), 0) + 2 * penalty_unique

    # (B) Soft Conflict Penalty:
    for (exam1, exam2), weight in conflicts.items():
        for slot in time_slots:
            var1, var2 = variables[(exam1, slot)], variables[(exam2, slot)]
            Q[(var1, var2)] = Q.get((var1, var2), 0) + penalty_conflict * weight

    # print("QUBO dictionary:")
    # for key, value in Q.items():
    #     print(f"{key}: {value}")

    # ------------------------------------------------------------------------------
    # 4. Convert the QUBO to a Sparse Pauli Operator (Cost Hamiltonian)
    # ------------------------------------------------------------------------------
    def qubo_to_sparse_pauli_op(Q, var_list):
        num_vars = len(var_list)
        constant = 0.0
        pauli_dict = {}

        for (i, j), coeff in Q.items():
            idx_i, idx_j = var_list.index(i), var_list.index(j)
            if i == j:
                constant += coeff / 2
                pauli_str = "I" * idx_i + "Z" + "I" * (num_vars - idx_i - 1)
                pauli_dict[pauli_str] = pauli_dict.get(pauli_str, 0) - coeff / 2
            else:
                constant += coeff / 4
                pauli_dict["I" * idx_i + "Z" + "I" * (num_vars - idx_i - 1)] = pauli_dict.get("I" * idx_i + "Z" + "I" * (num_vars - idx_i - 1), 0) - coeff / 4
                pauli_dict["I" * idx_j + "Z" + "I" * (num_vars - idx_j - 1)] = pauli_dict.get("I" * idx_j + "Z" + "I" * (num_vars - idx_j - 1), 0) - coeff / 4
                pauli_str = "I" * min(idx_i, idx_j) + "Z" + "I" * (abs(idx_i - idx_j) - 1) + "Z" + "I" * (num_vars - max(idx_i, idx_j) - 1)
                pauli_dict[pauli_str] = pauli_dict.get(pauli_str, 0) + coeff / 4

        if constant != 0:
            pauli_dict["I" * num_vars] = pauli_dict.get("I" * num_vars, 0) + constant

        return SparsePauliOp.from_list([(key, val) for key, val in pauli_dict.items()])

    var_list = list(variables.values())
    cost_operator = qubo_to_sparse_pauli_op(Q, var_list)

    # print("\nCost Operator (Hamiltonian):")
    # print(cost_operator)

    # ------------------------------------------------------------------------------
    # 5. Set Up and Run QAOA
    # ------------------------------------------------------------------------------
    optimizer = COBYLA(maxiter=200)
    backend = Aer.get_backend('aer_simulator')
    sampler = Sampler()

    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=1)

    result = qaoa.compute_minimum_eigenvalue(operator=cost_operator)

    # ------------------------------------------------------------------------------
    # 6. Interpret and Print Results
    # ------------------------------------------------------------------------------
    def interpret_results(result, variables, exams, time_slots):
        # Get the binary string of the best solution
        binary_solution = result.best_measurement['bitstring']
        
        # Create a dictionary to store the schedule
        schedule = {slot: [] for slot in time_slots}
        
        # Interpret the binary string
        for i, bit in enumerate(binary_solution):
            if bit == '1':
                for (exam, slot), index in variables.items():
                    if index == var_list[i]:
                        schedule[slot].append(exam)
                        break
        
        return schedule

    schedule = interpret_results(result, variables, exams, time_slots)
    res = ""
    res+= "Exam Schedule:\n"
    for slot, assigned_exams in schedule.items():
        res+=f"{slot}: {', '.join(assigned_exams)}\n"

    # Calculate the number of conflicts in the schedule
    conflicts_count = 0
    for slot, assigned_exams in schedule.items():
        for i in range(len(assigned_exams)):
            for j in range(i+1, len(assigned_exams)):
                if (assigned_exams[i], assigned_exams[j]) in conflicts or (assigned_exams[j], assigned_exams[i]) in conflicts:
                    conflicts_count += 1

    return {"response":res+f"\nNumber of conflicts in the schedule: {conflicts_count}, Total energy of the solution: {result.optimal_value}"}
