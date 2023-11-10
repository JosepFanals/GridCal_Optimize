import GridCalEngine.basic_structures
from GridCalEngine import *
from GridCalEngine.IO.file_handler import FileOpen
import GridCalEngine.Core.Devices as dev
import GridCalEngine.Simulations as sim
import numpy as np

grid = FileOpen('Grids_and_profiles/grids/IEEE118_rate_load15.xlsx').open()

line1 = dev.Line(grid.get_buses()[23],grid.get_buses()[71], ' Line_inv_1', r=0.0488, x=0.196, b=0.0488, rate=4.3)
line2 = dev.Line(grid.get_buses()[23],grid.get_buses()[69], ' Line_inv_1', r=0.00221, x=0.4115, b=0.10198, rate=9.4)
line3 = dev.Line(grid.get_buses()[71],grid.get_buses()[70], ' Line_inv_1', r=0.0446, x=0.18, b=0.04444, rate=13)

grid.add_line(line1)
grid.add_line(line2)
grid.add_line(line3)

I1 = dev.Investment(device_idtag=line1.idtag, name='Investment1', CAPEX=2)
I2 = dev.Investment(device_idtag=line2.idtag, name='Investment2', CAPEX=2)
I3 = dev.Investment(device_idtag=line3.idtag, name='Investment3', CAPEX=2)

grid.add_investment(I1)
grid.add_investment(I2)
grid.add_investment(I3)

pf_options = sim.PowerFlowOptions()
mvrsm = GridCalEngine.basic_structures.InvestmentEvaluationMethod.MVRSM
inv = sim.InvestmentsEvaluationDriver(grid, method=mvrsm, max_eval=15, pf_options=pf_options)
inv_results = sim.InvestmentsEvaluationResults(np.array([I1, I2, I3]), max_eval=15)

print(inv_results)