# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
"""
#proyectofinal2
#seimportapandas
#seleeelarchivoenpandas
synergy_dataframe =pd.read_csv('synergy_logistics_database.csv', index_col=0,
                                encoding='utf-8', 
                                parse_dates=[4, 5])
# se separandetalformaque
exports = synergy_dataframe[synergy_dataframe['direction'] == 'Exports']
imports = synergy_dataframe[synergy_dataframe['direction'] == 'Imports']

#  definefuncionparasaber las rutas de import y export
def tarea_1(df, num_rutas):
    rutas = df.groupby(by=['origin', 'destination', 'transport_mode'])
    descrip_rutas = rutas.describe()['total_value']
    rutas_freq = descrip_rutas['count']
    rutas_freq_sort = rutas_freq.sort_values(ascending=False)
    rutas_freq_sort_df = rutas_freq_sort.to_frame().reset_index()
    lista_rutas_demanda = rutas_freq_sort_df.head(num_rutas)  
    return lista_rutas_demanda
# se pide cantidad de rutas masdemanda
demanda_rutas = int(input('Numero minimo de rutas más demandadas de exportaciones/importaciones: '))
result1_exp = tarea_1(exports, demanda_rutas)
result1_imp = tarea_1(imports, demanda_rutas)
print('\nSolución a la consigna 1 para exportaciones:\n')
print(result1_exp)
print('\nSolución a la consigna 1 para importaciones:\n')
print(result1_imp)
import seaborn as sns
# se define la funcion para medio de trasporte
def tarea_2(df):
    datos_transport = df.copy()

    datos_transport['year_month'] = datos_transport['date'].dt.strftime('%Y-%m')
    datos_year_month = datos_transport.groupby(['year_month', 'transport_mode'])
    serie = datos_year_month.mean()['total_value']
    transport_dym = serie.to_frame().reset_index()
    transport_dym = transport_dym.pivot('year_month', 'transport_mode', 'total_value')
    # Grafico
    sns.lineplot(data=transport_dym)


#grafica de medios de transporte
tarea_2(synergy_dataframe)

# valor total de importaciones y exportaciones
def tarea_3(df, porcentaje):
    pais_total_value = df.groupby('origin').sum()['total_value'].reset_index()
    total_value_for_percent = pais_total_value['total_value'].sum()
    pais_total_value['percent'] = 100 * pais_total_value['total_value'] / total_value_for_percent
    pais_total_value.sort_values(by='percent', ascending=False, inplace=True)
    pais_total_value['percent accum'] = pais_total_value['percent'].cumsum()
    lista_acumulada = pais_total_value[pais_total_value['percent accum'] < porcentaje]
    
    return lista_acumulada

# porcentaje del valor total generado
porcent_util = int(input('¿Qué porcentaje del valor total generados quiere saber de la empresa?: '))

result3_exp = tarea_3(exports, porcent_util)
result3_imp = tarea_3(imports, porcent_util)

# se imprime en consola los resultados
print('\nSolución a la consigna 3 para exportaciones:\n')
print(result3_exp)
print('\nSolución a la consigna 3 para importaciones:\n')
print(result3_imp)