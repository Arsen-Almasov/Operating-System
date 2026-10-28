%%writefile deadlock_fixed.py
import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

def worker(name):
    with lock_a:
        with lock_b:
            print(f"{name}: обе блокировки получены")

threads = [
    threading.Thread(target=worker, args=("Поток A",)),
    threading.Thread(target=worker, args=("Поток B",)),
]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("Все потоки завершились.")
Writing deadlock_fixed.py
!python3 deadlock_fixed.py
Поток A: обе блокировки получены
Поток B: обе блокировки получены
Все потоки завершились.
