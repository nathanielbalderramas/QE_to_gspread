import pandas as pd
from datetime import datetime
import re
from aux_functions import get_cell_offset

"""
Aquí se maneja la spreadsheet de google

update_raw() sube todo el dataframe a la hoja RAW

update_dash() sube los pivots que uno quiera en la posición que uno quiera de la hoja que uno quiera.
Los pivots los generamos con las funciones que importamos de pivot_functions

"""
def update_raw(df, spread):
    """
    Sube todo el dataframe a la hoja RAW del spreadsheet
    """
    spread.df_to_sheet(df, index=False, sheet='RAW', start='A2', replace=False)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    spread.update_cells('A1', 'B1', ['Last updated:', now])
    print("RAW updated succesfully at:", now)

def update_pivots(df, spread, pivots):
    """
    Recibe una lista de listas con la forma:
    [
     [pivot_function, pivot_title, starting_cell, sheet],
    ]
    
    pivot_function: define el contenido de la tabla, importar de pivot_functions
    pivot_title: titulo de la tabla
    starting_cell: coordenada de la celda superior izquierda de la tabla
    sheet: nombre de la hoja dentro del spreadsheet donde subir
    """

    for pivot_fun, pivot_title, starting_cell , sheet in pivots:
        pivot = pivot_fun(df)

        pivot_cell = get_cell_offset(starting_cell, row_offset=1)
        pivot_width = pivot.shape[1]
        end_cell = get_cell_offset(starting_cell, col_offset=pivot_width-1)

        print(starting_cell, end_cell, pivot_cell)
        print(pivot)

        spread.df_to_sheet(pivot, index=False, sheet=sheet, start=pivot_cell)
        spread.update_cells(starting_cell, end_cell, [pivot_title]*pivot_width, sheet=sheet)
        spread.merge_cells(start=starting_cell, end=end_cell, sheet=sheet)
