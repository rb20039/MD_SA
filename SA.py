from itertools import combinations_with_replacement, permutations
import random
import math

def cost(columns, grid):
    rating = 0
    for i, columnog in enumerate(columns):
        column = columnog[:]
        cur_rating = 0
        count = column.pop(0)
        start = True
        for y in range(len(grid)):
            if len(column) > 0 and grid[y][i] == 0 and count == 0:
                count = column.pop(0)
                start = True
            elif grid[y][i] == 1 and count > 0:
                count -= 1
                start = False
            elif grid[y][i] == 1 and count == 0:
                cur_rating += 1
            elif len(column) > 0 and grid[y][i] == 0 and count > 0 and start == False:
                cur_rating += 1 + count
                count = column.pop(0)
        if count > 0:
            cur_rating += count
        if len(column) > 0:
            for num in column:
                cur_rating += num
        rating += cur_rating
    return -rating


def possible_permutations(row, width):
    filled = sum(row) + len(row) - 1
    spaces = width - filled
    
    result = []

    for combination in combinations_with_replacement(range(0, spaces+1), len(row)+1):
        if sum(combination) == spaces:
            for perm in permutations(combination):
                if perm not in result:
                    result.append(perm)

    valid_lines = []
    for spaces_config in result:
        line = [0] * width
        position = 0
        for i, block in enumerate(row):
            position += spaces_config[i]
            for j in range(block):
                line[position + j] = 1
            position += block+1
        valid_lines.append(line)
    
    return valid_lines

def step(row, width):
    perms = possible_permutations(row, width)
    if row in perms:
        return random.choice(perms.remove(row))
    else: 
        return random.choice(perms)

def grid_update(rows, grid):
    row_weights = [[0] for i in range(len(grid))]
    sum_weights = 0
    for i, grid_row in enumerate(grid):
        row_weights[i] = len(possible_permutations(rows[i], len(grid_row)))
        sum_weights += row_weights[i]
    for i, weight in enumerate(row_weights):
        row_weights[i] = weight/sum_weights
    chosen = random.choices(range(0, len(rows)), row_weights)[0]
    grid[chosen] = step(rows[chosen], len(grid[chosen]))
    return grid



def printng(grid):
    for gridrows in grid:
        for gridcolumn in gridrows:
            if gridcolumn == 0:
                print("_", end='')
            else:
                print("X", end='')
        print()

def main():
    f = open("ng2.txt", "r")
    width, height, rows, columns = f.read().split("\n")
    width, height = int(width), int(height)

    rows = [[int(n) for n in line.split(",")] for line in rows[1:-1].split('","')]
    columns = [[int(n) for n in line.split(",")] for line in columns[1:-1].split('","')]

    domain = [[0]*width for i in range(height)]
    for i, rowog in enumerate(rows):
        row = rowog[:]
        domain[i] = step(row, width)
    domain_eval = cost(columns, domain)

    current_domain, current_eval = domain[:], domain_eval
    # candidate_domain
    # Simulated Annealing
    iterations = 10000
    step_size = 0.01
    temp = 10
    for i in range(iterations):
        t = temp / float(i + 1)
        candidate = grid_update(rows, current_domain)
        candidate_eval = cost(columns, candidate)
        if candidate_eval > domain_eval or random.random() < math.exp((current_eval - candidate_eval) / t):
            current_domain, current_eval = candidate[:], candidate_eval
            if candidate_eval > domain_eval:
                domain, domain_eval = current_domain[:], candidate_eval
        
        if i % 100 == 0:
            print(f"Iteration {i}, Temperature {t:.3f}, Best Evaluation {domain_eval:.5f}")
        
        if domain_eval == 0:
            break


    printng(domain)
    printng(grid_update(rows, domain))




main()

        
  


