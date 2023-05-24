import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os
import pandas as pd

#TODO: Here you need to specify where the repository you downloaded from the cluster is located
repo = '20230523_lk001_Linux/CONFIG_vascular_growth_example.py_092842'

csv_file = ''
for filename in os.listdir(repo):
    # Check if the file is a csv file
    if filename.endswith('.csv'):
        csv_file = filename

param_space = pd.read_csv(f'{repo}/{csv_file}', sep=' ', header=0)
print(param_space)

print(param_space.columns)
#TODO: maybe change parameter the user wants to plot (what column in the csv file)
parameter = param_space.columns[1]

param = np.array(param_space[parameter])
number_of_iterations = len(param_space['Iteration'])

#TODO: change paths to match the simulation outputs (you should only need to change the DataOutput part)
paths = [f'{repo}/iter{i}/DataOutput/' for i in range(0, number_of_iterations)]


###################################################################################################################
###################################################################################################################
###################################################################################################################
#TODO: this is only an example of how to plot the data, you can change this to plot whatever you want with your own simulation outputs
tmin = 0  # Minimum time
tmax = 1000  # Maximum time
show_fits = False  # Show the exponential fits
show_necro = False
show_quiet_cycling = False
local = False
param_to_plot = []


if local: paths = ['DataOutput/']


number_cells_list = []
necrotic_cells_list = []
cycling_cells_list = []
quiescent_cells_list = []
tumor_size_list = []
tumor_size_free_list = []
times_list = []

for path in paths:
    number_cells = np.load(f'{path}number_tumor_cells.npy', allow_pickle=True)
    necrotic_cells = np.load(f'{path}number_necrotic_cells.npy', allow_pickle=True)
    cycling_cells = np.load(f'{path}number_cycling_cells.npy', allow_pickle=True)
    quiescent_cells = np.load(f'{path}number_quiescent_cells.npy', allow_pickle=True)
    tumor_size = np.load(f'{path}tumor_size.npy', allow_pickle=True)
    tumor_size_free = np.load(f'{path}tumor_size_free.npy', allow_pickle=True)
    times = np.load(f'{path}times.npy', allow_pickle=True)

    # Find the indices of the times that are within the time range
    idx = np.where((times >= tmin) & (times<=tmax))
    # Filter the arrays to only include the data between tmin and tmax
    number_cells = number_cells[idx]
    tumor_size = tumor_size[idx]
    tumor_size_free = tumor_size_free[idx]
    necrotic_cells = necrotic_cells[idx]
    cycling_cells = cycling_cells[idx]
    quiescent_cells = quiescent_cells[idx]
    times = times[idx]

    # Append the filtered arrays to the lists
    number_cells_list.append(number_cells)
    tumor_size_list.append(tumor_size)
    tumor_size_free_list.append(tumor_size_free)
    necrotic_cells_list.append(necrotic_cells)
    cycling_cells_list.append(cycling_cells)
    quiescent_cells_list.append(quiescent_cells)
    times_list.append(times)


# Fit the data to an exponential curve for each simulation and get the doubling time
doubling_times_number_cells = []
doubling_times_tumor_size = []
dpi = 300
fig, axes = plt.subplots(2, 1, figsize=(8, 10), dpi=dpi)



for i in range(len(paths)):
    print(param[i])
    if len(param_to_plot) > 0:
        if param[i] not in param_to_plot:
            continue
    print(paths[i])
    # Fit number of cells
    if show_fits:
        popt, pcov = curve_fit(func, times_list[i], number_cells_list[i], p0=(3000, 3e-3, 0), maxfev=100000)
        print(popt)
    color = axes[0].plot(times_list[i], number_cells_list[i], '.', markersize=3, alpha=0.8, label=parameter+': '+str(param[i]))[0].get_color()
    if show_necro: axes[0].plot(times_list[i], necrotic_cells_list[i], 's', markersize=5, alpha=0.5, color=color)
    if show_quiet_cycling:
        axes[0].plot(times_list[i], cycling_cells_list[i], '+', markersize=3, alpha=0.5, color=color)
        axes[0].plot(times_list[i], quiescent_cells_list[i], 'D', markersize=3, alpha=0.5, color=color)
    if show_fits:
        axes[0].plot(times_list[i], func(times_list[i], *popt), '-', color=color, label='fit '+parameter+': '+str(param[i]))
        doubling_time = np.log(2)/popt[1]
        print('Doubling time (Number of Cells):', doubling_time)
        doubling_times_number_cells.append(doubling_time)

    # Fit tumor size
    if show_fits:
        popt, pcov = curve_fit(func, times_list[i], tumor_size_list[i], p0=(1, 0.003, 0), maxfev=100000)
        print(popt)
    axes[1].plot(times_list[i], tumor_size_list[i], 'o', color = color, markersize = 5, alpha=0.5, label=parameter+': '+str(param[i]))
    axes[1].plot(times_list[i], tumor_size_free_list[i], '+', color = color, markersize = 5, alpha=0.5)
    if show_fits:
        axes[1].plot(times_list[i], func(times_list[i], *popt), '-', color=color, label='fit '+parameter+': '+str(param[i]))
        doubling_time = np.log(2)/popt[1]
        doubling_times_tumor_size.append(doubling_time)

axes[0].set_title('Number of Cells Evolution')
axes[0].set_xlabel('Time')
axes[0].set_ylabel('Number of Cells')
# axes[0].set_xlim(0, 250)
# axes[0].set_ylim(0, 2e5)
axes[0].grid(True)
axes[0].legend()

axes[1].set_title('Tumor Volume Evolution')
axes[1].set_xlabel('Time')
axes[1].set_ylabel('Tumor Volume [mm^3]')
# axes[1].set_xlim(0, 250)
# axes[1].set_ylim(0, 50)
axes[1].grid(True)
axes[1].legend()

#add a tiny text box in the corner with the repo name
plt.figtext(0.01, 0.01, repo, wrap=True, horizontalalignment='left', fontsize=6)
plt.tight_layout()
plt.savefig(repo+'/tumor_evolution_'+str(tmax)+'.png', dpi=dpi)
plt.show()

if show_fits:
    if len(param_to_plot) > 0:
        param = param_to_plot
    print('Doubling times (Number of Cells):', doubling_times_number_cells)
    print('Doubling times (Tumor Size):', doubling_times_tumor_size)

    print(param)
    print(doubling_times_number_cells)

    plt.plot(param, doubling_times_number_cells, 'bo', label='Cells doubling time')
    plt.xlabel(parameter)
    plt.ylabel('Doubling time [days]')
    plt.title('Doubling time vs. ' + parameter)
    # plt.yscale('log')  # set y-axis to logarithmic scale
    plt.legend()
    plt.grid(True)
    plt.savefig(repo+'/doubling_time.png', dpi=300)
    plt.show()

    plt.plot(param, doubling_times_tumor_size, 'ro', label='Tumor volume doubling time')
    plt.xlabel(parameter)
    plt.ylabel('Doubling time [days]')
    plt.title('Doubling time vs. ' + parameter)
    # plt.yscale('log')  # set y-axis to logarithmic scale
    plt.legend()
    plt.grid(True)
    plt.savefig(repo+'/doubling_time_tumor_size.png', dpi=300)
    plt.show()




