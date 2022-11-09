from flask import render_template, redirect, request, session, flash
from flask_app import app

#Importamos modelo
from flask_app.models.users import User
from flask_app.models.recipes import Recipe


#Importación de BCrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


#ruta raiz
@app.route('/')
def index():
    return render_template('index.html')



#ruta registro
@app.route('/register', methods=['Post'])
def register():
    #Validamos la info q recibimos
    if not User.valida_usuario(request.form):
        return redirect('/')

    #guardar registro
    pwd = bcrypt.generate_password_hash(request.form['password']) #Encriptando la contraseña del usuario y guardándola 
    #en pwd

    #creamos un diccionario con todos los datos del request.form
    #request.form['password'] = pwd ->ERROR: Request no se puede cambiar, x eso tenemos q crear otro, dnd password sea 
    #igual a la contraseña encriptada (pwd)
    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pwd
    }

    id = User.save(formulario) #Recibimos el identificador del nuevo usuario /id es una variable
    session['user_id'] = id #Guardamos en sesion el identificador del usuario

    return redirect('/dashboard')



#ruta login con mensaje verificacion y mensaje error email y contraseña
@app.route('/login', methods=['POST'])
def login():
    #verificamos q el email exista en la base de datos 
    user = User.get_by_email(request.form) #Recibimos una instancia de usuario O False

    if not user: #Si user = False 
        flash('E-mail no encontrado', 'login')
        return redirect('/') #regresa al index con los formularios

    #user es una instancia con todos los datos de mi usuario 
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/') #regresa al index con los formularios

    session['user_id'] = user.id
    return redirect('/dashboard') #si todo esta correcto, redirige a dashboard



#ruta dashboard / #validar q si se haya iniciado sesion para mostrar dashboard
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    #Lista con todas las recetas
    recipes = Recipe.get_all()

    return render_template('dashboard.html', user=user, recipes=recipes)



#ruta cerrar sesion
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
