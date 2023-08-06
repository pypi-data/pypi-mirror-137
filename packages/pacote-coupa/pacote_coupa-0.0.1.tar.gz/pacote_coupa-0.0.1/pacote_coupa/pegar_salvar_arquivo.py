#------------------------------------------------------------------------------------------------------
# imports
import PySimpleGUI as gui

#------------------------------------------------------------------------------------------------------
gui.theme('dark grey 9')

#------------------------------------------------------------------------------------------------------
# Funções
def pegar_arquivo():
    pegando_arquivo: str = gui.popup_get_file(
        "Pegando Arquivo",
        default_path = "",
        save_as=False,
        no_window=True,
    )
    
    return pegando_arquivo

#------------------------------------------------------------------------------------------------------
def salvar_arquivo_csv():
    salvarCSV: str = gui.popup_get_file(
        "Salvar Como",
        save_as=True,
        no_window=True,
        default_extension=".csv",
        file_types=(("CSV", ".csv"),),
    )
    
    return salvarCSV

#------------------------------------------------------------------------------------------------------