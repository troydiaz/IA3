import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt

def main():
    # The problem data (x_i, y_i)
    points = [(1,3), (2,5), (3,7), (5,11), (7,14), (8,15), (10,19)]
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]

    # Create the Gurobi model
    m = gp.Model("problem1_minmax")

    # a = slope, b = intercept, t = max deviation 
    a = m.addVar(lb=-GRB.INFINITY, name="a")
    b = m.addVar(lb=-GRB.INFINITY, name="b")
    t = m.addVar(lb=0,             name="t") 

    m.setObjective(t, GRB.MINIMIZE)

    # |a*x + b - y| <= t
    for i, (xi, yi) in enumerate(points):
        # a*xi + b - yi <= t
        m.addConstr(a*xi + b - yi <= t, name=f"upper_{i}")
        # -(a*xi + b - yi) <= t  =>  yi - (a*xi + b) <= t
        m.addConstr(-(a*xi + b - yi) <= t, name=f"lower_{i}")

    m.optimize()

    # Solution
    a_opt = a.X
    b_opt = b.X
    t_opt = t.X
    print(f"STATUS: {m.status}")
    print(f"Optimal line: y = {a_opt} * x + {b_opt}")
    print(f"Minimized max deviation (t): {t_opt}")

    # Plot the original data
    plt.figure()
    plt.scatter(x_vals, y_vals, color='blue', label='Data Points')
    
    # Generate best fitted line
    x_line = range(min(x_vals), max(x_vals)+1)
    y_line = [a_opt * x + b_opt for x in x_line]
    plt.plot(x_line, y_line, color='red', label='MinMax Line')

    # Labels and legend
    plt.title("Problem 1: Minimize Maximum Absolute Deviation")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
