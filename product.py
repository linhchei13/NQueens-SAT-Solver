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


def AMO_product(variables):
    clauses = []
    rows = []
    colummns = []
    n = len(variables)
    p = math.ceil(math.sqrt(n)) # number of rows)
    q = math.ceil(n / p) # number of columns
    global max_id
    # Generate variables for grid's rows and columns
    for i in range(p):
        rows.append(max_id)
        max_id += 1
    for i in range(q):
        colummns.append(max_id)
        max_id += 1
    # AMO for rows, columns of grid
    for i in range(p):
        for j in range(i + 1, p):
            clauses.append([-rows[i], -rows[j]])
    for i in range(q):
        for j in range(i + 1, q):
            clauses.append([-colummns[i], -colummns[j]])
    # One point of grid for each variable
    for i in range(p):
        group = []
        for j in range(q):
            if (i * q + j < n):
                clauses.append([-variables[i * q + j], rows[i]])
                clauses.append([-variables[i * q + j], colummns[j]])
    return clauses

def generate_clauses(n, variables):
    clauses = []
    # Exactly one queen in each row
    for i in range(n):
        # ALO
        clauses.append(variables[i]) # variables[i] is a list of n variables in one row
        # AMO: combinations of two variables in one row
        clauses.extend(AMO_product(variables[i]))
    # Exactly one queen in each column
    cols = []
    for j in range(n):
        #AtLeast One 
        clauses.append([variables[i][j] for i in range(n)])
        # List of columns
        cols.append([variables[i][j] for i in range(n)])
    for col in cols:
        clauses.extend(AMO_product(col))
            
    # At most one queen in each diagonal
    diagonals = get_all_diagonals(variables)
    for diagonal in diagonals:
        if (len(diagonal) > 1):
            clauses.extend(AMO_product(diagonal))
    print(clauses)
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