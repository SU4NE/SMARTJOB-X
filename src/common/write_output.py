import os

def write_output(solution, instance_path):
    instance_name = os.path.basename(instance_path).split('.')[0]

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{instance_name}.out.txt")

    with open(output_path, 'w') as f:
        for job_id, op_idx, machine, start, duration in solution:
            f.write(f"{job_id} {op_idx} {machine} {start} {duration}\n")
    
    print(f"Output written to {output_path}")
