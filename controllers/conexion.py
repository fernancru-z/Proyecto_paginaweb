import pyodbc

server = 'localhost'
database = 'GotaDeVida'
username = 'GotaDeVidaUser'
password = 'TuContraseñaSegura'


def get_db_conection():
    try:    
        conexion = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        if conexion:
            print('Conexión exitosa')
            return conexion
    except pyodbc.Error as e:
        print(f"Error de conexión: {e}")
        return None

conn = get_db_conection()
if conn:
    print("¡La conexión se ha establecido correctamente!")
else:
    print("No se pudo establecer la conexión a la base de datos.")

