import math
from pysat.solvers import Glucose3
def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

def get_all_diagonals(variables):
    diagonals = []
    n = len(variables)
    # Main diagonals
    for col in range(n):
        diagonal = []
        startcol = col
        startrow = 0
        while(startcol < n and startrow < n):
            diagonal.append(variables[startrow][startcol])
            startcol += 1
            startrow += 1
        diagonals.append(diagonal)
    # For each row start column is 0
    for row in range(1, n):
        diagonal = []
        startrow = row
        startcol = 0
        while(startrow < n and startcol < n):
            diagonal.append(variables[startrow][startcol])
            startcol += 1
            startrow += 1
        diagonals.append(diagonal)
    # Anti-diagonals
    for col in range(n):
        diagonal = []
        startcol = col
        startrow = 0
        while(startcol >= 0 and startrow < n):
            diagonal.append(variables[startrow][startcol])
            startcol -= 1
            startrow += 1
        diagonals.append(diagonal)
    # For each row start column is N-1
    for row in range(1, n):
        diagonal = []
        startrow = row
        startcol = n - 1
        while(startrow < n and startcol >= 0):
            diagonal.append(variables[startrow][startcol])
            startcol -= 1
            startrow += 1
        diagonals.append(diagonal)
    return diagonals

def AMO_commander(variables):
    clauses = []
    G = []
    C = []
    n = len(variables)
    m = int(math.sqrt(n)) # number of groups
    k = int(n / m)
    global max_id
    for i in range(m):
        C.append(max_id)
        max_id += 1
    # AMO for C
    for i in range(m):
        for j in range(i + 1, m):
            clauses.append([-C[i], -C[j]])
    # ALO, AMO for C and variables
    for i in range(m):
        group = []
        for j in range(k):
            if (i * k + j < n):
                group.append(variables[i * k + j])
        G.append(group)
    for k in range(m):
        group = G[k]
        list = [-C[k]]
        list.extend(group)
        clauses.append(list)
        for i in range (len(group)):
            clauses.append([C[k], -group[i]])
            for j in range(i + 1, len(group)):
                clauses.append([-C[k],-group[i], -group[j]])
    return clauses

def generate_clauses(n, variables):
    clauses = []
    # Exactly one queen in each row
    for i in range(n):
        # ALO
        clauses.append(variables[i]) # variables[i] is a list of n variables in one row
        # AMO: combinations of two variables in one row
        clauses.extend(AMO_commander(variables[i]))
    # Exactly one queen in each column
    cols = []
    for j in range(n):
        #AtLeast One 
        clauses.append([variables[i][j] for i in range(n)])
        # List of columns
        cols.append([variables[i][j] for i in range(n)])
    for col in cols:
        clauses.extend(AMO_commander(col))
            
    # At most one queen in each diagonal
    diagonals = get_all_diagonals(variables)
    for diagonal in diagonals:
        if (len(diagonal) > 1):
            clauses.extend(AMO_commander(diagonal))
    return clauses

def solve_n_queens(n):
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)
    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)
    if solver.solve():
        model = solver.get_model()
        print(model)
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
    else:
        return None
    
def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))
n = 8
max_id = n * n + 1
solution = solve_n_queens(n)
print_solution(solution)