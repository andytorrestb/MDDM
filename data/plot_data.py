import matplotlib.pyplot as plt
import pandas as pd

# data = pd.read_csv('eq24_d1e-6_2.csv')
# print(data)

curves = ['C1', 'C2', 'C3']
for curve in curves:
    fname = 'eq24_d1e-6_'+ curve +'.csv'
    data = pd.read_csv(fname)
    plt.plot(data['x'], data[' y'], label = curve)

plt.legend()
plt.yscale('log')
plt.xscale('log')
plt.title('Ballistic Trajectory Model')
plt.ylabel('Vertical Distance from Surface [m]')
plt.xlabel('Horizontal Distance from Nozzle Center [m]')
plt.savefig('ballistic_verification.png')