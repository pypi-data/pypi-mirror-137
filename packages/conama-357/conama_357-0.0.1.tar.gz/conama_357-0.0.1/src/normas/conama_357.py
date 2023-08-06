#!/usr/bin/env python
# coding: utf-8

import os
import pprint
import pandas as pd
from collections import OrderedDict


def get_parameters():
    # Read Data
    try:
        df_357 = pd.read_excel(
            io=os.path.join(os.path.dirname(__file__), 'data', 'tab_conama_357.xlsx'),
            sheet_name='conama_357',
            index_col=0,
        )
    except Exception as e:
        print(e, '\n')
        print('Read table from GitHub')
        df_357 = pd.read_excel(
            io='https://raw.githubusercontent.com/gaemapiracicaba/norma_res_conama_357-05/main/src/normas/data/tab_conama_357.xlsx',
            sheet_name='conama_357',
            index_col=0,
        )

    # Filter only quality
    df_357 = df_357.loc[(df_357['tipo_padrao'] == 'qualidade')]
    #print(df_357.head())

    # Classes
    list_classes = list(set(df_357['padrao_qualidade']))
    list_classes = [x for x in list_classes if pd.notnull(x)]
    list_classes.sort()
    pprint.pprint(list_classes)

    return df_357, list_classes


def filter_by_classe(df_357, classe):
    # Filter dataframe by Classe
    df_357 = df_357.loc[(df_357['padrao_qualidade'] == classe)]

    # Parâmetros
    list_parametros = list(set(df_357['parametro_descricao']))
    list_parametros = [x for x in list_parametros if pd.notnull(x)]
    list_parametros.sort()
    pprint.pprint(list_parametros)
    return df_357, list_parametros


def filter_by_parameters(df_357, parametro):
    # Filter dataframe by Parametro
    df_357 = df_357.loc[(df_357['parametro_descricao'] == parametro)]

    # Check and Get Results
    if len(df_357) == 1:
        dict_357 = df_357.to_dict(orient='records')[0]
        dict_357 = OrderedDict(sorted(dict_357.items(), key=lambda x: df_357.columns.get_loc(x[0])))
        return dict_357
    else:
        #TODO: Ajustar condições
        print('Tem mais de um registro de "{}". Específicar condição!'.format(parametro))
        return 'erro'


def set_type_desconformidade(dict_357):
    if pd.isnull(dict_357['valor_minimo_permitido']) & pd.notnull(dict_357['valor_maximo_permitido']):
        #print('Parâmetro só tem "valor máximo". Caso o valor medido esteja acima, é amostra desconforme!')
        tipo_357 = 'acima>desconforme'

    elif pd.notnull(dict_357['valor_minimo_permitido']) & pd.isnull(dict_357['valor_maximo_permitido']):
        #print('Parâmetro só tem "valor mínimo". Caso o valor medido esteja abaixo, é amostra desconforme!')
        tipo_357 = 'abaixo>desconforme'

    elif pd.notnull(dict_357['valor_minimo_permitido']) & pd.notnull(dict_357['valor_maximo_permitido']):
        #print('Parâmetro tem "valor mínimo" e "valor máximo". Caso o valor medido acima ou abaixo, é amostra desconforme!')
        tipo_357 = 'abaixo_acima>desconforme'

    elif pd.isnull(dict_357['valor_minimo_permitido']) & pd.isnull(dict_357['valor_maximo_permitido']):
        #print('Erro!')
        tipo_357 = 'erro'
    else:
        print('Erro!')
        tipo_357 = 'erro'

    return tipo_357


def evaluate_result(valor, dict_357):
    # Get type
    tipo_357 = set_type_desconformidade(dict_357)

    # Evaluate type
    if tipo_357 == 'acima>desconforme':
        if valor > dict_357['valor_maximo_permitido']:
            result_357 = 'desconforme'
        else:
            result_357 = 'conforme'

    elif tipo_357 == 'abaixo>desconforme':
        if valor < dict_357['valor_minimo_permitido']:
            result_357 = 'desconforme'
        else:
            result_357 = 'conforme'

    elif tipo_357 == 'abaixo_acima>desconforme':
        if dict_357['valor_minimo_permitido'] <= valor <= dict_357['valor_maximo_permitido']:
            result_357 = 'conforme'
        else:
            result_357 = 'desconforme'

    elif tipo_357 == 'erro':
        result_357 = 'erro'

    else:
        result_357 = 'erro'

    return result_357

