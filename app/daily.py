from app import db
from app.models import Cliente, Factura, Cuota

"""
En este modulo se especifican las acciones que debe hacer el programa 1 vez cada dia
    Hacer cada dia:
    Revisar cuotas vencidas
    Si hay cuotas vencidas, reportarlo a la factura y al cliente
"""

def Actualizacion_diaria(cuotas,fecha_actual):
    for cuota in cuotas:
        print(cuota.fecha.strftime("%j"))
        if cuota.fecha.strftime("%j") < fecha_actual.strftime("%j"):
            cuota.vencida=True
            cliente=Cliente.query.get(cuota.cliente_id)
            cliente.cliente_al_dia=False
            factura=Factura.query.get(cuota.factura_id)
            factura.al_dia=False
    db.session.commit()


def Actualizacion_abonar(cliente,factura_id):
    factura=Factura.query.get(factura_id)
    cuotas=factura.cuotas.all()
    cliente.cliente_al_dia=True
    factura.al_dia=True
    for cuota in cuotas:
        if cuota.vencida==True:
            cliente.cliente_al_dia=False
            factura.al_dia=False
    db.session.commit()


            
