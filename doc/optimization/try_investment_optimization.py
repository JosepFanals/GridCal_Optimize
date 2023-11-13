import os
import sys
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

# Load grid data from file
grid = FileOpen('Grids_and_profiles/grids/IEEE118_rate_load15.xlsx').open()

# Define investment power lines in the grid
line1 = dev.Line(grid.get_buses()[23], grid.get_buses()[71], ' Line_inv_1', r=0.0488, x=0.196, b=0.0488, rate=4.3, cost=2)
line2 = dev.Line(grid.get_buses()[23], grid.get_buses()[69], ' Line_inv_2', r=0.00221, x=0.4115, b=0.10198, rate=9.4, cost=2)
line3 = dev.Line(grid.get_buses()[71], grid.get_buses()[70], ' Line_inv_3', r=0.0446, x=0.18, b=0.04444, rate=13, cost=2)

# Add lines to the grid
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
grid.add_investments_group(Ig3)

# Configure power flow options
pf_options = sim.PowerFlowOptions()

# Specify the investment evaluation method
mvrsm = InvestmentEvaluationMethod.MVRSM

# Run the investment evaluation simulation
inv = sim.InvestmentsEvaluationDriver(grid, method=mvrsm, max_eval=15, pf_options=pf_options)
inv.run()

# Retrieve and display investment evaluation results
inv_results = inv.results
results_tpe_report = sim.result_types.ResultTypes.InvestmentsReportResults
results_tpe_plot = sim.result_types.ResultTypes.InvestmentsParetoPlot

# Print investment evaluation report
print(inv_results.mdl(results_tpe_report).to_df())

# Generate and display Pareto plot
results_plot = inv_results.mdl(results_tpe_plot)
results_plot.plot(selected_col_idx=[0, 1], selected_rows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
