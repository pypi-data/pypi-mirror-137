#!/usr/bin/env python
# coding: utf-8

import pprint
import pandas as pd


def get_8468_parameters():
    # Read Data
    df_8468 = pd.read_excel(
        #io='https://raw.githubusercontent.com/gaemapiracicaba/norma_dec_8468-76/main/data/tab_dec_8468.xlsx',
        io=os.path.join('..', 'data', 'tab_dec_8468.xlsx'),
        sheet_name='dec_8468',
        index_col=0
    )
    
    # Filter only quality
    df_8468 = df_8468.loc[(df_8468['tipo_padrao'] == 'qualidade')]
    #print(df_8468.head())

    # Classes
    list_classes = list(set(df_8468['padrao_qualidade']))
    list_classes = [x for x in list_classes if pd.notnull(x)]
    list_classes.sort()
    pprint.pprint(list_classes)

    return df_8468, list_classes


def filter_by_classe(df_8468, classe):
    # Filter dataframe by Classe
    df_8468 = df_8468.loc[(df_8468['padrao_qualidade'] == classe)]
    
    # Parâmetros
    list_parametros = list(set(df_8468['parametro_descricao']))
    list_parametros = [x for x in list_parametros if pd.notnull(x)]
    list_parametros.sort()
    pprint.pprint(list_parametros)
    return df_8468, list_parametros


def filter_by_parameters(df_8468, parametro):
    # Filter dataframe by Parametro
    df_8468 = df_8468.loc[(df_8468['parametro_descricao'] == parametro)]
    
    # Check and Get Results
    if len(df_8468) == 1:
        dict_8468 = df_8468.to_dict(orient='records')[0]
        return dict_8468
    else:
        print('Erro')


def set_type_desconformidade(dict_8468):
    if pd.isnull(dict_8468['valor_minimo_permitido']) & pd.isnull(dict_8468['valor_maximo_permitido']):
        print('Erro!')
        tipo_8486 = 'erro'

    elif pd.isnull(dict_8468['valor_minimo_permitido']) & pd.notnull(dict_8468['valor_maximo_permitido']):
        print('Parâmetro só tem "valor máximo". Caso o valor medido esteja acima, é amostra desconforme!')
        tipo_8486 = 'acima>desconforme'

    elif pd.notnull(dict_8468['valor_minimo_permitido']) & pd.isnull(dict_8468['valor_maximo_permitido']):
        print('Parâmetro só tem "valor mínimo". Caso o valor medido esteja abaixo, é amostra desconforme!')
        tipo_8486 = 'abaixo>desconforme'

    elif pd.notnull(dict_8468['valor_minimo_permitido']) & pd.notnull(dict_8468['valor_maximo_permitido']):
        print('Parâmetro tem "valor mínimo" e "valor máximo". Caso o valor medido acima ou abaixo, é amostra desconforme!')
        tipo_8486 = 'abaixo_acima>desconforme'

    return tipo_8486

