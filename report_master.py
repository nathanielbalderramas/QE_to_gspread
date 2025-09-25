"""
Aquí se define la estructura del dataframe.
Se define un patron de búsqueda de archivos y un set de funciones de análisis (importadas de report_functions)
Se aplica cada función a cada archivo encontrado y se lo agrega como una fila del dataframe
"""

import os
import pandas as pd
from report_functions import (get_calculation_type,
                              get_convergence,
                              get_final_energy,
                              get_total_magnetization,
                              get_absolute_magnetization)

# Example metric functions

# Dispatch dictionary
# Estas son las funciones que extraen métricas, importar de report_functions
function_dict = {
    "final_energy": get_final_energy,
    "calculation_type": get_calculation_type,
    "convergence": get_convergence,
}

# Esta es la función que recorre los directorios y genera el dataframe
# En mi caso las carpetas tienen la forma:
# main/element/sac/stage/sac.in   - i.e. - main/Co/CoN4/N2/CoN4.in
def generate_reports(base_dir, elements, structures, stages, metrics):
    results = []

    for element in elements:
        for structure in structures:
            sac = structure.replace("M", element)
            struct_dir = os.path.join(base_dir, element, sac)

            for stage in stages:
                in_file  = os.path.join(struct_dir, stage, f"{sac}.in")
                out_file = os.path.join(struct_dir, stage, f"{sac}.out")

                row = {"Element": element, "Structure": structure, "SAC": sac, "Stage": stage}

                # de acá para abajo es genérico/extensible
                if os.path.isfile(in_file) and os.path.isfile(out_file):
                    for metric in metrics:
                        func = function_dict.get(metric)
                        if func:
                            try:
                                row[metric] = func(in_file, out_file)
                            except Exception as e:
                                row[metric] = f"Error: {e}"
                        else:
                            row[metric] = "Unknown metric"
                else:
                    row.update({metric: "Files missing" for metric in metrics})

                results.append(row)

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Convert the columns to ordered categorical (for later convenience when pivoting)
    df["Element"] = pd.Categorical(df["Element"], categories=elements, ordered=True)
    df["Structure"] = pd.Categorical(df["Structure"], categories=structures, ordered=True)

    # Save single CSV
    df.to_csv("./thesis_scripts/csv/report.csv", index=False)
    # También se podría guardar como pickle (archivo binario), más conveniente para python, menos conveniente para humanos

    print("Report generated successfully.")
    return df