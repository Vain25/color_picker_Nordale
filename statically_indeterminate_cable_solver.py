import sympy as sp
import numpy as np

def get_input(prompt):
    user_val = input(prompt).strip()
    try:
        # Try to treat it as a number
        return sp.Float(user_val)
    except:
        # If not a number, treat it as a symbolic variable
        return sp.Symbol(user_val)

print("--- Fully Symbolic/Numeric Structural Analyzer ---")
print("Enter a number (e.g., 135000) or a variable (e.g., w, L, a).")

# 1. Prompting for every single input
w = get_input("Enter Distributed Load (w): ")
L = get_input("Enter Beam Length (L): ")
E = get_input("Enter Young's Modulus (E): ")
sy = get_input("Enter Yield Strength (σy): ")

d_in = input("Enter Diameter (d) or leave blank for Area (A): ").strip()
if d_in:
    try:
        d = sp.Float(d_in)
    except:
        d = sp.Symbol(d_in)
    A = sp.pi * (d / 2)**2
else:
    A = get_input("Enter Area (A): ")

# Prompting for Geometry (Verbatim from image_1e1b7d.jpg)
print("\n--- Cable Geometry ---")
x_coords = []
y_coords = []
for i in range(4):
    x = get_input(f"Cable {i+1} distance from pivot B (x{i+1}): ")
    y = get_input(f"Cable {i+1} height on tower (y{i+1}): ")
    x_coords.append(x)
    y_coords.append(y)

# 2. Symbolic Calculations
theta = sp.Symbol('theta')
moment_load = (w * L**2) / 2

stiffness_contribution = 0
cable_results = []

for i in range(4):
    xi = x_coords[i]
    yi = y_coords[i]
    
    # Geometry formulas
    Li = sp.sqrt(xi**2 + yi**2)
    sin_phi = yi / Li  # vertical component
    
    # Tension T_i = (A*E/L_i) * (xi * theta * sin_phi)
    Ti = (A * E / Li) * (xi * theta * sin_phi)
    
    # Moment contribution: T_i * sin_phi * xi
    stiffness_contribution += Ti * sin_phi * xi
    cable_results.append((Ti, Li))

# 3. Solve for theta: Sum of Moments = 0
# moment_load = stiffness_contribution
final_theta = sp.solve(sp.Eq(moment_load, stiffness_contribution), theta)[0]

# 4. Final Outputs
print("\n" + "="*50)
print("FINAL RESULTS")
print("="*50)
print(f"Angular Rotation (theta) = {sp.simplify(final_theta)}")

for i in range(4):
    Ti_final = cable_results[i][0].subs(theta, final_theta)
    stress = Ti_final / A
    fos = sy / stress
    
    print(f"\n--- Cable {i+1} ---")
    print(f"Tension: {sp.simplify(Ti_final)}")
    print(f"Factor of Safety: {sp.simplify(fos)}")