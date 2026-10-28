%%writefile wait_for_graph.py
def find_cycle(graph):
    visited = set()
    active = set()

    def dfs(node):
        visited.add(node)
        active.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in active:
                return True

        active.remove(node)
        return False

    for node in graph:
        if node not in visited and dfs(node):
            return True

    return False

deadlocked = {
    "P0": ["P1"],
    "P1": ["P2"],
    "P2": ["P0"],
}

no_deadlock = {
    "P0": ["P1"],
    "P1": ["P2"],
    "P2": [],
  }

print("Граф с циклом:", "DEADLOCK" if find_cycle(deadlocked) else "NO DEADLOCK")
print("Граф без цикла:", "DEADLOCK" if find_cycle(no_deadlock) else "NO DEADLOCK")
Writing wait_for_graph.py
!python3 wait_for_graph.py
Граф с циклом: DEADLOCK
Граф без цикла: NO DEADLOCK
