import sys
from common import read_jobshop_instance, write_output
from solver import Solver

def main(instance_path):
    jobs, num_jobs, num_machines  = read_jobshop_instance(instance_path)

    solver = Solver(jobs, num_jobs, num_machines)
    solution = solver.solve()
    #solver.print_schedule(solution)

    write_output(solution, instance_path)
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <instance_path>")
        sys.exit(1)

    main(sys.argv[1])
