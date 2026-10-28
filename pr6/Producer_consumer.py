import threading
import time
import random
import queue

# Создаем потокобезопасную очередь с максимальным размером 3
buffer = queue.Queue(maxsize=3)

# Флаг для контролируемой остановки потоков
stop_event = threading.Event()

def producer():
    item_id = 1
    while not stop_event.is_set():
        print(f"[Producer] Пытается добавить элемент #{item_id}...")
        
        # Если очередь полна (3 элемента), этот метод заблокирует поток и будет ждать
        buffer.put(item_id)
        
        print(f" -> [Producer] УСПЕШНО добавил #{item_id} (В очереди: {buffer.qsize()})")
        item_id += 1
        
        # Производитель работает чуть быстрее потребителя, чтобы искусственно заполнить очередь
        time.sleep(random.uniform(0.1, 0.3))

def consumer():
    while not stop_event.is_set():
        # Имитируем долгую "обработку" элемента потребителем
        time.sleep(random.uniform(0.5, 0.8))
        
        if buffer.empty() and stop_event.is_set():
            break
            
        print(f"    [Consumer] Пытается забрать элемент...")
        # Если очередь пуста, этот метод заблокирует поток и будет ждать появления элементов
        item = buffer.get()
        
        print(f"     -> [Consumer] УСПЕШНО обработал #{item} (Осталось: {buffer.qsize()})")
        
        # Сигнализируем очереди, что задача по этому элементу выполнена
        buffer.task_done()

# Создаем потоки
prod_thread = threading.Thread(target=producer, name="Producer")
cons_thread = threading.Thread(target=consumer, name="Consumer")

print("--- Старт симуляции (Очередь maxsize=3) ---")
prod_thread.start()
cons_thread.start()

# Даем симуляции поработать 5 секунд в прямом эфире Colab
try:
    time.sleep(5)
finally:
    print("\n--- Останавливаем потоки... ---")
    stop_event.set()
    
    # Извлекаем оставшиеся элементы, чтобы разблокировать put(), если производитель завис на заполнении
    while not buffer.empty():
        try:
            buffer.get_nowait()
            buffer.task_done()
        except queue.Empty:
            break

    prod_thread.join()
    cons_thread.join()
    print("Программа успешно завершена.")
--- Старт симуляции (Очередь maxsize=3) ---
[Producer] Пытается добавить элемент #1...
 -> [Producer] УСПЕШНО добавил #1 (В очереди: 1)
[Producer] Пытается добавить элемент #2...
 -> [Producer] УСПЕШНО добавил #2 (В очереди: 2)
[Producer] Пытается добавить элемент #3...
 -> [Producer] УСПЕШНО добавил #3 (В очереди: 3)
[Producer] Пытается добавить элемент #4...
    [Consumer] Пытается забрать элемент...
     -> [Consumer] УСПЕШНО обработал #1 (Осталось: 2)
 -> [Producer] УСПЕШНО добавил #4 (В очереди: 3)
[Producer] Пытается добавить элемент #5...
    [Consumer] Пытается забрать элемент...
     -> [Consumer] УСПЕШНО обработал #2 (Осталось: 2)
 -> [Producer] УСПЕШНО добавил #5 (В очереди: 3)
[Producer] Пытается добавить элемент #6...
    [Consumer] Пытается забрать элемент...
     -> [Consumer] УСПЕШНО обработал #3 (Осталось: 2)
 -> [Producer] УСПЕШНО добавил #6 (В очереди: 3)
[Producer] Пытается добавить элемент #7...
    [Consumer] Пытается забрать элемент...
     -> [Consumer] УСПЕШНО обработал #4 (Осталось: 2)
 -> [Producer] УСПЕШНО добавил #7 (В очереди: 3)
[Producer] Пытается добавить элемент #8...
    [Consumer] Пытается забрать элемент...
     -> [Consumer] УСПЕШНО обработал #5 (Осталось: 2)
 -> [Producer] УСПЕШНО добавил #8 (В очереди: 3)
[Producer] Пытается добавить элемент #9...
    [Consumer] Пытается забрать элемент...
     -> [Consumer] УСПЕШНО обработал #6 (Осталось: 2)
 -> [Producer] УСПЕШНО добавил #9 (В очереди: 3)
[Producer] Пытается добавить элемент #10...
    [Consumer] Пытается забрать элемент...
     -> [Consumer] УСПЕШНО обработал #7 (Осталось: 2)
 -> [Producer] УСПЕШНО добавил #10 (В очереди: 3)
[Producer] Пытается добавить элемент #11...
    [Consumer] Пытается забрать элемент...
     -> [Consumer] УСПЕШНО обработал #8 (Осталось: 2)
 -> [Producer] УСПЕШНО добавил #11 (В очереди: 3)

--- Останавливаем потоки... ---
Программа успешно завершена.
