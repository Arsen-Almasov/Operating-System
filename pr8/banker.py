%%writefile banker.py
import sys

def read_state(filename):
    with open(filename, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    available = tuple(map(int, lines[0].split(":")[1].split()))
    a_idx = lines.index("Allocation:")
    m_idx = lines.index("Max:")

    allocation = [
        tuple(map(int, lines[i].split()))
        for i in range(a_idx + 1, m_idx)
    ]
    maximum = [
        tuple(map(int, lines[i].split()))
        for i in range(m_idx + 1, len(lines))
    ]

    if len(allocation) != len(maximum):
        raise ValueError("Allocation и Max должны иметь одинаковое число строк.")
    if any(len(x) != len(available) for x in allocation + maximum):
        raise ValueError("Размеры векторов не совпадают.")
    if any(maximum[i][j] < allocation[i][j]
           for i in range(len(allocation))
           for j in range(len(available))):
        raise ValueError("Max не может быть меньше Allocation.")

    need = [
        tuple(maximum[i][j] - allocation[i][j]
              for j in range(len(available)))
        for i in range(len(allocation))
    ]
    return list(available), allocation, maximum, need

def safe_sequence(available, allocation, need):
    work = available[:]
    finished = [False] * len(allocation)
    sequence = []

    while len(sequence) < len(allocation):
        found = False

        for i in range(len(allocation)):
            if finished[i]:
                continue

            if all(need[i][j] <= work[j] for j in range(len(work))):
                work = [
                    work[j] + allocation[i][j]
                    for j in range(len(work))
                ]
                finished[i] = True
                sequence.append(f"P{i}")
                found = True
                break

        if not found:
            return False, []

    return True, sequence

def request_resources(state, process, request):
    available, allocation, maximum, need = (
        state[0][:],
        [list(x) for x in state[1]],
        state[2],
        [list(x) for x in state[3]]
    )

    if any(request[j] > need[process][j] for j in range(len(request))):
        return False, "Запрос превышает Need процесса."
    if any(request[j] > available[j] for j in range(len(request))):
        return False, "Недостаточно доступных ресурсов."

    # Временно выдаём ресурсы и проверяем безопасность состояния.
    for j in range(len(request)):
        available[j] -= request[j]
        allocation[process][j] += request[j]
        need[process][j] -= request[j]

    safe, sequence = safe_sequence(available, allocation, need)
    if safe:
        return True, "Запрос разрешён. Безопасная последовательность: " + " -> ".join(sequence)

    return False, "Запрос отклонён: состояние небезопасно."

def main():
    filenames = sys.argv[1:] or ["bank1.txt", "bank2.txt"]

    for filename in filenames:
        state = read_state(filename)
        available, allocation, maximum, need = state

        print(f"\n=== {filename} ===")
        print("Need = Max - Allocation:")
        for i, row in enumerate(need):
            print(f"P{i}: {row}")

        safe, sequence = safe_sequence(available, allocation, need)
        if safe:
            print("SAFE")
            print("Безопасная последовательность:", " -> ".join(sequence))
        else:
            print("UNSAFE")

        if filename == "bank1.txt":
            granted, message = request_resources(state, 1, (1, 0, 2))
            print("Запрос P1 (1, 0, 2):", message)

if __name__ == "__main__":
    main()
  Writing banker.py
