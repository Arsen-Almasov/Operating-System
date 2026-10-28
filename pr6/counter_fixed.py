import threading
import time

# Общее количество инкрементов, которое должен сделать КАЖДЫЙ поток
STEPS = 100_000
# Количество одновременно работающих потоков
NUM_THREADS = 4

# --- 1. ВАРИАНТ БЕЗ БЛОКИРОВКИ (Быстро, но неточно / Race Condition) ---
shared_counter_unsafe = 0

def unsafe_worker():
    global shared_counter_unsafe
    for _ in range(STEPS):
        # Операция не атомарна, здесь возникает состояние гонки
        shared_counter_unsafe += 1

print("=== Запуск без блокировки ===")
threads = [threading.Thread(target=unsafe_worker) for _ in range(NUM_THREADS)]

start_time = time.perf_counter()
for t in threads: t.start()
for t in threads: t.join()
end_time = time.perf_counter()

duration_unsafe = end_time - start_time
expected_value = STEPS * NUM_THREADS

print(f"Ожидалось: {expected_value}")
print(f"Получено:  {shared_counter_unsafe}")
print(f"Время выполнения: {duration_unsafe:.4f} секунд")
print(f"Потеряно инкрементов: {expected_value - shared_counter_unsafe}")
print("-" * 40)


# --- 2. ВАРИАНТ С БЛОКИРОВКОЙ (Медленнее, но 100% правильно / Thread-Safe) ---
shared_counter_safe = 0
lock = threading.Lock()

def safe_worker():
    global shared_counter_safe
    for _ in range(STEPS):
        # Защищаем критическую секцию
        with lock:
            shared_counter_safe += 1

print("=== Запуск с блокировкой ===")
threads = [threading.Thread(target=safe_worker) for _ in range(NUM_THREADS)]

start_time = time.perf_counter()
for t in threads: t.start()
for t in threads: t.join()
end_time = time.perf_counter()

duration_safe = end_time - start_time

print(f"Ожидалось: {expected_value}")
print(f"Получено:  {shared_counter_safe}")
print(f"Время выполнения: {duration_safe:.4f} секунд")
print("-" * 40)


# --- ИТОГОВОЕ СРАВНЕНИЕ ---
print("\n=== Результаты анализа ===")
if duration_unsafe > 0:
    slowdown = duration_safe / duration_unsafe
    print(f"Вариант с блокировкой медленнее в {slowdown:.1f} раз.")
print("Зато вариант с блокировкой гарантирует корректность данных!")
=== Запуск без блокировки ===
Ожидалось: 400000
Получено:  400000
Время выполнения: 0.0572 секунд
Потеряно инкрементов: 0
----------------------------------------
=== Запуск с блокировкой ===
Ожидалось: 400000
Получено:  400000
Время выполнения: 0.1336 секунд
----------------------------------------

=== Результаты анализа ===
Вариант с блокировкой медленнее в 2.3 раз.
Зато вариант с блокировкой гарантирует корректность данных!
