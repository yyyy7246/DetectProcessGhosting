import os
import psutil
import time

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
                
                # Check file locking status.
                try:
                    with open(proc.exe(), 'r+'):
                        print("The file is not locked.")
                except IOError:
                    print("The file is locked.")

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        last_seen_procs = current_procs
        time.sleep(1)  # wait for a second before checking again

check_new_process()
