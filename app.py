#importacion de las librerias necesarias para el codigo
from flask import Flask,request ,render_template, redirect, url_for,flash, request, session, get_flashed_messages
from controllers.consultas import Consultas
from controllers.appis import *
from flask import jsonify
import time

#se llama las herramientas para usar flask
app = Flask(__name__)
app.secret_key = 'Admin1234'

#se obtienen datos para rellenar Select de la pagina de voluntariado
@app.route('/get_data')
def get_data():
    time.sleep(4) #esto da 4 segundos de retraso
    data = {"message": "Datos cargados correctamente"}
    return jsonify(data)

#hace referencia a la pagina principal si no esta logueado
@app.route('/')
def hometwo():
    datos_clima = clima()
    return render_template('index.html', datos=datos_clima)

#se manda a llamar a la pagina principal si el usuario esta logueado
@app.route('/index.html')
def home():
    datos_clima = clima()
    if 'logged_in' in session and session['logged_in']:
        email = session.get('nombreUsuario')
        print("Nombre en home:", email)
        return render_template('index.html', datos=datos_clima, email=email)  # Asegúrate de que 'home.html' exista
    else:
        # Redirige a la página de login si no está autenticado
        return redirect(url_for('/'))

#MANDA A LLAMAR A LA PAGINA DE DONACIONES
@app.route('/donar', methods=['GET', 'POST'])
def donaciones():
    consulta = Consultas()
    if request.method == 'POST':
        # Cambia request.method['campo'] por request.form['campo']
        nombre   = request.form['nombre']
        apellido = request.form['apellido']
        email    = request.form['Email']
        phone    = request.form['phone']
        donacion = request.form['dinero']
        
        # Verifica que todos los campos estén presentes
        if nombre and apellido and email and phone and donacion:
            try:
                # Llama al método para insertar la donación en la base de datos
                result = consulta.donaciones(nombre, apellido, email, phone, donacion)
                if result:
                    flash('DONACION EXITOSA', 'SUCCESS')
                else:
                    flash('HUBO UN ERROR CON TU DONACION :(', 'ERROR')
            except Exception as err:
                flash('HUBO UN ERROR CON TU DONACION :(')
                return f"Error: {err}"
        else:
            flash('LLene todos los campos para completar la donacion')
    return render_template('dona.html')  


@app.route('/login', methods = ['GET', 'POST'])
def login():
    consulta = Consultas()
    
    if request.method == 'POST':
        email = request.form['email']
        passw = request.form['password']
        resultado = consulta.validacion_login(email,passw)
        data = resultado.json
        
        if data['success']:
            session['email'] = email
            session['nombreUsuario'] = data['nombreUsuario']
            session['logged_in'] = True
            print("Nombre guardado en sesión:", session['nombreUsuario']) 
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error= data['message'])
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/form', methods =['GET','POST'])
def formularioRegistro():
    consulta = Consultas()
    mensaje = ''
    
    if request.method == 'POST':
        nombre     =   request.form['nombreUsuario']
        email      =   request.form['emailUsuario']
        password   =   request.form['passwordUsuario']
        
        if nombre and email and password:
            try:
                resultado = consulta.insertar_usuario(nombre, email, password)
                #return redirect(url_for('login', resultado = resultado)), flash("Datos ingresados correctamente", 'success')
                flash("Datos ingresados correctamente", 'success')
                return render_template('login.html')
            except Exception as e:
                flash('Hubo un error, intente de nuevo', 'error', {e})
                #return f"Error: {e}"
        else:
            flash('Llene todos los campos para completar el registro', 'error')
        #return redirect(url_for('login'))
    
    return render_template('login.html')

#formulario de voluntario

@app.route('/voluntariado', methods=['GET', 'POST'])
def voluntariadoRegistro():
    consulta = Consultas()
    
    if request.method == 'POST':
        nombre          = request.form['nombreUsuario']
        edad            = request.form['edad']
        email           = request.form['emailUsuario']
        numero_telefono = request.form['phone']
        actividad_id    = request.form['actividad']
        
        if nombre and edad and email and numero_telefono:
            try:
                # Llamar a la verificación antes de insertar
                verificacion = consulta.verificacion_voluntario(email, nombre)
                
                if verificacion:
                    flash("Ya eres voluntario para una actividad amigo. Bien hecho.", 'warning')
                else:
                    resultado = consulta.insertar_voluntarios(nombre, edad, email, numero_telefono, actividad_id)
                    flash(resultado, 'SUCCESS')
            except Exception as e:
                flash('Hubo un error, intente de nuevo', 'error')
                return f"Error: {e}"
        else:
            flash('Llene todos los campos para completar el registro', 'error')
    
        return redirect(url_for('voluntariadoRegistro'))
    else:
        actividades = consulta.get_actividad()
        if actividades is not None and isinstance(actividades, list):
            return render_template('voluntariado.html', actividades=actividades)
        else:
            return "Error al cargar actividades", 500

if __name__ == '__main__':
    app.run(debug=True)

# Ruta principal para mostrar el formulario y resultados
