from flask import Flask, render_template, request, redirect, url_for
import db
from models import Tarea

app= Flask(__name__) # En app se encuentra nuestro servidor web de Flask

#Pagina de inicio (pagina home)
@app.route("/")
def home():
    todas_las_tareas= db.session.query(Tarea).all() #Consultamos y almacenamos todas las tareas de la base de datos
    return render_template("index.html", lista_de_tareas= todas_las_tareas)

@app.route('/crear-tarea', methods= {'POST'})
def crear():
    tarea= Tarea(contenido=request.form['contenido_tarea'], hecha= False) #No necesario id ya que es primary key
    db.session.add(tarea) #Añadir el objeto de Tarea a la base de datos
    db.session.commit() # Ejecutar la operacion pendiente de la base de datos
    db.session.close()
    return redirect(url_for('home'))

@app.route('/eliminar-tarea/<id>')
def eliminar(id):
    tarea= db.session.query(Tarea).filter_by(id=int(id)).delete()#Buscar un registro y si se encuentra, eliminarlo
    db.session.commit()
    db.session.close()
    return redirect(url_for('home')) # Redireccionar a home

@app.route('/tarea-hecha/<id>')
def hecha(id):
    tarea= db.session.query(Tarea).filter_by(id=int(id)).first() #Buscar la tarea
    tarea.hecha= not(tarea.hecha) #Cambiamos al valor contrario la variable booleana
    db.session.commit()
    db.session.close()
    return redirect(url_for('home')) # Redireccionar a home

@app.route('/eliminar-todo')
def eliminar_todo():
    todas_las_tareas = db.session.query(Tarea).all()  # Consultamos y almacenamos todas las tareas de la base de datos
    id = 1
    for tarea in todas_las_tareas:
        db.session.query(Tarea).delete()
    db.session.commit()
    db.session.close()
    return redirect(url_for('home')) # Redireccionar a home



if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine) #Creacion del modelo de datos
    app.run(debug= True) #El debut=True hace que cada vez que reiniciemos el servidor o modifiquemos codigo, el servidor de Flask se reinicie solo