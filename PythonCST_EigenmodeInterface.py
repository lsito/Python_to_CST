# Tell where to find cst library
import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2023\AMD64\python_cst_libraries")

import cst
import cst.interface
import cst.results

# High level operations with files
import shutil

#%%
# Local path to CST project file
cst_project_folder = r"C:\Users\lsito\Desktop\CurrentSimul\Eigenmode_TestPython"
cst_filename = '\V5.3_Operational_Eigenmode'

cst_project_path = cst_project_folder + cst_filename + '.cst'
cst_result_folder = cst_project_folder + '\Results'

# Open CST as software
mycst = cst.interface.DesignEnvironment()

# Open CST Project
mycst1 = cst.interface.DesignEnvironment.open_project(mycst, cst_project_path) 
mycst1.modeler()

#%% Setting up and solving

start_freq = 0.1 # GHz

# Start Solver - most commands are VBA lines 
setup = '''Sub Main() \n
            EigenmodeSolver.SetNumberOfModes (1) \n
            EigenmodeSolver.SetFrequencyTarget (True, 0.1)
            End Sub'''

mycst1.schematic.execute_vba_code(setup, timeout=None)

mycst1.modeler.run_solver()
mycst1.save()

#%% Accessing the result

# I need a ProjectFile object (where I set where to take the results from)
# I need a ResultModule object (that I get with the method get_3d)
# I need a ResultItem object which has the method get_data() to have my df

project = cst.results.ProjectFile(cst_project_path, allow_interactive=True)

# Just to see what strings to use to access values
project.get_3d().get_tree_items()

f_obj = project.get_3d().get_result_item('Tables\\1D Results\\Frequency (Multiple Modes)')
f_data = f_obj.get_data()[0][1]

