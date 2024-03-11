from flask import Flask, request, render_template, flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db
from models import Alumnos, Maestros, Pedido
import forms
from sqlalchemy import func, cast, Date
from datetime import datetime, timedelta
from sqlalchemy.sql.expression import text

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
            'Subtotal': subtotal,
            'FechaPedido': form.fechaPedido.data
        }
        orders.append(order_data)

    if orders:  
        form.nombre.data = orders[0]['Nombre']
        form.direccion.data = orders[0]['Direccion']
        form.telefono.data = orders[0]['Telefono']
        form.fechaPedido.data = orders[0]['FechaPedido']
        print("ordenesPizzas: {}".format(orders[0]))

    return render_template('pizzas.html', form=form, orders=orders)

dias_en_ingles = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miercoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sabado",
    "Sunday": "Domingo"
}


@app.route("/finalizar_pedido", methods=["GET", "POST"])
def finalizar_pedido():
    for order in orders:
        fecha_pedido = order['FechaPedido']
        nombre_dia_semana_es = dias_en_ingles.get(fecha_pedido.strftime('%A'), 'Desconocido')
        
        pedido = Pedido(
            nombre=order['Nombre'],
            direccion=order['Direccion'],
            telefono=order['Telefono'],
            tamano_pizza=order['Tamano'],
            ingredientes=order['Ingredientes'],
            num_pizzas=order['Num. Pizzas'],
            subtotal=order['Subtotal'],
            fecha_pedido=fecha_pedido,
            nombre_dia_semana=nombre_dia_semana_es,
            dia_del_mes=fecha_pedido.day,
            numero_mes=fecha_pedido.month,
            ano=fecha_pedido.year
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
            flash("Pedido eliminado con éxito.")
            break

    if orders:
        form = forms.PizzeriaForm(request.form)
        form.nombre.data = orders[0]['Nombre']
        form.direccion.data = orders[0]['Direccion']
        form.telefono.data = orders[0]['Telefono']
        form.tamanioPizza.data = orders[0]['Tamano']
        form.fechaPedido.data = orders[0]['FechaPedido']
        
    else:
        flash("No hay pedidos disponibles.")
        return redirect(url_for('pizzas'))

    print("ordenes: {}".format(orders))
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


from flask import render_template, request
from sqlalchemy import func, cast, Date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta







days_of_week = {
    "lunes": 1,
    "martes": 2,
    "miércoles": 3,
    "jueves": 4,
    "viernes": 5,
    "sábado": 6,
    "domingo": 7
}

months = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12
}


from sqlalchemy import func

@app.route('/ventas_acumuladas', methods=['GET', 'POST'])
def ventas_acumuladas():
    form = forms.VentasForm(request.form)

    if request.method == 'POST' and form.validate():
        dia = form.dia.data
        mes = form.mes.data
        ano = form.ano.data
        tipo = form.tipo.data
        
        print(dia, mes, ano, tipo)

        consulta = Pedido.query

        if tipo == 'dia' and dia:
            if dia.isdigit():
                dia_nombre = {v: k for k, v in days_of_week.items()}.get(int(dia))
                if dia_nombre:
                    consulta = consulta.filter(Pedido.nombre_dia_semana == dia_nombre)
            else:
                consulta = consulta.filter(Pedido.nombre_dia_semana == dia)
        elif tipo == 'mes' and mes:
            if mes.isdigit():
                mes_nombre = {v: k for k, v in months.items()}.get(int(mes))
                if mes_nombre:
                    consulta = consulta.filter(Pedido.numero_mes == int(mes))
            else:
                mes_numero = months.get(mes.lower())
                if mes_numero:
                    consulta = consulta.filter(Pedido.numero_mes == mes_numero)
        elif tipo == 'todos':
            pass

        if ano:
            consulta = consulta.filter(Pedido.ano == int(ano))

        ventas_agrupadas = consulta.group_by(Pedido.fecha_pedido, Pedido.nombre).with_entities(
            Pedido.fecha_pedido,
            Pedido.nombre,
            func.sum(Pedido.subtotal).label('total_subtotal')
        ).all()

        total_todas_las_ventas = sum(venta.total_subtotal for venta in ventas_agrupadas)

        return render_template('ventas_acumuladas.html', form=form, ventas=ventas_agrupadas, total_todas_las_ventas=total_todas_las_ventas, tipo=tipo)

    return render_template('ventas_acumuladas.html', form=form, ventas=None, total_todas_las_ventas=None, tipo=None)








from sqlalchemy import func, text






def obtener_resultados(fecha_ingresada, tipo):
    if tipo == 'dia':
        resultados = db.session.query(
            Pedido.nombre_dia_semana.label('DiaSemana'),
            Pedido.nombre.label('NombreCliente'),
            func.sum(Pedido.subtotal).label('TotalVentas')
        ) \
            .filter(Pedido.nombre_dia_semana == fecha_ingresada.lower()) \
            .group_by(Pedido.nombre_dia_semana, Pedido.nombre) \
            .order_by('DiaSemana', Pedido.nombre) \
            .all()
    elif tipo == 'mes':
        resultados = db.session.query(
            Pedido.numero_mes.label('NumeroMes'),
            Pedido.nombre.label('NombreCliente'),
            func.sum(Pedido.subtotal).label('TotalVentas')
        ) \
            .filter(Pedido.numero_mes == fecha_ingresada.month) \
            .group_by(Pedido.numero_mes, Pedido.nombre) \
            .order_by('NumeroMes', Pedido.nombre) \
            .all()
    else:
        resultados = []

    return resultados





if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
    app.run()
