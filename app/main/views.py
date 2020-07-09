from app.main import main
from app.forms import IngresoClientesForm, IngresoFacturaForm, IngresoAbonoForm
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.models import Cliente, Factura, Abono, Usuario, Cuota
from app import db
from datetime import datetime, timedelta
from app.daily import Actualizacion_diaria, Actualizacion_abonar

global Actualizar_Cuotas
Actualizar_Cuotas=False
@main.route('/')
@login_required
def index():
    cuotas= Cuota.query.all()
    fecha_actual=datetime.now()
    #fecha_actual=datetime(2020, 8, 13)
    global dia
    global Actualizar_Cuotas
    try:
        # se actualizan las cuotas cuando: 
        #   El programa detecte que es un nuevo dia por medio de la variable dia
        #   El programa detecte que se encuentra en un año muchas mayor
        #   El programa detecte que necesita actualizar, ya sea que se halla ingresado una nueva factura o un nuevo abono
        if dia.strftime("%j") < datetime.now().strftime("%j") or dia.strftime("%y") > datetime.now().strftime("%y") or Actualizar_Cuotas:
            Actualizacion_diaria(cuotas,fecha_actual)
            Actualizar_Cuotas=False
            print("normal")
    except:
        dia=datetime.now()
        Actualizacion_diaria(cuotas,fecha_actual)
        print("excepcion")

    clientes= Cliente.query.all()
    context = {
    'fecha_actual':fecha_actual,
    'clientes': clientes,
    'cuotas':cuotas,
    'usuario': current_user
    }    
    return(render_template('index.html', **context))

@main.route('/visualizar_cuotas')
@login_required
def visualizar_cuotas():
    cuotas= Cuota.query.all()
    fecha_actual=datetime.now()    
    clientes= Cliente.query.all()
    context = {
    'fecha_actual':fecha_actual,
    'clientes': clientes,
    'cuotas':cuotas,
    'usuario': current_user
    }    
    return(render_template('visualizar_cuotas.html', **context))

@main.route('/visualizacion_clientes')
@login_required
def visualizacion_clientes():

    clientes= Cliente.query.all()
    context = {
    'clientes': clientes,
    'usuario': current_user

    }    
    return(render_template('visualizacion_clientes.html', **context))

@main.route('/detalle_cliente')
@login_required
def detalle_cliente():

    id_cliente=request.args.get('id','None')
    if id_cliente is not None:
        cliente=Cliente.query.get(id_cliente)
        facturas=cliente.facturas.all()
 
    context = {
    'facturas':facturas,
    'cliente': cliente,
    'usuario': current_user
    }

    return(render_template('detalles_cliente.html',**context))

@main.route('/ingreso_cliente', methods=['GET','POST'])
@login_required
def ingreso_cliente():
    ingreso_clientes_form=IngresoClientesForm()
    
    if ingreso_clientes_form.validate_on_submit():

        cliente = Cliente()
        cliente.id = ingreso_clientes_form.id.data
        cliente.tipo_identificacion = ingreso_clientes_form.tipo_identificacion.data
        cliente.nombre = ingreso_clientes_form.nombre.data
        cliente.email = ingreso_clientes_form.email.data
        cliente.recibir_notificaciones = ingreso_clientes_form.recibir_notificaciones.data
        cliente.numero_tel = ingreso_clientes_form.numero_tel.data
        cliente.direccion = ingreso_clientes_form.direccion.data
        cliente.descripcion = ingreso_clientes_form.descripcion.data
        db.session.add(cliente)
        db.session.commit()
        flash('Cliente agregado con exito')

    context = {
    'ingreso_clientes_form':ingreso_clientes_form,
    'usuario': current_user
    }

    return(render_template('ingreso_cliente.html',**context))

@main.route('/visualizacion_facturas')
@login_required
def visualizacion_facturas():

    clientes= Cliente.query.all()
    facturas=Factura.query.all()
    context = {
    'clientes':clientes,
    'facturas': facturas,
    'usuario': current_user

    }    
    return(render_template('visualizacion_facturas.html', **context))

@main.route('/detalle_factura')
@login_required
def detalle_factura():
    clientes= Cliente.query.all()
    id_factura=request.args.get('id','None')
    if id_factura is not None:
        factura=Factura.query.get(id_factura)
 
    context = {
    'clientes':clientes,
    'factura': factura,
    'usuario': current_user
    }

    return(render_template('detalles_factura.html',**context))
    

