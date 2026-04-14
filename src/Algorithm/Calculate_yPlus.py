import sys  # Import system-specific parameters and functions
import os
import webbrowser
import logging
import json
import numpy as np

from pathlib import Path
from urllib.parse import quote_plus

sys.path.append(str(Path(__file__).resolve().parent.parent))   # Add the parent directory of 'src' to the Python path

#-----------------------------------------------------------------------
# Impot the class from the local python files
from GUI.Utils import utils
#-----------------------------------------------------------------------



#***********************************************************************
# Very important: you need to use usr_dir when you want to save data
# utils.resource_path only used for reading static files
#***********************************************************************


# Function to calculate y+
def calculate_yPlus(progress_callback=None):

    usr_dir = utils.get_usr_dir()
    progress_file = usr_dir / "progress.txt"

    #------------------------------------------------------------------
    def log_progress(msg):

        """Print and write to progress.txt"""

        # Print to console (it will be obtained by stdout of subprocess)
        print(msg, flush=True)

        # Send message to GUI log window
        if progress_callback: progress_callback(msg)

        # Write to progress.txt
        with open(progress_file, "w", encoding="utf-8") as f:
            f.write(msg + "\n")
    #------------------------------------------------------------------


    #------------------------------------------------------------------
    # Load the data from the file of usr/input_data.json
    # log_progress("Start to run 'Calculate_yPlus.py'.")

    # Load the input data from the file
    
    input_data_file = usr_dir / "input_data.json"
    with open(input_data_file, "r", encoding="utf-8") as f:
        input_data = json.load(f)
    
    # Get the input data from the dictionary
    # Initialize variables
    freestream_velocity = None     # Freestream velocity
    freestream_density = None      # Freestream density
    dynamic_viscosity = None       # Dynamic viscosity
    reference_length = None        # Reference length
    grid_stretch_ratio = None      # Grid stretch ratio
    desired_yPlus = None           # Desired y+
    spatial_discretization = None  # Spatial discretization scheme
    skin_friction_formula = None   # Skin friction formula
    boundary_layer_formula = None  # Boundary layer formula
    
    #-------------------------------------------------------------------
    # Loop through the dictionary and match partially
    log_progress(f'Input data:')
    for key, value in input_data.items():
        if "freestream_velocity" in key:
            freestream_velocity = float(value)
            log_progress(f'Freestream velocity: {freestream_velocity:.8f}')
        elif "freestream_density" in key:
            freestream_density = float(value)
            log_progress(f'Freestream density: {freestream_density:.8f}')
        elif "dynamic_viscosity" in key:
            dynamic_viscosity = float(value)
            log_progress(f'Dynamic viscosity: {dynamic_viscosity:.8E}')
        elif "reference_length" in key:
            reference_length = float(value)
            log_progress(f'Reference length: {reference_length:.8f}')
        elif "grid_stretch_ratio" in key:
            grid_stretch_ratio = float(value)
            log_progress(f'Grid stretch ratio: {grid_stretch_ratio:.8f}')
        elif "desired_yPlus" in key:
            desired_yPlus = float(value)
            log_progress(f'Desired y+: {desired_yPlus:.2f}')
        elif "spatial_discretization" in key:
            spatial_discretization = value
            log_progress(f'Spatial discretization scheme: {spatial_discretization}')
        elif "skin_friction_formula" in key:
            skin_friction_formula = value
            log_progress(f'Skin friction formula: {skin_friction_formula}')
        elif "boundary_layer_formula" in key:
            boundary_layer_formula = value
            log_progress(f'Boundary layer formula: {boundary_layer_formula}')


    # Check if values were found
    if freestream_velocity is None:
        raise ValueError("Freestream velocity not found in input data")
    if freestream_density is None:
        raise ValueError("Freestream density not found in input data")
    if dynamic_viscosity is None:
        raise ValueError("Dynamic viscosity not found in input data")
    if reference_length is None:
        raise ValueError("Reference length not found in input data")
    if desired_yPlus is None:
        raise ValueError("Desired y+ not found in input data")
    #-------------------------------------------------------------------

    #-------------------------------------------------------------------
    # Output result
    result_data = {}

    # Calculate Reynolds number
    kenematic_viscosity = dynamic_viscosity / freestream_density
    Reynolds_number = freestream_velocity * reference_length / kenematic_viscosity
    log_progress(f'Output data:')
    log_progress(f'Reynolds number: {Reynolds_number:.8E}')
    result_data["Reynolds number"] = Reynolds_number


    # Calculate the estimated skin friction
    if skin_friction_formula == "Prandtl-Schlichting (1979)":

        # Warning: Schlichting 1979 formula is recommended for Re >= 1e6
        skin_friction = (2.0 * np.log10(Reynolds_number) - 0.65)**(-2.3)

    elif skin_friction_formula == "ITTC-1957 (ship)":

        # Warning: ITTC-1957 formula is recommended for Re >= 1e6
        skin_friction = 0.075 / (np.log10(Reynolds_number) - 2)**2

    elif skin_friction_formula == "Prandtl-Kármán (1932)":

        # Warning: ITTC-1957 formula is recommended for 5e5 < Re < 1e7
        skin_friction = 0.026 / Reynolds_number**(1.0/7.0)

    log_progress(f'Estimated skin friction coefficient: {skin_friction:.8E}')
    result_data["Estimated skin friction coefficient"] = skin_friction
    #-------------------------------------------------------------------

    # Calculate the estimated boundary layer thickness
    if boundary_layer_formula == "Schlichting (1979)":

        boundary_layer_thickness = 0.37 * reference_length / Reynolds_number ** (1.0/5.0)

    elif boundary_layer_formula == "White (1991)":

        boundary_layer_thickness = 0.376 * reference_length / Reynolds_number ** (1.0/5.0)

    log_progress(f'Estimated boundary layer thickness: {boundary_layer_thickness:.8E}')
    result_data["Estimated boundary layer thickness"] = boundary_layer_thickness
    #-------------------------------------------------------------------

    #-------------------------------------------------------------------
    # Calculate the first-grid spacing
    if spatial_discretization == "Cell-centered" or spatial_discretization == "网格中心点":

        first_grid_spacing = 2 * desired_yPlus * reference_length / ( Reynolds_number * np.sqrt(0.5 * skin_friction) )
        
    elif spatial_discretization == "Vertex-centered" or spatial_discretization == "网格节点":

        first_grid_spacing = desired_yPlus * reference_length / ( Reynolds_number * np.sqrt(0.5 * skin_friction) )

    log_progress(f'First-grid spacing: {first_grid_spacing:.8E}')
    result_data["First-grid spacing"] = first_grid_spacing
    #-------------------------------------------------------------------



    #-------------------------------------------------------------------
    # Calculate the number of prism grids
    if grid_stretch_ratio is None:
        pass
    else:

        # N = ceil(ln(1 - δ/Δy * (1-r)) / ln(r))
        Number_of_prism_layers = np.ceil(np.log(1 - (boundary_layer_thickness / first_grid_spacing) * (1 - grid_stretch_ratio)) / np.log(grid_stretch_ratio))    

        Number_of_prism_layers = int(Number_of_prism_layers)

        # total_thickness = first_grid_spacing * (1 - grid_stretch_ratio**Number_of_prism_layers) / (1 - grid_stretch_ratio)

        log_progress(f'Number of prism layers: {Number_of_prism_layers:8d}')
        result_data["Number of prism layers"] = Number_of_prism_layers
    #-------------------------------------------------------------------

    #-------------------------------------------------------------------
    # Output results to the file
    usr_dir = utils.get_usr_dir()
    results_file = usr_dir / "results.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(result_data, f, indent=4)
        
    #-------------------------------------------------------------------


#-----------------------------------------------------------------------
# Main execution block
if __name__ == '__main__':  # Ensure this code runs only when the file is executed directly
    
    calculate_yPlus()
#-----------------------------------------------------------------------
