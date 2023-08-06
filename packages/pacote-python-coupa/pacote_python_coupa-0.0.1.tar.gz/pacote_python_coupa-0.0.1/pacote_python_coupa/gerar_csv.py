#------------------------------------------------------------------------------------------------------
# imports
import csv, PySimpleGUI as gui, pandas as pd, numpy as np, pegar_salvar_arquivo as sv
from datetime import datetime
from datetime import timedelta
from time import strftime
from humanfriendly import format_timespan
from scalpl import Cut

#------------------------------------------------------------------------------------------------------
gui.theme('dark grey 9')

#------------------------------------------------------------------------------------------------------
# Funções

def gerar_csv(cabecalhoFunctionGerarCSV: list, valoresFunctionGerarCSV: list):
    try:
        if len(cabecalhoFunctionGerarCSV) == 1 and len(valoresFunctionGerarCSV) == 1:
            cabecalhoFunctionGerarCSV = cabecalhoFunctionGerarCSV[0].split(',')
            valoresFunctionGerarCSV = valoresFunctionGerarCSV[0].split(',')
            
        try:
            # Remove os \n no final da lista
            valoresFunctionGerarCSV = list(map(lambda x:x.strip(), valoresFunctionGerarCSV))
            
        except:
            pass
        
        # Deixa os valores com a mesma quantidade de keys.
        listaDivididaPorKeys = [valoresFunctionGerarCSV[i:i + len(cabecalhoFunctionGerarCSV)] for i in range(0, len(valoresFunctionGerarCSV), len(cabecalhoFunctionGerarCSV))]
        
        # Junta duas lista e transforma em um dicionario
        dicionarioFormadoComValues = [dict(zip(cabecalhoFunctionGerarCSV, valoresFomatados)) for valoresFomatados in listaDivididaPorKeys]
        
        # Criar um arquivo .csv delimitado com "," e Aspas duplas
        salvar = sv.salvar_arquivo_csv()
        with open(salvar, 'w', newline='', encoding='utf-8') as saida:
            escrever = csv.DictWriter(saida, dicionarioFormadoComValues[0].keys(), delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            
            escrever.writeheader() # Escreve o cabeçalho(keys) do .csv
            escrever.writerows(dicionarioFormadoComValues) # Escreve os valores(values) do .csv
        # Cria um Pop-Up
        gui.popup(
                    'CSV Criado',
                    font = ('Arial', 40),
                    no_titlebar = True,
                    button_type = 5,
                    auto_close = True
                )
        
    except IndexError as erro:
        gui.popup(
                    erro,
                    font = ('Arial', 40),
                    no_titlebar = True,
                    button_type = 5,
                    auto_close_duration = 10
                )

#------------------------------------------------------------------------------------------------------