def read_jobshop_instance(filepath):
    with open(filepath, 'r') as file:
        lines = [line.strip() for line in file if line.strip() and not line.startswith("#")]

    num_jobs, num_machines = map(int, lines[0].split())
    jobs = []

    for line in lines[1:num_jobs + 1]:
        data = list(map(int, line.split()))
        job = []
        for i in range(0, len(data), 2):
            machine = data[i]
            duration = data[i + 1]
            job.append((machine, duration))
        jobs.append(job)

    return jobs, num_jobs, num_machines
