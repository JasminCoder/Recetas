from flask import render_template, redirect, request, session, flash
from flask_app import app

#Importamos los modelos
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

#Importaciones para subir imágenes
from werkzeug.utils import secure_filename
import os


#ruta nueva receta
@app.route('/new/recipe')
def new_recipe():
    #validar q si se haya iniciado sesion para mostrar dashboard
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    return render_template('new_recipe.html', user=user)



#ruta crear receta
@app.route('/create/recipe', methods=['POST'])
def create_recipe():
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')
    
    #Validación de Receta
    if not Recipe.valida_receta(request.form):
        return redirect('/new/recipe')

    #Validamos que haya subido algo
    if 'image' not in request.files:
        flash('No seleccionó ninguna imagen', 'receta')
        return redirect('/new/recipe') 

    #Variable con imagen
    image = request.files['image'] 

    #Validamos que el nombre no este vacío
    if image.filename == '':
        flash('Nombre de imagen vacío', 'receta')
        return redirect('/new/recipe')
    
    #Generamos de manera segura el nombre de la imagen
    nombre_imagen = secure_filename(image.filename) 

    #Guardamos la imagen
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_imagen))


    #Diccionario con todos los datos del formulario
    formulario = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_30": int(request.form['under_30']),
        "image": nombre_imagen,
        "user_id": request.form['user_id']
    }

    #Guardamos la receta
    Recipe.save(formulario)

    return redirect('/dashboard')



#para recibir identificador del boton editar del dashboard
@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    #la instancia de la receta que se debe desplegar en editar (en base al ID que recibimos en URL)
    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta)

    return render_template('edit_recipe.html', user=user, recipe=recipe)



#ruta actualizar receta
@app.route('/update/recipe', methods=['POST'])
def update_recipe():
    #Verificar que haya iniciado sesion
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #recibimos formulario = request.form 
    #request.form = {name: "Albondigas", description:"123"....... recipe_id:1}

    #Verificar que todos los datos esten correctos
    if not Recipe.valida_receta(request.form):
        return redirect('/edit/recipe/'+request.form['recipe_id']) #/edit/recipe/1

    #Guardar los cambios
    Recipe.update(request.form)

    #Redireccionar a /dashboard
    return redirect('/dashboard')



#borrar receta
@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    #Verificar que haya iniciado sesion
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #Borramos
    formulario = {"id": id}
    Recipe.delete(formulario)

    #Redirigir a /dashboard
    return redirect('/dashboard')



#ruta ver receta
@app.route('/view/recipe/<int:id>')
def view_recipe(id):
    #Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session: #Comprobamos que inicia sesión
        return redirect('/')

    #Saber cuál es el nombre del usuario que inicio sesión
    #Yo sé que en sesión tengo el id de mi usuario (session['user_id'])
    #Queremos una función que en base a ese id me regrese una instancia del usuario
    formulario = {"id": session['user_id']}
            

    user = User.get_by_id(formulario) #Recibo la instancia de usuario en base a su ID

    #Objeto receta q queremos desplegar
    formulario_receta = {"id": id}
    recipe = Recipe.get_by_id(formulario_receta)

    #Renderizamos show_recipe.html
    return render_template('show_recipe.html', user=user, recipe=recipe)