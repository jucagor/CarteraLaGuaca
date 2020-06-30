from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, IntegerField, BooleanField, DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class IngresoClientesForm(FlaskForm):
    id = IntegerField('Identificacion', validators=[DataRequired()])
    tipo_identificacion = StringField('Tipo de identificacion', validators=[DataRequired()])
    nombre = StringField('Nombre del cliente', validators=[DataRequired()])
    email = StringField('Correo electronico')
    recibir_notificaciones = BooleanField('Recibir notificaciones')
    numero_tel= StringField('Numero de telefono', validators=[DataRequired()])
    direccion = StringField('Direccion', validators=[DataRequired()])
    descripcion = StringField('Descripcion')
    submit = SubmitField('Registrar')

class IngresoFacturaForm(FlaskForm):
    id = IntegerField('Numero de factura', validators=[DataRequired()])
    cliente_id = IntegerField('Identificacion del cliente', validators=[DataRequired()])
    monto = IntegerField('Valor de la factura', validators=[DataRequired()])
    vigencia = StringField('vigencia de la factura')
    descripcion = StringField('Descripcion')
    contado = BooleanField('Factura de contado?')
    numero_cuotas = IntegerField('Numero de cuotas')
    periodicidad_cuotas = IntegerField('Periodicidad de cuotas en dias')
    submit = SubmitField('Registrar')
    vendedor = StringField('Vendedor')

class IngresoAbonoForm(FlaskForm):
    id = IntegerField('Numero de abono', validators=[DataRequired()])
    factura_id = IntegerField('Numero de factura a abonar', validators=[DataRequired()])
    monto = IntegerField('Valor del Abono', validators=[DataRequired()])
    descripcion = StringField('Descripcion')
    reduccion_cuotas = BooleanField('Reduccion de cuotas?')
    abono_capital = BooleanField('Abono a capital?')

    submit = SubmitField('Registrar')
