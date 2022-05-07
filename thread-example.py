import threading
import subprocess
import os
import time
import signal
# the example powershell commands to execute in windows os.
win_cmds = ['Start-Sleep -Seconds 30',
            'Start-Sleep -Seconds 40',
            ]

unix_cmds = []

process_pid_running = []
process_running = []


# executes all commands in wincmds list
def create_win_process():
    global process_pid_running
    global process_running
    os.environ["COMSPEC"] = 'pwsh'  # use powershell 7 as shell! not cmd :)
    # create processes to execute commands in win_cmds
    for command in win_cmds:
        
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, text=True)
        process_running.append(p)  # add process to the process_runnig list.
        process_pid_running.append(p.pid)  # add process's pid value to the process_pid_running list.
        print(f"Started Process {p.pid}")
        #print("returncode: ", p.returncode) # if a process is running and not terminated yet, returncode is None. Otherwise 0 (or negative in POSIX OSs)
       
    
# to read the states of the process and output also.
def communicate_process(process):
    data = process.communicate()  # communicate() waits for the executucion of the command is finished.


# we have used one thread per one process in order to get live and real returncode from processes.
# we are using returncode value to check if process is alive or not.
# if we didnt use threads  and have used .communicate in the main process , we would need
# to wait for each process to complete. each process would have to wait for the next one.
# to execute each command concurrently and see their states , we used threads.
def create_check_thread():
    global process_running
    for process in process_running:
        t = threading.Thread(target=communicate_process, args=(process,))

# to show the state of the processes on the terminal.
def check_process():
    global process_running
    global process_pid_running
    while len(process_running) != 0:
        if len(process_running) > 0:
            time.sleep(2)    
        for process in process_running:
            if process.poll() is None:
                print(f"{process.pid} is alive")
            else:
                print(f"{process.pid} is dead")
                process_running.remove(process)
                process_pid_running.remove(process.pid)
        
        print("-------------------------------------------------------------------------------------")
        print(f"Running Processes:{process_running}")
        print(f"Running Processes PIDs:{process_pid_running}")
        print(f"Running Process Count:{len(process_running)}")
        print("-------------------------------------------------------------------------------------")
        
    print("All processes terminated.")


def create_unix_process():
    pass


create_win_process()
create_check_thread()
check_process()
#t = threading.Thread(target=create_win_process, daemon=True)
#t.start()

