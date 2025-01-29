from .conexion import get_db_conection
import hashlib
import pyodbc
from flask import jsonify
from werkzeug.security import check_password_hash

class Consultas:
    #METODO DONDE SE HACE MENCION A LA CONEXION
    def __init__(self):
        self.connection = get_db_conection()
    
    #VERIFICA SI EN LA BASE DE DATOS NO HAY O HAY UN CORREO IGUAL
    def varificacion_correo(self, correo):
        try:
            cursorVerifi = self.connection.cursor()
            query = "SELECT COUNT(*) FROM usuario WHERE correo = ?"
            cursorVerifi.execute(query,(correo,))
            resultado = cursorVerifi.fetchone()
            return resultado[0]>0
        except pyodbc.Error as ex:
            print (f"Error al ejecutar consulta de verificacion: {ex}")
            return False
        finally:
            cursorVerifi.close()
    
    #INSERTA UN NUEVO USUARIO Y HACE UN FILTRO SI HAY UN USUARIO INDICA QUE YA ESTA EN USO EL CORREO
    def insertar_usuario(self, nombre_usuario, correo, password):
        if self.connection:
            if self.varificacion_correo(correo):
                return "El correo ya esta en uso"
            
        cursor = self.connection.cursor()
        query = "INSERT INTO usuario (nombreUsuario, correo, pass) VALUES (?, ?, ?)"
        cursor.execute(query, (nombre_usuario, correo, password))
        self.connection.commit()
        cursor.close()
    
    #ESTE METODO VALIDA SI EL USUARIO SE HA LOGUEADO CORRECTAMENTE A LA WEB O EN SU DEFECTO SI NO ESTAN BIEN LAS CREDENCIALES
    def validacion_login(self, email, password):
        try:
            if self.connection:
                cursorLogin = self.connection.cursor()
                cursorLogin.execute("SELECT nombreUsuario FROM usuario WHERE correo = ? AND pass = ?" ,(email.strip(), password.strip()))
                resultado = cursorLogin.fetchone()
                cursorLogin.close()
                self.connection.close()
                
                if resultado:
                    nombreUsuario = resultado[0]
                    print("El nombre obtenido: ", nombreUsuario)
                    return jsonify(success = True, message="Bienvenido nuevamente", nombreUsuario = nombreUsuario)
                else:
                    return jsonify(success = False, message = "Verica tu correo o contraseña")

        except pyodbc.Error as e:
            return jsonify(success = False, message = f"Error al conectar con la base de datos {e}")
    
    #para decifrar contraseñas   
    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).digest()
    
    #validacion de login para sessiones
    def validando_secion(self, correo, password):
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT correo, password FROM usuario WHERE correo = ?', (correo,))
        usuario = cursor.fetchone()
        cursor.close()
        
        if usuario:
            decifradoPass = self.hash_password(password)
            if usuario.password == decifradoPass:
                return True
        return False
                
    #insertar voluntarios
    def insertar_voluntarios(self, nombre, edad, email, telefono, actividad):
        if self.connection:
            if self.verificacion_voluntario(email, nombre):
                return "Ya eres voluntario para una actividad amigo Bien hecho"
            
            cursorVolun = self.connection.cursor()
            query = "INSERT INTO voluntariado (nombreVolun, edadVolun, correoVolun, numeroTel, idActividad) VALUES (?, ?, ?, ?, ?)"
            cursorVolun.execute(query , (nombre , edad,  email, telefono, actividad))
            self.connection.commit()
            cursorVolun.close()
            
    #VERIFICA SI UNA PERSONA YA SE REGISTRO COMO VOLUNTARIADO EN ALGUNA ACTIVIDAD
    def verificacion_voluntario(self, correo, nombre):
        try:
            cursoVerificacion = self.connection.cursor()
            query = "SELECT COUNT(*) FROM voluntariado WHERE correoVolun = ? AND nombreVolun = ?"
            cursoVerificacion.execute(query, (correo, nombre))
            result = cursoVerificacion.fetchone()
            return result[0] > 0
        except pyodbc.Error as err:
            print (f"Error al ejecutar la consulta de verificacion: {err}")
            return False
        finally:
            cursoVerificacion.close()
    
    #obtener actividades
    def get_actividad(self):
        actividad = []
        if self.connection:
            try:
                
                cursorObtener = self.connection.cursor()
                queryTwo = ("SELECT idActividad, actividad FROM actividad")
                cursorObtener.execute(queryTwo)
                actividad = cursorObtener.fetchall()
                cursorObtener.close()
                self.connection.close()
                return actividad
            except pyodbc.Error as err:
                print(f"Error al obtener las actividades: {err}")
                return actividad
        return actividad
    
    #metodo para insertar donaciones:
    def donaciones(self, nombreDonador, apellidoDonador, correoDonador, telefono, cantidadDonacion):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                query = "INSERT INTO donaciones(nombreDonador, apellidoDonador, correoDonador, telefono, cantidadDonacion) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(query, (nombreDonador, apellidoDonador, correoDonador, telefono, cantidadDonacion))
                self.connection.commit()
                cursor.close()
                return True
            except pyodbc.Error as err:
                print(f"No se pudieron insertar datos: {err}")
                return False

    
    
                
        
        
    

