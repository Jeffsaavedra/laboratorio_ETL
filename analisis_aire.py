import pandas as pd
import requests
from typing import Set

#----------->>>>>>>>>> EJERCICIO 1 <<<<<<<<<<---------------------------

def ej_1_cargar_datos_demograficos() -> pd.DataFrame:
    url = "https://public.opendatasoft.com/explore/dataset/us-cities-demographics/download/?format=csv&timezone=Europe/Berlin&lang=en&use_labels_for_header=true&csv_separator=%3B"
    data = pd.read_csv(url, sep=';')
    data.drop(columns=['Race', 'Count', 'Number of Veterans'], inplace=True)
    data.drop_duplicates(inplace=True)

    # Guardar los datos demográficos en un archivo CSV
    data.to_csv("datos_demograficos.csv", index=False)

    return data

#----------->>>>>>>>>> EJERCICIO 2 <<<<<<<<<<---------------------------

def obtener_calidad_aire(ciudad: str, api_key: str) -> dict:
    api_url = f'https://api.api-ninjas.com/v1/airquality?city={ciudad}'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})

    if response.status_code == requests.codes.ok:
        data = response.json()  # La respuesta se guarda en data

        try:
            # volcamos resultados a la variable concentraciones
            concentraciones = {k: v['concentration'] for k, v in data.items() if k != 'overall_aqi'}
            concentraciones['city'] = ciudad
            concentraciones['overall_aqi'] = data['overall_aqi']
            return concentraciones
        # manejo de errores
        except KeyError as e:
            print(f"Error en el formato de datos para la ciudad: {ciudad}, Error: {e}")
            return {}
    else:
        print("Error en la solicitud:", response.status_code, response.text)
        return {}
    
def ej_2_cargar_calidad_aire(ciudades: Set[str], api_key: str) -> None:
    calidad_aire = []
    for ciudad in ciudades:
        try:
            print(f"Obteniendo datos de calidad del aire para la ciudad: {ciudad}")
            datos = obtener_calidad_aire(ciudad, api_key)
            if datos:
                calidad_aire.append(datos)
        except Exception as e:
            print(f"No se pudieron obtener datos para la ciudad: {ciudad}. Error: {e}")

    if calidad_aire:  # Verifica si se recuperaron datos
        df_calidad_aire = pd.DataFrame(calidad_aire)
        df_calidad_aire.to_csv("calidad_aire.csv", index=False)
    else:
        print("No se recuperaron datos de calidad del aire.")


"""# ejemplo Ejercicio 1
data_demograficos = ej_1_cargar_datos_demograficos()
print("Datos Demográficos:")
print(data_demograficos.head())

# ejemplo Ejercicio 2 (Especifica las ciudades que deseas consultar)
ciudades_a_consultar = {"New York", "Los Angeles", "Chicago", "Houston", "Phoenix"}
data_calidad_aire = ej_2_cargar_calidad_aire(ciudades_a_consultar,  api_url )
print("\nDatos de Calidad del Aire:")
print(data_calidad_aire.head())"""

#----------->>>>>>>>>> EJERCICIO 3 <<<<<<<<<<---------------------------

def ej_3_limpiar_datos_demograficos(data_demograficos: pd.DataFrame) -> pd.DataFrame:
    # Elimina columnas especificadas
    data_demograficos = data_demograficos.drop(columns=["Race", "Count", "Number of Veterans"])

    # Elimina filas duplicadas
    data_demograficos = data_demograficos.drop_duplicates()

    return data_demograficos

#----------->>>>>>>>>> EJERCICIO 4 <<<<<<<<<<---------------------------

import sqlite3
import pandas as pd

def ej_4_crear_cargar_base_de_datos():
    # Conexión a la base de datos (se crea si no existe)
    db = sqlite3.connect('calidad_aire.db')

    try:
        # Cargar y guardar datos demográficos en la base de datos
        df_demograficos = pd.read_csv("datos_demograficos.csv")
        print("Datos demográficos cargados correctamente.")
        print(df_demograficos.head())  # Imprime los primeros registros para verificar

        df_demograficos.to_sql('demografia', db, if_exists='replace', index=False)
        print("Datos demográficos guardados en la base de datos.")

        # Cargar y guardar datos de calidad del aire en la base de datos
        df_calidad_aire = pd.read_csv("calidad_aire.csv")
        print("Datos de calidad del aire cargados correctamente.")
        

        df_calidad_aire.to_sql('calidad_aire', db, if_exists='replace', index=False)
        print("Datos de calidad del aire guardados en la base de datos.")

    except Exception as e:
        print("Ocurrió un error durante la carga de datos: ", e)
    finally:
        # Cerrar la conexión a la base de datos
        db.close()
        print("Conexión a la base de datos cerrada.")

if __name__ == "__main__":
    ej_4_crear_cargar_base_de_datos()

#----------->>>>>>>>>> EJERCICIO 5 <<<<<<<<<<---------------------------

def ej_5_analizar_calidad_aire_ciudades_mas_pobladas() -> pd.DataFrame:
    # Conectar a la base de datos SQLite
    db = sqlite3.connect('calidad_aire.db')

    # Consulta SQL para JOIN entre las tablas y ordenar por población y calidad del aire
    consulta_sql = """
    SELECT d.City, d.State, d.`Total Population`, a.overall_aqi
    FROM demografia d
    INNER JOIN calidad_aire a ON d.City = a.city
    ORDER BY d.`Total Population` DESC, a.overall_aqi DESC
    LIMIT 10
    """

    # Ejecutar la consulta y obtener los resultados
    resultados = pd.read_sql_query(consulta_sql, db)
    print(resultados)

    # Cerrar la conexión a la base de datos
    db.close()


if __name__ == "__main__":
    ej_5_analizar_calidad_aire_ciudades_mas_pobladas()