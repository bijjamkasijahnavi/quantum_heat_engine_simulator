import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from qutip import *

# User Inputs
omega_h = float(input("Enter energy level for hot bath (ωh)(positive): "))
omega_c = float(input("Enter energy level for cold bath (ωc)(positive): "))
gamma_h = float(input("Enter hot bath coupling strength: "))
gamma_c = float(input("Enter cold bath coupling strength: "))
temperature_h = float(input("Enter hot bath temperature: "))
temperature_c = float(input("Enter cold bath temperature: "))

# Constants
hbar = 1.0  

# Define quantum states
ground = basis(2, 0)
excited = basis(2, 1)
sigma_z = sigmaz()

# Define Hamiltonians
H_h = omega_h * sigma_z / 2  
H_c = omega_c * sigma_z / 2  

# Collapse operator function
def thermal_collapse_ops(omega, gamma, temperature):
    if temperature == 0:
        n = 0
    else:
        n = 1 / (np.exp(hbar * omega / (temperature)) - 1)
    return [np.sqrt(gamma * (n + 1)) * sigmam(), np.sqrt(gamma * n) * sigmap()]

# Collapse operators
c_ops_hot = thermal_collapse_ops(omega_h, gamma_h, temperature_h)
c_ops_cold = thermal_collapse_ops(omega_c, gamma_c, temperature_c)

# Time steps
t_list = np.linspace(0, 10, 500)

# Solve dynamics
result_hot = mesolve(H_h, excited, t_list, c_ops_hot, [H_h])
result_cold = mesolve(H_c, ground, t_list, c_ops_cold, [H_c])

# Extract energy expectation values
energy_hot = result_hot.expect[0] if result_hot.expect else [0] * len(t_list)
energy_cold = result_cold.expect[0] if result_cold.expect else [0] * len(t_list)

# Calculate work and efficiency
work_done = max(energy_hot) - min(energy_cold)
efficiency = work_done / max(energy_hot) if max(energy_hot) != 0 else 0

# Plot results
sns.set(style="darkgrid")
plt.figure(figsize=(8, 5))
plt.plot(t_list, energy_hot, label="Hot Expansion Energy", color="red")
plt.plot(t_list, energy_cold, label="Cold Compression Energy", color="blue")
plt.xlabel("Time")
plt.ylabel("Energy")
plt.title(f"Quantum Heat Engine Simulation\nEfficiency: {efficiency:.2f}")
plt.legend()
plt.show()

# Print results
print(f"\nWork Done by Quantum Heat Engine: {work_done:.2f}")
print(f"Efficiency of Quantum Heat Engine: {efficiency:.2f}")
