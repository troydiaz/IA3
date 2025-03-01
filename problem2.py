# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# # Load and prepare the data
# data = pd.read_csv("Corvallis.csv", delimiter=";")

# # We use the 'day' column (days since May 1, 1952) as d_i and the 'average' column as T_i.
# d_values = data['day.1'].values
# T_values = data['average'].values

# # Define the periods for the two sinusoidal components.
# P_season = 365.25              # period for the annual cycle
# P_solar = 365.25 * 10.7        # period for the solar cycle

# ### Code for linear programming ###


# ###################################

# print("Optimal solution found:")
# print(f"x0 = {x0}")
# print(f"x1 = {x1}  (daily drift in °C)")
# print(f"x2 = {x2}")
# print(f"x3 = {x3}")
# print(f"x4 = {x4}")
# print(f"x5 = {x5}")
# print(f"Minimum maximum absolute deviation (E) = {E}")
# print(f"Estimated annual drift (x1 * 365.25) = {x1 * 365.25} °C/year")

# # Plot the D and T values
# plt.figure(figsize=(14, 6))
# plt.plot(d_values, T_values, 'ro', label="Data points")
# plt.xlabel("Day")
# plt.ylabel("Temperature (°C)")

# # Plot the fitted model
# d_values_sorted = np.sort(d_values)
# T_model_values = [x0 + x1 * d + x2 * np.cos(2 * np.pi * d / P_season) + x3 * np.sin(2 * np.pi * d / P_season) + x4 * np.cos(2 * np.pi * d / P_solar) + x5 * np.sin(2 * np.pi * d / P_solar) for d in d_values_sorted]
# plt.plot(d_values_sorted, T_model_values, 'b-', label="Fitted model")

# # Plot the linear trend
# d_values_sorted = np.sort(d_values)
# T_trend_values = [x0 + x1 * d for d in d_values_sorted]
# plt.plot(d_values_sorted, T_trend_values, 'g-', label="Linear trend")

# plt.title("Temperature Fit with Seasonal and Solar Components")
# plt.legend()
# plt.show()

# # Save the plot
# plt.savefig("temperature_fit.png")
# print("Plot saved as 'temperature_fit.png'")

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Read the CSV file with a semicolon delimiter
    data = pd.read_csv("Corvallis.csv", delimiter=';')
    print("CSV columns found:", data.columns.tolist())
    
    # Use the proper columns:
    # Based on the header, we expect:
    # - "average" for the average daily temperature.
    # - "day.1" for the number of days since May 1, 1952 (the last column).
    if "average" in data.columns and "day.1" in data.columns:
        T_vals = data["average"].values
        d_vals = data["day.1"].values
    else:
        # If the expected names are not found, use the last two columns as fallback.
        T_vals = data.iloc[:, -2].values
        d_vals = data.iloc[:, -1].values
        print("Warning: Using the last two columns as temperature and day data respectively.")
    
    # Create the Gurobi model
    m = gp.Model("problem2_minmax")
    
    # Add variables for the temperature model:
    # T(d) = x0 + x1*d + x2*cos(2π*d/365.25) + x3*sin(2π*d/365.25)
    #        + x4*cos(2π*d/(365.25*10.7)) + x5*sin(2π*d/(365.25*10.7))
    x0 = m.addVar(lb=-GRB.INFINITY, name="x0")
    x1 = m.addVar(lb=-GRB.INFINITY, name="x1")
    x2 = m.addVar(lb=-GRB.INFINITY, name="x2")
    x3 = m.addVar(lb=-GRB.INFINITY, name="x3")
    x4 = m.addVar(lb=-GRB.INFINITY, name="x4")
    x5 = m.addVar(lb=-GRB.INFINITY, name="x5")
    t  = m.addVar(lb=0,             name="t")  # t is the maximum absolute deviation
    
    # Objective: minimize t
    m.setObjective(t, GRB.MINIMIZE)
    
    # Add constraints for each data point (d_i, T_i)
    # Ensure that |predicted - T_i| <= t.
    for d_i, T_i in zip(d_vals, T_vals):
        cos_year  = np.cos(2 * np.pi * d_i / 365.25)
        sin_year  = np.sin(2 * np.pi * d_i / 365.25)
        cos_solar = np.cos(2 * np.pi * d_i / (365.25 * 10.7))
        sin_solar = np.sin(2 * np.pi * d_i / (365.25 * 10.7))
        
        pred = (x0 +
                x1 * d_i +
                x2 * cos_year +
                x3 * sin_year +
                x4 * cos_solar +
                x5 * sin_solar)
        
        m.addConstr(pred - T_i <= t)
        m.addConstr(-(pred - T_i) <= t)
    
    # Solve the model
    m.optimize()
    
    # Print the results
    print("Status:", m.status)
    print("x0 =", x0.X)
    print("x1 =", x1.X)
    print("x2 =", x2.X)
    print("x3 =", x3.X)
    print("x4 =", x4.X)
    print("x5 =", x5.X)
    print("Minimized max deviation (t) =", t.X)
    
    # Compute the warming/cooling trend in °C per century (x1 is in °C per day)
    trend_per_century = x1.X * 365.25 * 100
    if x1.X > 0:
        print(f"Warming trend: {trend_per_century:.4f} °C per century.")
    else:
        print(f"Cooling trend: {trend_per_century:.4f} °C per century.")
    
    # Plotting: show raw data, the best-fit curve, and the linear trend.
    plt.figure(figsize=(10, 6))
    plt.scatter(d_vals, T_vals, color="blue", s=5, label="Raw Data")
    
    # Generate a smooth range of d values for plotting the curve
    d_plot = np.linspace(min(d_vals), max(d_vals), 500)
    T_plot = []
    T_linear = []
    for d in d_plot:
        cy = np.cos(2 * np.pi * d / 365.25)
        sy = np.sin(2 * np.pi * d / 365.25)
        cS = np.cos(2 * np.pi * d / (365.25 * 10.7))
        sS = np.sin(2 * np.pi * d / (365.25 * 10.7))
        pred_val = (x0.X +
                    x1.X * d +
                    x2.X * cy +
                    x3.X * sy +
                    x4.X * cS +
                    x5.X * sS)
        T_plot.append(pred_val)
        T_linear.append(x0.X + x1.X * d)
    
    plt.plot(d_plot, T_plot, color="red", label="Best Fit Curve")
    plt.plot(d_plot, T_linear, color="green", linestyle="--", label="Linear Trend")
    
    plt.xlabel("Day (since May 1, 1952)")
    plt.ylabel("Average Temperature (°C)")
    plt.title("Problem 2: Best Fit Temperature Curve")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
