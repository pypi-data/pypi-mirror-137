#!/usr/bin/env python
# coding: utf-8

import os
print(os.getcwd())


print(this_filename)

from decreto_estadual_8468 import *




# Get Table
df_8468, list_classes = get_8468_parameters()

# Filter Data by "Classe"
df_8468, list_parametros = filter_by_classe(df_8468, classe='Classe 2')

# Filter Data by "Parâmetros"
dict_8468 = filter_by_parameters(df_8468, parametro='Oxigênio Dissolvido')
print(dict_8468)

# Set Tipo
set_type_desconformidade(dict_8468)
