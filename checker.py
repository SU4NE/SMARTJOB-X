import sys
from collections import defaultdict

from src.common import read_jobshop_instance

def read_solution_order(path):
    """Lê a ordem de solução de um arquivo."""
    order = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) != 5:
                    print(f"❌ Linha inválida: {line}. Esperava 5 valores.")
                    continue
                order.append(tuple(map(int, parts)))
    return order

def check_duplicates(order):
    """Verifica se há operações duplicadas na solução."""
    seen = set()
    for operation in order:
        if operation in seen:
            print(f"❌ Operação repetida: {operation}")
            return False
        seen.add(operation)
    return True

def check_all_operations_scheduled(jobs, order):
    """Verifica se todas as operações dos jobs estão agendadas corretamente."""
    required_ops = set((j, o) for j in range(len(jobs)) for o in range(len(jobs[j])))
    given_ops = set((job, op) for job, op, _, _, _ in order)

    missing = required_ops - given_ops
    extra = given_ops - required_ops

    if missing:
        print(f"❌ Operações faltando: {missing}")
        return False
    if extra:
        print(f"❌ Operações extras: {extra}")
        return False
    return True

def build_schedule(order):
    """Constrói o cronograma baseado na ordem de solução."""
    job_next_op = defaultdict(int)
    job_ready_time = defaultdict(int)
    machine_ready_time = defaultdict(int)
    schedule = []

    for job, op, machine, start_time, duration in order:
        if op != job_next_op[job]:
            raise ValueError(f"Operação fora de ordem no job {job}: esperava op {job_next_op[job]}, recebeu {op}")

        job_ready_time[job] = max(job_ready_time[job], start_time)
        machine_ready_time[machine] = max(machine_ready_time[machine], start_time)
        end_time = start_time + duration

        job_next_op[job] += 1
        machine_ready_time[machine] = end_time

        schedule.append((job, op, machine, start_time, duration))

    return schedule

def check_conflicts(schedule):
    """Verifica se há conflitos de máquina no cronograma."""
    machine_ops = defaultdict(list)
    for job, op, machine, start, duration in schedule:
        machine_ops[machine].append((start, start + duration, job, op))

    for machine, ops in machine_ops.items():
        ops.sort()
        for i in range(1, len(ops)):
            end_prev = ops[i - 1][1]
            start_curr = ops[i][0]
            if start_curr < end_prev:
                print(f"❌ Conflito na máquina {machine}: operação ({ops[i][2]},{ops[i][3]}) começa em {start_curr}, antes do fim de ({ops[i - 1][2]},{ops[i - 1][3]}) em {end_prev}.")
                return False
    return True

def main(instance_file, solution_file):
    """Função principal para validar a solução de jobshop."""
    try:
        jobs, _, _ = read_jobshop_instance(instance_file)
        order = read_solution_order(solution_file)
        
        if not check_duplicates(order):
            print("❌ Solução inválida (operações repetidas).")
            return

        if not check_all_operations_scheduled(jobs, order):
            print("❌ Solução inválida (operações faltando ou extras).")
            return

        schedule = build_schedule(order)

        if check_conflicts(schedule):
            print("✅ Solução válida (sem conflitos de máquina).")
        else:
            print("❌ Solução inválida (conflitos detectados).")

        makespan = max(start + duration for _, _, _, start, duration in schedule)
        print(f"⏱️ Makespan: {makespan}")

    except Exception as e:
        print(f"Erro ao validar: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python checker.py instancia.txt solucao.txt")
    else:
        main(sys.argv[1], sys.argv[2])
