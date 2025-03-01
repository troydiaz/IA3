# IA3
CS 325 - Implementation Assignment 3 (SOLO)

This repository contains solutions for **Implementation Assignment 3** in CS 325, focusing on **linear programming with Gurobi**. 

---

# Setting Up and Using Gurobi in a Virtual Environment (macOS)

## 1. Creating a Virtual Environment
Before using Gurobi, create a **Python virtual environment** to manage dependencies separately from the system installation.

```sh
python3 -m venv gurobi_env
```

```
source gurobi_env/bin/activate
```

## 2. Install Gurobi Inside Virtual Environment

```
pip install gurobipy
```

And verify it:
```
python -c "import gurobipy; print(gurobipy.gurobi.version())"
```

## 3. Running Python Scripts with Gurobi
```
import gurobipy as gp
print("Gurobi is working! Version:", gp.gurobi.version())
```

## 4. Deactivating the Virtual Environment
```
deactivate
```
