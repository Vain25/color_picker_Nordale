import numpy as np
import matplotlib.pyplot as plt
import scipy

# 1. Inputs
bridge_name = input("Enter the name of the bridge: ")   
L = float(input("Enter the length (m): ")) 
E = float(input("Enter the Young's modulus (Pa): "))
I = float(input("Enter the moment of inertia (m^4): "))
w = float(input("Enter the uniform load (N/m): "))

# 2. Calculations
x = np.linspace(0, L, 100)      
y = (w * x / (24 * E * I)) * (L**3 - 2 * L * x**2 + x**3)

# 3. Plotting
plt.figure(figsize=(10, 4))
plt.plot(x, -y, label='Beam Deflection', color='red', linewidth=2)
plt.axhline(0, color='black', lw=1) 

# FIX 1: Combined the titles into one line
plt.title(f'Vertical Deflection Analysis: {bridge_name}')  

plt.xlabel('Position along the beam (m)')
plt.ylabel('Deflection (m)')
plt.grid(True, linestyle='--')
plt.legend()

# FIX 2: Calculate and print BEFORE showing the graph
max_deflection = np.max(y)
print(f"\n--- Results for {bridge_name} ---")
print(f"The maximum deflection is: {max_deflection * 1000:.2f} mm")

# FIX 3: Save the file BEFORE calling show()
plt.savefig("beam_deflection_results.png", dpi=300)

# Finally, show the window
plt.show()

