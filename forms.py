from wtforms import Form
from wtforms import StringField, TextAreaField,SelectField, RadioField, IntegerField, BooleanField, DateField
from wtforms import EmailField
from wtforms import validators

class UserForm(Form):
    nombre=StringField("nombre",[
        validators.DataRequired(message='el campo es reuqerido'),
        validators.length(min=4,max=10,message='ingrese nombre válido')
        ])
    apaterno=StringField("apaterno")
    amaterno=StringField("amaterno")
    edad=IntegerField('edad',[
        validators.number_range(min=1,max=20,message='valor no válido')
    ])
    correo=EmailField("correo",[
        validators.Email(message='Ingrese un correo válido')
    ])
    #materias=SelectField(choices=[('Español','Esp'),('Mat', 'Matematicas'),('Ingles','IN')])
    #radios=RadioField('Curso',choices=[('1','1'),('2','2'),('3','3')])
    
class UserForm2(Form):
    id=IntegerField('id')
    nombre=StringField("nombre",[
        validators.DataRequired(message='el campo es reuqerido'),
        validators.length(min=4,max=10,message='ingrese nombre válido')
        ])
    apaterno=StringField("apaterno")
    email=EmailField("correo",[
        validators.Email(message='Ingrese un correo válido')
    ])
    
class UserForm3(Form):
    id=IntegerField('id')
    segnombre=StringField("segnombre",[
        validators.DataRequired(message='el campo es requerido'),
        validators.length(min=4,max=10,message='ingrese nombre válido')
        ])
    amaterno=StringField("amaterno")
    telefono=StringField('telefono',[
        validators.length(min=1,max=11,message='valor no válido')
    ])
    añoNac=StringField('añoNac',[
        validators.length(min=1,max=4,message='valor no válido')
    ])
    edad=IntegerField('edad',[
        validators.number_range(min=1,max=99,message='valor no válido')
    ])
    
class PizzeriaForm(Form):
    nombre=StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=20,message='Ingrese nombre válido')
        ])
    direccion=StringField("Direccion",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=20,message='Ingrese dirección válida')
        ])
    telefono=StringField('Telefono',[
        validators.length(min=1,max=11,message='valor no válido')
    ])
    tamanioPizza=RadioField('Tamaño Pizza',choices=[('Chica','Chica $40'),('Mediana','Mediana $80'),('Grande','Grande  $120')])
    jamon=BooleanField('Jamón $10')
    pinia=BooleanField('Piña $10')
    champiniones=BooleanField('Champiñones $10')
    numPizzas=IntegerField("Num de Pizzas",[validators.number_range(min=1,max=99, message='Valor no válido')])
    
class VentasForm(Form):
    fecha = DateField('Fecha', validators=[validators.DataRequired()], format='%Y-%m-%d')
    tipo = RadioField('Tipo', choices=[('dia', 'Día'), ('mes', 'Mes'), ('todos', 'Todos')], default='todos')
    