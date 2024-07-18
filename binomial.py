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
    # For each row start column is N-1
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
    # For each row start column is 0
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

def AMO(variables):
    clauses = []
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            clauses.append([-variables[i], -variables[j]])
    return clauses


def generate_clauses(n, variables):
    clauses = []
    # Exactly one queen in each row
    for i in range(n):
        # ALO
        clauses.append(variables[i]) # variables[i] is a list of n variables in one row
        # AMO: combinations of two variables in one row
        clauses.extend(AMO(variables[i]))
                
    # Exactly one queen in each column
    cols = []
    for j in range(n):
        # ALO
        clauses.append([variables[i][j] for i in range(n)]) # variables[i] is a list of n variables in one column
        cols.append([variables[i][j] for i in range(n)])
    # AMO: combinations of two variables in one column
    for col in cols:
        clauses.extend(AMO(col))

    diagonals = get_all_diagonals(variables)
    print(diagonals)
    for diagonal in diagonals:
        clauses.extend(AMO(diagonal))
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
        solution = []
        for i in range(n):
            sol = []
            for j in range(n):
                if int(model[i * n + j]) > 0:
                    sol.append(1)
                else:
                    sol.append(0)
            solution.append(sol)
        return solution
    else:
        return None
    
def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))

n = 8
solution = solve_n_queens(n)
print_solution(solution)