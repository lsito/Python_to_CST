# Tell where to find cst library
import sys
sys.path.append(r"C:\Program Files (x86)\CST Studio Suite 2023\AMD64\python_cst_libraries")

import cst
import cst.interface
import cst.results

# High level operations with files
import shutil

# Local path to CST project file
cst_project_folder = r"C:\Users\lsito\Desktop\CurrentSimul\Eigenmode_TestPython"
cst_filename = '\V5.3_Operational_Eigenmode'

cst_project_path = cst_project_folder + cst_filename + '.cst'
cst_result_folder = cst_project_folder + '\Results'

f = [0]
Q = [0]
RoverQ = [0]

# Open CST as software
mycst = cst.interface.DesignEnvironment()

# Open CST Project
mycst1 = cst.interface.DesignEnvironment.open_project(mycst, cst_project_path) 
# mycst1.modeler()

while(f[-1]<2):
    
    test_freq = 0.1 # GHz

    # Start Solver - most commands are VBA lines 
    setup = f'''Sub Main() \n 
                EigenmodeSolver.SetNumberOfModes (1) \n 
                EigenmodeSolver.SetFrequencyTarget (True, {f[-1]+test_freq}) \n 
                End Sub'''
    
    mycst1.schematic.execute_vba_code(setup, timeout=None)
    
    mycst1.modeler.run_solver()
    mycst1.save()

    project = cst.results.ProjectFile(cst_project_path, allow_interactive=True)

    f_obj = project.get_3d().get_result_item('Tables\\1D Results\\Frequency (Multiple Modes)')
    f_data = f_obj.get_data()[0][1]
    
    Q_obj = project.get_3d().get_result_item('Tables\\1D Results\\Q-Factor (lossy E) (Multiple Modes)')
    Q_data = Q_obj.get_data()[0][1]
    
    RoverQ_obj = project.get_3d().get_result_item('Tables\\1D Results\\R over Q beta=1 (Multiple Modes)')
    RoverQ_data = RoverQ_obj.get_data()[0][1]
    
    f.append(f_data)
    Q.append(Q_data)
    RoverQ.append(RoverQ_data)
    
    