@main.route('/ingreso_factura', methods=['GET','POST'])
@login_required
def ingreso_factura():
    global Actualizar_Cuotas
    id_cliente=request.args.get('id','None')
    ingreso_Factura_form=IngresoFacturaForm()
    hoy=datetime.now().strftime("%Y-%m-%d")
    if ingreso_Factura_form.validate_on_submit():
        factura = Factura()
        factura.id = ingreso_Factura_form.id.data
        factura.cliente_id = ingreso_Factura_form.cliente_id.data
        factura.monto = ingreso_Factura_form.monto.data
        factura.vendedor= ingreso_Factura_form.vendedor.data
        # formato="%Y-%m-%d"
        # factura.fecha = datetime.strptime(ingreso_Factura_form.fecha.data,formato)
        factura.fecha = ingreso_Factura_form.fecha.data
        factura.descripcion = ingreso_Factura_form.descripcion.data
        factura.contado = ingreso_Factura_form.contado.data

        if factura.contado:
            factura.cancelada=True
            factura.al_dia=True
            factura.numero_cuotas=0
            factura.periodicidad_cuotas=0
            factura.saldo=0
            factura.vigencia= factura.fecha
        else:
            factura.numero_cuotas = ingreso_Factura_form.numero_cuotas.data
            factura.periodicidad_cuotas = ingreso_Factura_form.periodicidad_cuotas.data
            factura.saldo = factura.monto
            factura.vigencia= factura.fecha + timedelta(days=factura.periodicidad_cuotas*factura.numero_cuotas)

            for i in range (1,1+factura.numero_cuotas):
                cuota=Cuota()
                cuota.id=int(str(factura.id)+str(0)+str(i))
                cuota.factura_id=factura.id
                cuota.numero=i
                cuota.monto=int(factura.saldo/factura.numero_cuotas)
                cuota.fecha=factura.fecha + timedelta(days=(factura.periodicidad_cuotas*i))
                cuota.cliente_id=factura.cliente_id
                db.session.add(cuota)
        #Se actualiza el saldo del cliente

        cliente=Cliente.query.get(factura.cliente_id)
        cliente.saldo=cliente.saldo+factura.saldo
        

        if db.session.query(Factura).filter_by(id=factura.id).count() < 1:
            db.session.add(factura)
            db.session.commit()
            flash('Factura agregado con exito')
        else:
            flash('factura ya existe')
        Actualizar_Cuotas=True

    context = {
    'id_cliente':id_cliente,
    'ingreso_factura_form':ingreso_Factura_form,
    'usuario': current_user,
    'hoy': hoy
    }

    return(render_template('ingreso_factura.html',**context))

@main.route('/visualizacion_abonos')
@login_required
def visualizacion_abonos():

    facturas= Factura.query.all()
    abonos=Abono.query.all()
    context = {
    'facturas':facturas,
    'abonos': abonos,
    'usuario': current_user

    }    
    return(render_template('visualizacion_abonos.html', **context))

@main.route('/ingreso_abono', methods=['GET','POST'])
@login_required
def ingreso_abono():
    global Actualizar_Cuotas
    monto=request.args.get('monto','None')
    id_factura=request.args.get('id','None')
    ingreso_Abono_form=IngresoAbonoForm()
    hoy=datetime.now().strftime("%Y-%m-%d")

    if ingreso_Abono_form.validate_on_submit():
        abono = Abono()
        abono.id = ingreso_Abono_form.id.data
        abono.factura_id = ingreso_Abono_form.factura_id.data
        abono.monto = ingreso_Abono_form.monto.data        
        abono.descripcion = ingreso_Abono_form.descripcion.data
        abono.reduccion_cuotas=ingreso_Abono_form.reduccion_cuotas.data
        abono.abono_capital=ingreso_Abono_form.abono_capital.data
        abono.fecha = ingreso_Abono_form.fecha.data

        factura=Factura.query.get(abono.factura_id)
        factura.saldo=factura.saldo-abono.monto
        
        cliente=Cliente.query.get(factura.cliente_id)
        cliente.saldo=cliente.saldo-abono.monto

        # SI es una reduccion a cuotas, empieza a descontar el saldo desde las primeras cuotas hasta las ultimas
        if abono.reduccion_cuotas:
            cuotas=factura.cuotas.all()
            valor_a_abonar=abono.monto
            for cuota in cuotas:
                if valor_a_abonar < cuota.monto:
                    cuota.monto=cuota.monto-valor_a_abonar
                    break
                if valor_a_abonar == cuota.monto:
                    db.session.delete(cuota)
                    break
                if valor_a_abonar > cuota.monto:
                    valor_a_abonar=valor_a_abonar-cuota.monto
                    db.session.delete(cuota)
        
        #Si es un abono a capital, el valor del abono se divide entre el numero de cuotas, y se descuento a cada cuota
        if abono.abono_capital:
            cuotas=factura.cuotas.all()
            valor_a_abonar=abono.monto
            disminucion_en_cuota=int(abono.monto/len(cuotas))
            excedente=0
            for cuota in cuotas:
                cuota.monto=cuota.monto-(disminucion_en_cuota+excedente)
                excedente=0
                if cuota.monto<0:
                    excedente=abs(cuota.monto)
                    db.session.delete(cuota)
                if cuota.monto==0:
                    db.session.delete(cuota)  

        db.session.add(abono)
        db.session.commit()
        #se Realiza una acutalizacion en la base de datos sobre el cliente que abona, y la factura.
        Actualizacion_abonar(cliente,abono.factura_id)
        flash('Abono agregado con exito')
        Actualizar_Cuotas=True

    context = {
    'id_factura':id_factura,
    'monto':monto,
    'ingreso_Abono_form':ingreso_Abono_form,
    'usuario': current_user,
    'hoy': hoy
    }

    return(render_template('ingreso_abono.html',**context))
