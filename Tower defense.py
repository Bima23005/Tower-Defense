import heapq
import time

# Grid simbol
# S: Start, G: Goal, T: Tower, .: Kosong
grid = [
    ['S', '.', '.', 'T', '.', '.', '.'],
    ['.', 'T', '.', 'T', '.', 'T', '.'],
    ['.', 'T', '.', '.', '.', 'T', '.'],
    ['.', '.', 'T', 'T', '.', '.', '.'],
    ['T', '.', '.', '.', 'T', 'T', 'G']
]

# Tower dengan posisi, range, damage, dan cooldown
towers = {
    (0, 3): {'range': 1, 'damage': 3, 'cooldown': 2, 'cd_now': 0},
    (1, 1): {'range': 1, 'damage': 2, 'cooldown': 1, 'cd_now': 0},
    (1, 3): {'range': 1, 'damage': 2, 'cooldown': 1, 'cd_now': 0},
    (1, 5): {'range': 1, 'damage': 3, 'cooldown': 3, 'cd_now': 0},
    (2, 5): {'range': 1, 'damage': 2, 'cooldown': 2, 'cd_now': 0},
    (4, 4): {'range': 1, 'damage': 3, 'cooldown': 2, 'cd_now': 0},
    (4, 5): {'range': 1, 'damage': 3, 'cooldown': 2, 'cd_now': 0}
}

start = goal = None
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 'S':
            start = (i, j)
        elif grid[i][j] == 'G':
            goal = (i, j)

# Heuristik Manhattan
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Arah gerakan
directions = [(-1,0), (1,0), (0,-1), (0,1)]

# GBFS dengan pelacakan jalur
def greedy_best_first_search(start, goal):
    visited = set()
    came_from = {}
    queue = []
    heapq.heappush(queue, (heuristic(start, goal), start))

    while queue:
        _, current = heapq.heappop(queue)
        if current == goal:
            break
        if current in visited:
            continue
        visited.add(current)
        for d in directions:
            ni, nj = current[0] + d[0], current[1] + d[1]
            if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]):
                if grid[ni][nj] != 'T' and (ni, nj) not in visited:
                    heapq.heappush(queue, (heuristic((ni, nj), goal), (ni, nj)))
                    came_from[(ni, nj)] = current
    return came_from

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []
    path.reverse()
    return path

def in_range(tower_pos, target_pos, range_val):
    return heuristic(tower_pos, target_pos) <= range_val

def print_grid_with_enemy(path, pos, step):
    print(f"\n📍 Step {step} | Posisi Musuh: {pos}")
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) == pos:
                print('E', end=' ')
            elif (i, j) in path and grid[i][j] == '.':
                print('*', end=' ')
            else:
                print(grid[i][j], end=' ')
        print()

# Enemy setup
enemy = {
    'hp': 12,
    'pos': start
}

# Simulasi jalan
came_from = greedy_best_first_search(start, goal)
path = reconstruct_path(came_from, start, goal)

# Statistik
total_damage = 0
total_hits = 0

print("\n--- SIMULASI DIMULAI ---")
for step, pos in enumerate(path, 1):
    enemy['pos'] = pos
    print_grid_with_enemy(path, pos, step)

    # Tower menyerang bila cooldown 0
    for tower_pos, info in towers.items():
        if info['cd_now'] == 0 and in_range(tower_pos, pos, info['range']):
            enemy['hp'] -= info['damage']
            total_damage += info['damage']
            total_hits += 1
            print(f"  💥 Tower {tower_pos} menyerang! (-{info['damage']} HP)")
            info['cd_now'] = info['cooldown']  # reset cooldown
        else:
            info['cd_now'] = max(0, info['cd_now'] - 1)

    print(f"  ❤️ HP Musuh: {enemy['hp']}")
    if enemy['hp'] <= 0:
        print("❌ Musuh mati di tengah jalan.")
        break
    elif pos == goal:
        print("🎯 Musuh berhasil mencapai tujuan!")
        break

    time.sleep(0.7)

print("\n--- SIMULASI SELESAI ---")
print(f"\n📊 Statistik:")
print(f"- Langkah dilalui: {step}")
print(f"- Total serangan tower: {total_hits}")
print(f"- Total damage diterima: {total_damage}")
print(f"- Status akhir: {'Mati' if enemy['hp'] <= 0 else 'Lolos'}")
