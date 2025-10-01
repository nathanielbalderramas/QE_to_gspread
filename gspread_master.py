import pandas as pd
from gspread_pandas import Spread, Client

from report_master import generate_reports
from gspread_handler import update_raw, update_pivots

from pivot_functions import (CAT_final_energy, 
                             N2_adsorption_energy, 
                             N2_disociative_adsorption_energy, 
                             N2_surface_disociation_energy, 
                             CAT_status, 
                             N2_status, 
                             twoN_status,
)


if __name__ == "__main__":
    # Opcion 1: Se genera el dataframe con las métricas que uno desee
    base_dir = "/home/nmorgan/doc/eusync/doc/MNGph-spinON/"
    elements = ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"]
    structures = ["M2b", "MN", "MN2", "MN3", "MN4", "M2N4", "M2N5", "M2N5b", "M2N6"]
    stages = ["CAT", "N2", "2N"]
    metrics = [ # importante, para actualizar las métricas disponibles hay que editar report_master
        "calculation_type",
        "convergence",
        "final_energy"
    ]
    df = generate_reports(base_dir=base_dir, elements=elements, structures=structures, stages=stages, metrics=metrics)

    # Opción 2: Cargarlo desde el disco
    df = pd.read_csv("./thesis_scripts/csv/report.csv")
    elements = ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"]
    structures = ["M2b", "MN", "MN2", "MN3", "MN4", "M2N4", "M2N5", "M2N5b", "M2N6"]
    df["Element"] = pd.Categorical(df["Element"], categories=elements, ordered=True)
    df["Structure"] = pd.Categorical(df["Structure"], categories=structures, ordered=True)


    # Abrimos la spreadsheet de google 
    # ver: https://docs.gspread.org/en/v6.1.4/oauth2.html    
    # &    https://gspread-pandas.readthedocs.io/en/latest/configuration.html#
    spread = Spread('My_first_auto_spreadsheet')


    # Subimos lo que querramos
    update_raw(df, spread)
    #dash_pivots =[[CAT_final_energy, "Final Energy [CAT] (eV)", "A5", "DASH"],
    #             [N2_adsorption_energy, "N2 Eads (eV)", "A20", "DASH"],
    #             [N2_disociative_adsorption_energy, "N2 Eads+dis (eV)", "A35", "DASH"],
    #             [N2_surface_disociation_energy, "N2 Esurfdis", "A50", "DASH"],
    #            ]
    #update_pivots(df, spread, dash_pivots)

    stat_pivots =[[CAT_status, "CAT status", "A5", "STATUS"],
                 [N2_status, "N2 status", "A20", "STATUS"],
                 [twoN_status, "2N status", "A35", "STATUS"],
                ]
    update_pivots(df, spread, stat_pivots)

