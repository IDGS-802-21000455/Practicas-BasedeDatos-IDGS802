from flask import Flask,request,render_template,flash, g
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db
from models import Alumnos,Maestros
import forms


app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route("/index",methods=["GET","POST"])
def index():
    alum_form=forms.UserForm2(request.form)
    if request.method=='POST'and alum_form.validate():
        alum=Alumnos(nombre=alum_form.nombre.data,
                 apaterno=alum_form.apaterno.data,
                 email=alum_form.email.data)
        #insert into alumnos values()
        db.session.add(alum)
        db.session.commit()    
    return render_template('index.html', form=alum_form)

@app.route("/maestros",methods=["GET","POST"])
def maestros():
    maes_form=forms.UserForm3(request.form)
    if request.method=='POST'and maes_form.validate():
        maes=Maestros(segnombre=maes_form.segnombre.data,
                 amaterno=maes_form.amaterno.data,
                 numerotel=maes_form.telefono.data,
                 añoNac=maes_form.añoNac.data,
                 edad=maes_form.edad.data)
        #insert into maestros values()
        db.session.add(maes)
        db.session.commit()    
    return render_template('maestros.html', form=maes_form)

@app.route("/ABC_Completo", methods=["GET", "POST"])
def ABCompleto():
    alum_form = forms.UserForm2(request.form)
    alumno = Alumnos.query.all()
    maestro = Maestros.query.all()  # Obtener la lista de maestros
    
    return render_template("/ABC_Completo.html", alumno=alumno, maestro=maestro)


@app.route("/alumnos",methods=["GET","POST"])
def alumnos():
    
    nombre=''
    apa=''
    ama=''  
    alum_form=forms.UserForm(request.form)
    if request.method=='POST'and alum_form.validate():
        nombre=alum_form.nombre.data
        apa=alum_form.apaterno.data
        ama=alum_form.amaterno.data
        mensaje='Bienvenido: {}'.format(nombre)
        flash(mensaje)
        print("nombre:{}".format(nombre))
        print("apaterno:{}".format(apa))
        print("amaterno:{}".format(ama))
    return render_template('alumnos.html',form=alum_form,nombre=nombre,apaterno=apa,amaterno=ama)


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    app.run()
