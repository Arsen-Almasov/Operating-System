%%writefile pipe_demo.py
import os

read_fd, write_fd = os.pipe()
pid = os.fork()

if pid == 0:
    os.close(read_fd)
    try:
        os.write(write_fd, b"Hello from child process!\n")
    finally:
        os.close(write_fd)
    os._exit(0)
else:
    os.close(write_fd)
    try:
        data = b""
        while True:
            chunk = os.read(read_fd, 4096)
            if not chunk:
                break
            data += chunk
    finally:
        os.close(read_fd)

    os.waitpid(pid, 0)
    print("Родитель получил:", data.decode().strip())
  !python3 pipe_demo.py
Родитель получил: Hello from child process!
