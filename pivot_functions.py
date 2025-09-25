"""
Acá viven las funciones que generan las "pivot tables" de interés

La estructura de estas funciones es

def nombre(df):
    filtered = df[(df["NOMBRECOLUMNA"] == "VALORAFILTRAR")]
    pivot = filtered.pivot_table(   index="NOMBRECOLUMNA_FILAS", 
                                    columns="NOMBRECOLUMNA_COLUMNAS", 
                                    values="NOMBRECOLUMNA_VALORES", 
                                    aggfunc="first")

    # si requiere operaciones matemáticas:
    pivot = pivot.apply(pd.to_numeric, errors='coerce')
    pivot = MATEMATICAS HIJO
    
    pivot = pivot.reset_index()
    return pivot
"""


import pandas as pd

Ry2eV = 13.6057039763
E_N2       =	-40.2799584800  # E in Ry
E_H2       =	-2.3302500600   # E in Ry
E_NH3      =	-23.7123639500  # E in Ry
E_N2H2     =	-42.3963318814  # E in Ry
E_N2H4     =	-44.8165742783  # E in Ry
E_G_V0_N0  =	-689.6101981800 # E in Ry
E_G_V0_N1  =	-698.1885700100 # E in Ry
E_G_V1_N0  =	-677.5548651500 # E in Ry
E_G_V1_N1  =	-686.3611719500 # E in Ry
E_G_V1_N2  =	-695.0470631300 # E in Ry
E_G_V1_N3  =	-703.7963414900 # E in Ry
E_G_V2_N4  =	-700.9337578200 # E in Ry
E_Cr       =	-175.2022842300 # E in Ry
E_Fe       =	-249.9805479500 # E in Ry
E_Ni       =	-342.9229682100 # E in Ry
E_Sc       =	-94.0084303100  # E in Ry
E_Co       =	-298.1031528400 # E in Ry
E_Cu       =	-403.5247926700 # E in Ry
E_Mn       =	-210.9284318900 # E in Ry
E_Ti       =	-118.8359320700 # E in Ry
E_V        =	-144.6837845800 # E in Ry
E_Zn       =	-461.4729529300 # E in Ry


elements = ["Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"]
structures = ["M2b", "MN", "MN2", "MN3", "MN4", "M2N4", "M2N5", "M2N5b", "M2N6"]

def CAT_status(df):
    filtered = df[(df["Stage"] == "CAT")]
    pivot = filtered.pivot_table(index="Element", columns="Structure", values="convergence", aggfunc="first")
    pivot = pivot.reset_index()
    return pivot

def N2_status(df):
    filtered = df[(df["Stage"] == "N2")]
    pivot = filtered.pivot_table(index="Element", columns="Structure", values="convergence", aggfunc="first")
    pivot = pivot.reset_index()
    return pivot

def twoN_status(df):
    filtered = df[(df["Stage"] == "2N")]
    pivot = filtered.pivot_table(index="Element", columns="Structure", values="convergence", aggfunc="first")
    pivot = pivot.reset_index()
    return pivot

def CAT_final_energy(df):
    # --- FILTER rows you actually want ---
    # For adsorption energy table, maybe you only care about Stage == "N2" and calculation_type == "vc"
    filtered = df[(df["convergence"] == "TRUE") & (df["Stage"] == "CAT")]

    # --- Pivot into wide form ---
    pivot = (
        filtered.pivot_table(
            index="Element",      # metals go into rows
            columns="Structure",  # structure family goes into columns
            values="final_energy",
            aggfunc="first"       # or min/mean/max depending on your logic
        )  # Element stays as a proper column
            )
    pivot = pivot.apply(pd.to_numeric, errors='coerce')
    pivot = pivot * Ry2eV
    return pivot.reset_index()

def N2_adsorption_energy(df):
    # --- FILTER rows you actually want ---
    # For adsorption energy table, maybe you only care about Stage == "N2" and calculation_type == "vc"
    filtered_CAT = df[(df["Stage"] == "CAT")]
    filtered_N2  = df[(df["Stage"] == "N2")]

    # --- Pivot into wide form ---
    pivot_CAT = (
        filtered_CAT.pivot_table(
            index="Element",      # metals go into rows
            columns="Structure",  # structure family goes into columns
            values="final_energy",
            aggfunc="first"       # or min/mean/max depending on your logic
        )
            )
    
    # --- Pivot into wide form ---
    pivot_N2 = (
        filtered_N2.pivot_table(
            index="Element",      # metals go into rows
            columns="Structure",  # structure family goes into columns
            values="final_energy",
            aggfunc="first"       # or min/mean/max depending on your logic
        )
            )
    
    pivot_CAT = pivot_CAT.apply(pd.to_numeric, errors='coerce')
    pivot_N2 = pivot_N2.apply(pd.to_numeric, errors='coerce')
    pivot = ( pivot_N2 - (pivot_CAT + E_N2) ) * Ry2eV    
    return pivot.reset_index()

def N2_surface_disociation_energy(df):
    # --- FILTER rows you actually want ---
    # For adsorption energy table, maybe you only care about Stage == "N2" and calculation_type == "vc"
    filtered_N2 = df[(df["Stage"] == "N2")]
    filtered_2N = df[(df["Stage"] == "2N")]

    # --- Pivot into wide form ---
    pivot_N2 = (
        filtered_N2.pivot_table(
            index="Element",      # metals go into rows
            columns="Structure",  # structure family goes into columns
            values="final_energy",
            aggfunc="first"       # or min/mean/max depending on your logic
        )
            )
    
    # --- Pivot into wide form ---
    pivot_2N = (
        filtered_2N.pivot_table(
            index="Element",      # metals go into rows
            columns="Structure",  # structure family goes into columns
            values="final_energy",
            aggfunc="first"       # or min/mean/max depending on your logic
        )
            )
    
    pivot_N2 = pivot_N2.apply(pd.to_numeric, errors='coerce')
    pivot_2N = pivot_2N.apply(pd.to_numeric, errors='coerce')
    pivot = ( pivot_2N - (pivot_N2) ) * Ry2eV    
    return pivot.reset_index()   

def N2_disociative_adsorption_energy(df):
    # --- FILTER rows you actually want ---
    # For adsorption energy table, maybe you only care about Stage == "N2" and calculation_type == "vc"
    filtered_CAT = df[(df["Stage"] == "CAT")]
    filtered_2N  = df[(df["Stage"] == "2N")]

    # --- Pivot into wide form ---
    pivot_CAT = (
        filtered_CAT.pivot_table(
            index="Element",      # metals go into rows
            columns="Structure",  # structure family goes into columns
            values="final_energy",
            aggfunc="first"       # or min/mean/max depending on your logic
        )
            )
    
    # --- Pivot into wide form ---
    pivot_2N = (
        filtered_2N.pivot_table(
            index="Element",      # metals go into rows
            columns="Structure",  # structure family goes into columns
            values="final_energy",
            aggfunc="first"       # or min/mean/max depending on your logic
        )
            )
    
    pivot_CAT = pivot_CAT.apply(pd.to_numeric, errors='coerce')
    pivot_2N = pivot_2N.apply(pd.to_numeric, errors='coerce')
    pivot = ( pivot_2N - (pivot_CAT + E_N2) ) * Ry2eV    
    return pivot.reset_index()
