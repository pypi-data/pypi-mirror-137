#!/usr/bin/env python
# coding: utf-8

from normas import decreto_estadual_8468

# Get Table
df_8468, list_classes = decreto_estadual_8468.get_parameters()

# Filter Data by "Classe"
df_8468, list_parametros = decreto_estadual_8468.filter_by_classe(df_8468, classe='Classe 2')

# Filter Data by "Parâmetros"
dict_8468 = decreto_estadual_8468.filter_by_parameters(df_8468, parametro='Oxigênio Dissolvido')
print(dict_8468)

# Set Tipo
decreto_estadual_8468.set_type_desconformidade(dict_8468)
