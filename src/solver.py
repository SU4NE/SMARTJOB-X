class Solver:
    def __init__(self, jobs, num_jobs=None, num_machines=None):
        self.jobs = jobs
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.schedule = []

    def solve(self):
        return self.schedule

    def get_makespan(self, schedule):
        if not schedule:
            raise ValueError("Schedule is empty")
        return max(start + duration for _, _, _, start, duration in schedule)

    def print_schedule(self, schedule):
        print("Schedule:")
        for job_id, op_idx, machine, start, duration in schedule:
            print(f"Job {job_id}, Op {op_idx} -> Machine {machine} | Start: {start}, Duration: {duration}")
        print(f"\nTotal Makespan: {self.get_makespan(schedule)}")

    def is_valid_schedule(self, schedule):
        seen_operations = set()
        op_start_times = {}

        for job_id, op_idx, machine, start, duration in schedule:
            if (job_id, op_idx) in seen_operations:
                print(f"Invalid schedule: Repeated operation for Job {job_id}, Operation {op_idx}.")
                return False
            seen_operations.add((job_id, op_idx))
            op_start_times[(job_id, op_idx)] = (start, start + duration)

        for job_id in range(self.num_jobs):
            for op_idx in range(1, len(self.jobs[job_id])):
                if (job_id, op_idx) in op_start_times and (job_id, op_idx - 1) in op_start_times:
                    prev_end = op_start_times[(job_id, op_idx - 1)][1]
                    curr_start = op_start_times[(job_id, op_idx)][0]
                    if curr_start < prev_end:
                        print(f"Invalid schedule: Job {job_id} - Operation {op_idx} starts before previous ends.")
                        return False

        machine_usage = {}
        for job_id, op_idx, machine, start, duration in schedule:
            if machine not in machine_usage:
                machine_usage[machine] = []
            machine_usage[machine].append((start, start + duration))

        for machine, intervals in machine_usage.items():
            intervals.sort()
            for i in range(1, len(intervals)):
                prev_end = intervals[i - 1][1]
                curr_start = intervals[i][0]
                if curr_start < prev_end:
                    print(f"Invalid schedule: Overlapping operations on machine {machine}.")
                    return False

        return True
