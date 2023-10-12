import os
import psutil
import time

def list_processes():
    process_list = []

    for proc in psutil.process_iter(['pid', 'exe', 'name']):
        try:
            process_info = (proc.info['pid'], proc.info['exe'], proc.info['name'])
            process_list.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return process_list

initial_processes = list_processes()

def check_new_process():
    last_seen_procs = set(p.info['pid'] for p in psutil.process_iter(['pid']))

    while True:
        current_procs = set(p.info['pid'] for p in psutil.process_iter(['pid']))
        new_procs = current_procs - last_seen_procs

        for pid in new_procs:
            try:
                proc = psutil.Process(pid)
                print(f"New process detected: PID: {proc.pid}, Name: {proc.name()}, Executable Path: {proc.exe()}")

                if not os.path.exists(proc.exe()):
                    print(f"Warning! The executable file for the process with PID {proc.pid} does not exist.")
                
                # Check if the exe path is in the initial processes.
                matching_initial_process = next((p for p in initial_processes if p[1] == proc.exe()), None)

                if matching_initial_process is not None and matching_initial_process[2] != proc.name():
                    print(f"Warning! The name of the new process ({proc.name()}) doesn't match with the initial one ({matching_initial_process[2]}). This might be a dangerous process.")

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        last_seen_procs = current_procs
        time.sleep(1)  # wait for a second before checking again

check_new_process()
