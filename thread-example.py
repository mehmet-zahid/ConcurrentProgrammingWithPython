import threading
import subprocess
import os
import time
import signal

win_cmds = ['Start-Sleep -Seconds 30',
            'Start-Sleep -Seconds 40',
            ]

unix_cmds = []

process_pid_running = []
process_running = []


# Functions to execute by the Thread!
def create_win_process():
    global process_pid_running
    global process_running
    os.environ["COMSPEC"] = 'pwsh'  # use powershell 7 as shell! not cmd :)
    for command in win_cmds:
        # create a process for powershell to execute
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, text=True)
        process_running.append(p)
        process_pid_running.append(p.pid)


        print("PID: ", p.pid)
        print("returncode: ", p.returncode)
        print("p.poll()", p.poll())
    print(f"{process_running}-{process_pid_running}-{len(process_running)}")
    # while p.poll() is None:
    #     print(p.poll())
    #     print('process still alive!')
    # print(p.poll())
    # print('I guess process has terminated!')


def communicate_process(process):
    data = process.communicate()


# we have used threads per process due to get returncode from processes.
# we are using returncode value to check if process is alive or not.
# if we didnt use threads  and have used .communicate in the main process , we would need
# to wait for each process to complete. each process would have to wait for the next one.
# to execute each command concurrently and see their states , we used threads.
def create_check_thread():
    global process_running
    for process in process_running:
        t = threading.Thread(target=communicate_process, args=(process,))


def check_process():
    global process_running
    global process_pid_running
    while len(process_running) != 0:
        for process in process_running:
            print("process.poll(): ", process.poll())
            if process.poll() is None:
                print(process.returncode)
                print(f"{process.pid} is alive")
            else:
                print(f"{process.pid} is dead")
                process_running.remove(process)
                process_pid_running.remove(process.pid)
                break
        print(f"{process_running}-{process_pid_running}-{len(process_running)}")
        time.sleep(5)
    print("All processes terminated.")


def create_unix_process():
    pass


create_win_process()
create_check_thread()
check_process()
#t = threading.Thread(target=create_win_process, daemon=True)
#t.start()

