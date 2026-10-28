import os
os.makedirs("/content/pr4", exist_ok=True)

with open("/content/pr4/benchmark.py", "w", encoding="utf-8") as f:
    f.write('''import os
import time
import threading
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = "/content/pr4/data/http_files"
PORT = 8765
URLS = [f"http://127.0.0.1:{PORT}/file_{i}.txt"
        for i in range(20)]


def prepare_files():
    os.makedirs(BASE_DIR, exist_ok=True)
    for i in range(20):
        path = os.path.join(BASE_DIR, f"file_{i}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Test file number {i}\\n" * 100)


def download(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return len(response.read())


def measure(label, function):
    start = time.perf_counter()
    sizes = function()
    elapsed = time.perf_counter() - start
    print(f"{label}: {elapsed:.6f} sec; "
          f"files={len(sizes)}; bytes={sum(sizes)}")
    return elapsed


def sequential():
    return [download(url) for url in URLS]


def threaded():
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(download, URLS))


if __name__ == "__main__":
    prepare_files()

    server = subprocess.Popen(
        ["python", "-m", "http.server", str(PORT),
         "--directory", BASE_DIR],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        # Дожидаемся запуска локального сервера
        for _ in range(50):
            try:
                download(URLS[0])
                break
            except Exception:
                time.sleep(0.1)
        else:
            raise RuntimeError("HTTP-сервер не запустился")

        # Прогрев перед измерением не включаем в результаты
        download(URLS[0])

        sequential_time = measure("Sequential", sequential)
        threaded_time = measure("4 threads", threaded)

        print(f"Ускорение: {sequential_time / threaded_time:.2f}x")
    finally:
        server.terminate()
        server.wait()
''')
!python /content/pr4/benchmark.py
Sequential: 0.019723 sec; files=20; bytes=39000
4 threads: 0.017824 sec; files=20; bytes=39000
Ускорение: 1.11x
print("Файл /content/pr4/benchmark.py успешно записан!")
