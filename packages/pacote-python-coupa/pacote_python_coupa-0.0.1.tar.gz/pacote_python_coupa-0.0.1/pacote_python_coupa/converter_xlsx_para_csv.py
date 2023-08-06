#------------------------------------------------------------------------------------------------------
# imports
from turtle import color
import pandas as pd, csv, pegar_salvar_arquivo as sv, PySimpleGUI as gui

#------------------------------------------------------------------------------------------------------
gui.theme('dark grey 9')

#------------------------------------------------------------------------------------------------------
# Funções
def converter_xlsx_para_csv(arquivo_xlsx: str, campos_especificos: list):
    
    data_xls = pd.read_excel(arquivo_xlsx, usecols = campos_especificos)
    data_xls = data_xls.replace('"', '', regex=True).replace("'", "", regex=True).replace("\n", " ", regex=True).replace('\s+', ' ', regex=True)
    
    try:
        salvar = sv.salvar_arquivo_csv()
        data_xls.to_csv(salvar, header=True, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL, quotechar='"', line_terminator='')
        
        gui.popup(
                    'Conversão completa',
                    font = ('Arial', 40),
                    no_titlebar = True,
                    button_type = 5,
                    auto_close = True
                )
        
    except FileNotFoundError :
        gui.popup(
                    'É necessário ter um caminho para salvar o arquivo',
                    font = ('Arial', 40),
                    no_titlebar = True,
                    button_type = 5,
                    auto_close = True
                )
    
#------------------------------------------------------------------------------------------------------
try:
    #campo = ['Solicitação', 'Requisitante', 'Identificador']
    campo = ['Solicitação']

    converter_xlsx_para_csv(sv.pegar_arquivo(), campo)

except FileNotFoundError :
    gui.popup(
                'É necessário ter um arquivo',
                font = ('Arial', 40),
                no_titlebar = True,
                button_type = 5,
                auto_close = True
            )
    