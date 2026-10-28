import threading
import time
import random

# Инициализация начальных данных
accounts = {
    "Alice": 1000,
    "Bob": 1000,
    "Charlie": 1000
}

# Фиксируем начальную общую сумму для проверки инварианта
initial_total = sum(accounts.values())

# Создаем один общий лок для защиты критической секции
transfer_lock = threading.Lock()

def transfer(sender, receiver, amount):
    # Защищаем проверку баланса, списание и зачисление одним локом
    with transfer_lock:
        if accounts[sender] >= amount:
            # Имитируем небольшую задержку внутри критической секции
            time.sleep(random.uniform(0.01, 0.05))
            
            accounts[sender] -= amount
            accounts[receiver] += amount
            print(f"[УСПЕХ] {sender} перевел {amount} для {receiver}")
        else:
            print(f"[ОТКЛОНЕНО] У {sender} недостаточно средств для перевода {amount}")
        
        # Проверяем инвариант: общая сумма всех аккаунтов не должна меняться
        current_total = sum(accounts.values())
        assert current_total == initial_total, f"Ошибка! Общая сумма изменилась: {current_total} вместо {initial_total}"

def worker_loop():
    names = list(accounts.keys())
    for _ in range(5):
        sender, receiver = random.sample(names, 2)
        amount = random.randint(50, 300)
        transfer(sender, receiver, amount)

# Создаем и запускаем несколько потоков, имитирующих одновременные переводы
threads = []
print(f"Начальный баланс: {accounts} (Всего: {initial_total})\n")

for i in range(3):
    t = threading.Thread(target=worker_loop, name=f"Thread-{i+1}")
    threads.append(t)
    t.start()

# Ждем завершения всех потоков
for t in threads:
    t.join()

print(f"\nИтоговый баланс: {accounts} (Всего: {sum(accounts.values())})")
Начальный баланс: {'Alice': 1000, 'Bob': 1000, 'Charlie': 1000} (Всего: 3000)

[УСПЕХ] Alice перевел 269 для Bob
[УСПЕХ] Bob перевел 183 для Alice
[УСПЕХ] Alice перевел 122 для Bob
[УСПЕХ] Alice перевел 161 для Bob
[УСПЕХ] Bob перевел 255 для Charlie
[УСПЕХ] Alice перевел 273 для Bob
[УСПЕХ] Charlie перевел 62 для Alice
[УСПЕХ] Bob перевел 68 для Alice
[УСПЕХ] Charlie перевел 186 для Alice
[УСПЕХ] Alice перевел 188 для Bob
[УСПЕХ] Bob перевел 298 для Charlie
[УСПЕХ] Bob перевел 70 для Charlie
[УСПЕХ] Bob перевел 148 для Alice
[УСПЕХ] Bob перевел 73 для Charlie
[УСПЕХ] Alice перевел 181 для Bob

Итоговый баланс: {'Alice': 453, 'Bob': 1099, 'Charlie': 1448} (Всего: 3000)
