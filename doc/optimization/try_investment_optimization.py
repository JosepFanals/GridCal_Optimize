import os
import sys
import time
import pandas as pd
import matplotlib.pyplot as plt

# Determine the path to the 'GridCal_Optimize' directory, necessary to import GridCal
current_script_dir = os.path.dirname(os.path.abspath(__file__))
gridcal_optimize_dir = os.path.abspath(os.path.join(current_script_dir, '../../'))
src_path = os.path.join(gridcal_optimize_dir, 'src')

# Add the 'src' directory to sys.path
sys.path.append(src_path)

# Import necessary modules and classes
from GridCalEngine import *
from GridCalEngine.IO.file_handler import FileOpen
import GridCalEngine.Core.Devices as dev
import GridCalEngine.Simulations as sim
from GridCalEngine.basic_structures import InvestmentEvaluationMethod


# Define investment power lines in the grid
def add_investments_to_grid(grid):
    line1 = dev.Line(grid.get_buses()[23], grid.get_buses()[71], 'Line_inv_1', r=0.0488, x=0.196, b=0.0488, rate=4.3,
                     cost=2)
    line2 = dev.Line(grid.get_buses()[23], grid.get_buses()[69], 'Line_inv_2', r=0.00221, x=0.4115, b=0.10198, rate=9.4,
                     cost=2)
    line3 = dev.Line(grid.get_buses()[71], grid.get_buses()[70], 'Line_inv_3', r=0.0446, x=0.18, b=0.04444, rate=13,
                     cost=2)
    line4_1 = dev.Line(grid.get_buses()[71], grid.get_buses()[69], 'Line_inv_41', r=0.02, x=0.2, b=0.08, rate=10,
                       cost=2)
    line5_1 = dev.Line(grid.get_buses()[23], grid.get_buses()[66], 'Line_inv_51', r=0.02, x=0.2, b=0.02, rate=10,
                       cost=2)
    line6_1 = dev.Line(grid.get_buses()[71], grid.get_buses()[22], 'Line_inv_61', r=0.02, x=0.2, b=0.02, rate=10,
                       cost=2)
    line4_2 = dev.Line(grid.get_buses()[71], grid.get_buses()[69], 'Line_inv_42', r=0.02, x=0.2, b=0.08, rate=10,
                       cost=2)
    line5_2 = dev.Line(grid.get_buses()[23], grid.get_buses()[66], 'Line_inv_52', r=0.02, x=0.2, b=0.02, rate=10,
                       cost=2)
    line6_2 = dev.Line(grid.get_buses()[71], grid.get_buses()[22], 'Line_inv_62', r=0.02, x=0.2, b=0.02, rate=10,
                       cost=2)

    lines_list = [line1, line2, line3, line4_1, line5_1, line6_1, line4_2, line5_2, line6_2]

    # Add each line as an investment & Investment group
    for i, line in enumerate(lines_list):
        grid.add_line(line)
        inv_group = dev.InvestmentsGroup(name='Ig' + str(i))
        investment = dev.Investment(device_idtag=line.idtag, name='Investment' + str(i), CAPEX=i%3+1, group=inv_group)
        grid.add_investment(investment)
        grid.add_investments_group(inv_group)

    return grid

def obtain_multiple_optimal_points(grid, pf_options, method, number_it):
    ### Store data of different optimal points
    # Initialize empty lists to store data
    of_values = []
    capex_values = []
    combinations = []

    # Run the investment evaluation simulation
    start_time = time.time()
    for _ in range(number_it):
        inv = sim.InvestmentsEvaluationDriver(grid, method=method, max_eval=100, pf_options=pf_options)
        inv.run()
        of_value = inv.optim_fobj
        capex_value = inv.optim_CAPEX
        combination = inv.active_investments

        # Append values to lists
        of_values.append(of_value)
        capex_values.append(capex_value)
        combinations.append(combination)

    # Create DataFrame from lists
    df_total = pd.DataFrame({'Objective function': of_values, 'CAPEX (M€)': capex_values, 'Combinations': combinations})

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Elapsed time: {elapsed_time} seconds. {number_it} iterations")

    # Retrieve and display last investment evaluation results
    inv_results = inv.results
    results_tpe_report = sim.result_types.ResultTypes.InvestmentsReportResults
    results_tpe_plot = sim.result_types.ResultTypes.InvestmentsParetoPlot

    # Print investment evaluation report
    df_last = inv_results.mdl(results_tpe_report).to_df()

    return df_total, df_last


def plot_scatter_plot(df_results, title):
    # Generate and display Pareto plot
    x_values = df_results['CAPEX (M€)']
    y_values = df_results['Objective function']

    # Scatter plot
    plt.scatter(x_values, y_values, marker='o', alpha=0.5)

    # Set axis labels and title
    plt.xlabel('CAPEX (M€)')
    plt.ylabel('Objective function')
    plt.title(title)

if __name__ == "__main__":
    grid = FileOpen('Grids_and_profiles/grids/IEEE118_rate_load15.xlsx').open()

    grid = add_investments_to_grid(grid)

    pf_options = sim.PowerFlowOptions()
    mvrsm = InvestmentEvaluationMethod.MVRSM
    iterations = 50

    df_total, df_last_inv = obtain_multiple_optimal_points(grid=grid, pf_options=pf_options, method=mvrsm, number_it=iterations)

    plt.figure(1)
    plot_scatter_plot(df_last_inv,'Dispersion Plot: Objective function vs CAPEX for 1 MVRSM optimization process')

    plt.figure(2)
    plot_scatter_plot(df_total, 'Dispersion Plot: Objective function vs CAPEX for optimal points')

    print('Plots are here!!')
    plt.show()


'''
# Try random lines redundancies

i = 0
for line in grid.lines:
    i += 1
    if i % 3 == 0:
        line_copy = line.copy()
        line_copy.idtag = 'cc' + str(i)
        grid.add_line(line_copy)
        Ig = dev.InvestmentsGroup(name='Ig'+str(i))
        grid.add_investments_group(Ig)
        I = dev.Investment(device_idtag=line_copy.idtag, name='Investment1', CAPEX=2, group=Ig)
        grid.add_investment(I)

print('Done')'''

'''# Add lines to the grid
grid.add_line(line1)
grid.add_line(line2)
grid.add_line(line3)

# Create investment groups
Ig1 = dev.InvestmentsGroup(name='Ig1')
Ig2 = dev.InvestmentsGroup(name='Ig2')
Ig3 = dev.InvestmentsGroup(name='Ig3')

# Define each line as an investment
I1 = dev.Investment(device_idtag=line1.idtag, name='Investment1', CAPEX=2, group=Ig1)
I2 = dev.Investment(device_idtag=line2.idtag, name='Investment2', CAPEX=2, group=Ig2)
I3 = dev.Investment(device_idtag=line3.idtag, name='Investment3', CAPEX=2, group=Ig3)

# Add investments to the grid
grid.add_investment(I1)
grid.add_investment(I2)
grid.add_investment(I3)

# Add investment groups to the grid
grid.add_investments_group(Ig1)
grid.add_investments_group(Ig2)
grid.add_investments_group(Ig3)'''
