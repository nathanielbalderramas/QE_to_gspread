"""
Acá viven las funciones que se encargan de extraer las métricas para armar la base de datos.
Todas tienen que tener la signatura

def nombre(in_file, out_file): #incluso aunque no utilizen alguno de los dos.
    #MAGIC CODE GOES HERE
    return VALUE

Este es el código que hace el heavylifting, hay que definir bien estas funciones para que la información que se extraiga pueda efectivamente ser útil.
"""

import re

def get_calculation_type(in_file, out_file):
    """Extracts the calculation type from a Quantum Espresso .in file."""
    with open(in_file, "r") as f:
        for line in f:
            match = re.search(r"calculation\s*=\s*['\"]?(\w+)['\"]?", line)
            if match:
                return match.group(1)
    return None


def get_convergence(in_file, out_file):
    """Checks if the QE calculation ended gracefully according to its type."""
    calc_type = get_calculation_type(in_file, out_file)
    scf_converged = False
    bfgs_finished = False
    job_done = False
    with open(out_file, "r") as f:
        for line in f:
            if "convergence has been achieved" in line:
                scf_converged = True
            if "End of BFGS Geometry Optimization" in line:
                bfgs_finished = True
            if "JOB DONE" in line:
                job_done = True
    if calc_type == "scf":
        return job_done and scf_converged
    elif calc_type in ["relax", "vc-relax"]:
        return job_done and scf_converged and bfgs_finished
    else:
        return job_done
    
def get_final_energy(in_file, out_file):
    """Extracts the final energy from a Quantum Espresso .out file."""
    energy_regex = re.compile(r"!\s+total energy\s+=\s+([-+]?\d*\.\d+|\d+)\s+Ry")
    energy = None
    with open(out_file, "r") as f:
        for line in f:
            match = energy_regex.search(line)
            if match:
                energy = float(match.group(1))
    return energy

def get_total_magnetization(in_file, out_file):
    return None

def get_absolute_magnetization(in_file, out_file):
    return None

