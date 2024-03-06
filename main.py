from flask import Flask,request,render_template,flash, g, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db
from models import Alumnos,Maestros,Pedido
import forms
from sqlalchemy import func



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
       
        db.session.add(maes)
        db.session.commit()    
    return render_template('maestros.html', form=maes_form)



orders = []  
def generate_order_id():
    return len(orders) + 1

@app.route("/pizzas", methods=["GET", "POST"])
def pizzas():
    form = forms.PizzeriaForm(request.form)

    if request.method == 'POST' and form.validate():
        subtotal = calcular_subtotal(
            form.tamanioPizza.data,
            form.jamon.data,
            form.pinia.data,
            form.champiniones.data,
            form.numPizzas.data
        )

        order_data = {
            'ID': len(orders) + 1,  
            'Nombre': form.nombre.data,
            'Direccion': form.direccion.data,
            'Telefono': form.telefono.data,
            'Tamano': form.tamanioPizza.data,
            'Ingredientes': ', '.join([ingredient for ingredient, value in [('Jamón', form.jamon.data),
                                                                            ('Piña', form.pinia.data),
                                                                            ('Champiñones', form.champiniones.data)] if value]),
            'Num. Pizzas': form.numPizzas.data,
            'Subtotal': subtotal
        }
        orders.append(order_data)

    return render_template('pizzas.html', form=form, orders=orders)

@app.route("/finalizar_pedido", methods=["GET", "POST"])
def finalizar_pedido():
    for order in orders:
        pedido = Pedido(
            nombre=order['Nombre'],
            direccion=order['Direccion'],
            telefono=order['Telefono'],
            tamano_pizza=order['Tamano'],
            ingredientes=order['Ingredientes'],
            num_pizzas=order['Num. Pizzas'],
            subtotal=order['Subtotal']
            
        )
        db.session.add(pedido)

    db.session.commit()
    orders.clear()  

    return redirect(url_for('pizzas'))




@app.route("/cancelar_pedido", methods=["POST"])
def cancelar_pedido():
    flash("El pedido ha sido cancelado.")
    return redirect(url_for('pizzas'))

@app.route("/confirmar_pedido", methods=["POST"])
def confirmar_pedido():
    total_costo = sum(order['Subtotal'] for order in orders)
    return render_template('confirmar_pedido.html', total_costo=total_costo)


@app.route("/remove_order", methods=["POST"])
def remove_order():
    order_id = int(request.form.get('order_id'))

    
    for order in orders:
        if order['ID'] == order_id:
            orders.remove(order)
            break

    return redirect(url_for('pizzas'))

def calcular_subtotal(tamanio, jamon, pinia, champiniones, num_pizzas):
   
    precios = {'Chica': 40, 'Mediana': 80, 'Grande': 120, 'Jamon': 10, 'Pinia': 10, 'Champiniones': 10}

   
    if tamanio not in precios:
        return 0  

    subtotal = precios[tamanio]
    if jamon:
        subtotal += precios['Jamon']
    if pinia:
        subtotal += precios['Pinia']
    if champiniones:
        subtotal += precios['Champiniones']

    return subtotal * num_pizzas




@app.route("/ABC_Completo", methods=["GET", "POST"])
def ABCompleto():
    alum_form = forms.UserForm2(request.form)
    alumno = Alumnos.query.all()
    maestro = Maestros.query.all()  
    
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

from sqlalchemy import cast, Date

from sqlalchemy import func, cast, Date
import datetime

from sqlalchemy import func, cast, Date
from sqlalchemy.sql.expression import text

# ...

@app.route("/ventas_acumuladas", methods=["GET", "POST"])
def ventas_acumuladas():
    form = forms.VentasForm(request.form)

    if request.method == 'POST' and form.validate():
        fecha_ingresada = form.fecha.data

        if form.tipo.data == 'dia':
            ventas = db.session.query(func.date(Pedido.fecha_pedido).label('Fecha'),
                                      func.sum(Pedido.subtotal).label('TotalVentas')) \
                .filter(cast(Pedido.fecha_pedido, Date) == fecha_ingresada) \
                .group_by(func.date(Pedido.fecha_pedido)) \
                .order_by('Fecha') \
                .all()
            tipo = 'Día'
        elif form.tipo.data == 'mes':
            ventas = db.session.query(func.DATE_FORMAT(Pedido.fecha_pedido, '%Y-%m-01').label('Fecha'),
                                      func.sum(Pedido.subtotal).label('TotalVentas')) \
                .filter(func.DATE_FORMAT(Pedido.fecha_pedido, '%Y-%m') == fecha_ingresada.strftime('%Y-%m')) \
                .group_by(func.DATE_FORMAT(Pedido.fecha_pedido, '%Y-%m-01')) \
                .order_by('Fecha') \
                .all()
            tipo = 'Mes'
        else:
            ventas = db.session.query(func.date(Pedido.fecha_pedido).label('Fecha'),
                                      func.sum(Pedido.subtotal).label('TotalVentas')) \
                .group_by(func.date(Pedido.fecha_pedido)) \
                .order_by('Fecha') \
                .all()
            tipo = 'Todos'

        return render_template('ventas_acumuladas.html', form=form, ventas=ventas, tipo=tipo)

    return render_template('ventas_acumuladas.html', form=form, ventas=None, tipo='Todos')









if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    app.run()
