from analisis_aire import ej_1_cargar_datos_demograficos, ej_2_cargar_calidad_aire

def main():
    api_key = "aEWMvpOC8a1Xob8ZI3refQ==4tLhGVzzZs7QkQqZ"

    # se llama a la función para cargar los datos demográficos
    df_data_demograficos = ej_1_cargar_datos_demograficos()

    # Crear un conjunto de ciudades a partir de los datos demográficos
    ciudades = set(df_data_demograficos['City'])

    # se llama la función para cargar calidad de aire, pasamos el API_Key y el conjunto de ciudades
    ej_2_cargar_calidad_aire(ciudades, api_key)

if __name__ == "__main__":
    main()