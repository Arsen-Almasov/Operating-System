%%writefile deadlock.py
import threading
import time
import faulthandler

lock_a = threading.Lock()
lock_b = threading.Lock()

def worker_a():
    with lock_a:
        print("Поток A захватил lock_a", flush=True)
        time.sleep(0.2)
        print("Поток A ожидает lock_b", flush=True)
        with lock_b:
            print("Поток A получил обе блокировки", flush=True)

def worker_b():
    with lock_b:
        print("Поток B захватил lock_b", flush=True)
        time.sleep(0.2)
        print("Поток B ожидает lock_a", flush=True)
        with lock_a:
            print("Поток B получил обе блокировки", flush=True)

if __name__ == "__main__":
    faulthandler.dump_traceback_later(3, repeat=False)
    a = threading.Thread(target=worker_a, name="Worker-A", daemon=True)
    b = threading.Thread(target=worker_b, name="Worker-B", daemon=True)
    a.start()
    b.start()
    a.join()
    b.join()
  Writing deadlock.py
import subprocess
import sys

p = subprocess.Popen(
    [sys.executable, "deadlock.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

try:
    output, _ = p.communicate(timeout=5)
    print(output)
except subprocess.TimeoutExpired:
    p.kill()
    output, _ = p.communicate()
    print(output)
    print("Подтверждение: программа не завершилась за 5 секунд.")
  Поток A захватил lock_a
Поток B захватил lock_b
Поток A ожидает lock_b
Поток B ожидает lock_a
Timeout (0:00:03)!
Thread 0x00007cbf53fff6c0 (most recent call first):
  File "/content/deadlock.py", line 21 in worker_b
  File "/usr/lib/python3.13/threading.py", line 995 in run
  File "/usr/lib/python3.13/threading.py", line 1044 in _bootstrap_inner
  File "/usr/lib/python3.13/threading.py", line 1015 in _bootstrap

Thread 0x00007cbf507ff6c0 (most recent call first):
  File "/content/deadlock.py", line 13 in worker_a
  File "/usr/lib/python3.13/threading.py", line 995 in run
  File "/usr/lib/python3.13/threading.py", line 1044 in _bootstrap_inner
  File "/usr/lib/python3.13/threading.py", line 1015 in _bootstrap

Thread 0x00007cbf59670080 (most recent call first):
  File "/usr/lib/python3.13/threading.py", line 1095 in join
  File "/content/deadlock.py", line 30 in <module>

Подтверждение: программа не завершилась за 5 секунд.
