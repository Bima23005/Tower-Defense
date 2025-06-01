import heapq
import time

# Grid
grid = [
    ['S', '.', '.', 'T', '.', '.', '.'],
    ['.', 'T', '.', 'T', '.', 'T', '.'],
    ['.', 'T', '.', '.', '.', 'T', '.'],
    ['.', '.', 'T', 'T', '.', '.', '.'],
    ['T', '.', '.', '.', 'T', 'T', 'G']
]

# Tower data
towers = {
    (0, 3): {'range': 1, 'damage': 3, 'cooldown': 2, 'cd_now': 0},
    (1, 1): {'range': 1, 'damage': 2, 'cooldown': 1, 'cd_now': 0},
    (1, 3): {'range': 1, 'damage': 2, 'cooldown': 1, 'cd_now': 0},
    (1, 5): {'range': 1, 'damage': 3, 'cooldown': 3, 'cd_now': 0},
    (2, 5): {'range': 1, 'damage': 2, 'cooldown': 2, 'cd_now': 0},
    (4, 4): {'range': 1, 'damage': 3, 'cooldown': 2, 'cd_now': 0},
    (4, 5): {'range': 1, 'damage': 3, 'cooldown': 2, 'cd_now': 0}
}

# Cari start & goal
start = goal = None
for i in range(len(grid)):
    for j in range(len(grid[0])):
        if grid[i][j] == 'S':
            start = (i, j)
        elif grid[i][j] == 'G':
            goal = (i, j)

# Heuristik
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# GBFS
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
        for d in [(-1,0), (1,0), (0,-1), (0,1)]:
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

# Cetak grid
def print_grid(enemies, step):
    print(f"\n🔄 Step {step}")
    grid_out = [['.' for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'T':
                grid_out[i][j] = 'T'
            elif grid[i][j] == 'S':
                grid_out[i][j] = 'S'
            elif grid[i][j] == 'G':
                grid_out[i][j] = 'G'
    for idx, e in enumerate(enemies):
        if e['alive']:
            ei, ej = e['pos']
            grid_out[ei][ej] = f"E{idx+1}"
    for row in grid_out:
        print(' '.join(row))

# Buat banyak musuh
enemy_count = 3
enemies = []
for i in range(enemy_count):
    came_from = greedy_best_first_search(start, goal)
    path = reconstruct_path(came_from, start, goal)
    enemies.append({
        'id': i+1,
        'hp': 10,
        'path': path,
        'step': 0,
        'pos': start,
        'alive': True,
        'status': 'jalan'
    })

# Statistik
total_damage = 0
total_hits = 0
step = 0

# Simulasi
print("\n=== SIMULASI MULTI MUSUH ===")
while any(e['alive'] and e['status'] == 'jalan' for e in enemies):
    step += 1
    print_grid(enemies, step)

    # Update posisi musuh
    for e in enemies:
        if e['alive'] and e['step'] < len(e['path']):
            e['pos'] = e['path'][e['step']]
            e['step'] += 1
        elif e['alive'] and e['pos'] == goal:
            e['status'] = 'lolos'

    # Tower menyerang musuh dalam jangkauan
    for t_pos, t in towers.items():
        if t['cd_now'] == 0:
            # Cari musuh dalam jangkauan
            targets = [e for e in enemies if e['alive'] and in_range(t_pos, e['pos'], t['range'])]
            if targets:
                target = targets[0]  # ambil pertama saja
                target['hp'] -= t['damage']
                print(f"💥 Tower {t_pos} menyerang E{target['id']} (-{t['damage']})")
                total_damage += t['damage']
                total_hits += 1
                if target['hp'] <= 0:
                    target['alive'] = False
                    target['status'] = 'mati'
                t['cd_now'] = t['cooldown']
        else:
            t['cd_now'] = max(0, t['cd_now'] - 1)

    time.sleep(0.6)

print("\n=== SIMULASI SELESAI ===")
for e in enemies:
    print(f"- E{e['id']} status: {e['status']} | HP: {e['hp']}")
print(f"\n📊 Statistik Total:")
print(f"- Serangan Tower: {total_hits}")
print(f"- Total Damage: {total_damage}")
