from pysat.solvers import Glucose3
import math
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

# Generate all binary strings of length n
def generate_binary_string(n):
    binary_string = []
    def genbin(n, bs = ''):
        if (len(bs) == n):
            binary_string.append(bs)
        else:
            genbin(n, bs + '0')
            genbin(n, bs + '1')
    genbin(n)
    return binary_string

# AMO for a list of variables
def AMO_binary(list):
    clauses = []
    global max_idy
    log2_n = math.ceil(math.log2(len(list))) # number of aux vars
    aux_vars = []
    for i in range(log2_n):
        aux_vars.append(max_idy)
        max_idy += 1
    bin_strings = generate_binary_string(log2_n)
    for i in range(len(list)):
        string = bin_strings[i]
        for id in range(log2_n):
            if string[log2_n - 1 - id] == '1':
                clauses.append([-list[i], aux_vars[id]])
            else:
                clauses.append([-list[i], -aux_vars[id]])
    return clauses

def generate_clauses(n, variables):
    clauses = []
    # Exactly one queen in each row
    for i in range(n):
        # AtLeast One
        clauses.append(variables[i])
        # AtMost One for each row
        clauses.extend(AMO_binary(variables[i])) 

    # Exactly one queen in each column
    cols = []
    for j in range(n):
        #AtLeast One 
        clauses.append([variables[i][j] for i in range(n)])
        # List of columns
        cols.append([variables[i][j] for i in range(n)])
    #AMO for each column
    for col in cols:
        clauses.extend(AMO_binary(col))

    # At most one queen in each diagonal
    diagonals = get_all_diagonals(variables)
    for diagonal in diagonals:
        clauses.extend(AMO_binary(diagonal))
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
max_idy = n * n + 1
solution = solve_n_queens(n)
print_solution(solution)