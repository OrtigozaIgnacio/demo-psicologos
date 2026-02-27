from flask import Flask, request, jsonify, render_template
import os
from datetime import datetime, timedelta, time

app = Flask(__name__, static_folder='../frontend', static_url_path='', template_folder='../frontend')

# --- VARIABLES DINÁMICAS (MODO DEMO - ESPAÑOL) ---
NOMBRE_PROFESIONAL = os.environ.get("NOMBRE_PROFESIONAL", "Lic. María Gómez")
ESPECIALIDAD = os.environ.get("ESPECIALIDAD", "Psicología Clínica")

# Horarios configurables
HORA_INICIO_LABORAL = int(os.environ.get("HORA_INICIO_LABORAL", 9))
HORA_FIN_LABORAL = int(os.environ.get("HORA_FIN_LABORAL", 18))
DURACION_SESION = int(os.environ.get("DURACION_SESION", 60))

# --- LÓGICA DE NEGOCIO SIMULADA (MOCK) ---
def generar_slots_libres_mock(servicio='fisico'):
    """
    Simulador de agenda: Genera turnos libres para los próximos 14 días
    sin necesidad de conectarse a un Google Calendar real.
    """
    slots_disponibles = []
    ahora = datetime.now()
    
    duracion_minutos = DURACION_SESION if servicio != 'consulta' else 20
    
    for i in range(1, 15):
        fecha_evaluar = ahora + timedelta(days=i)
        
        # De Lunes a Viernes (0 al 4)
        if fecha_evaluar.weekday() > 4:
            continue

        hora_actual = datetime.combine(fecha_evaluar.date(), time(HORA_INICIO_LABORAL, 0))
        hora_fin_dia = datetime.combine(fecha_evaluar.date(), time(HORA_FIN_LABORAL, 0))

        while hora_actual + timedelta(minutes=duracion_minutos) <= hora_fin_dia:
            # Simulamos el horario de almuerzo excluyendo las 13 hs
            if hora_actual.hour == 13:
                hora_actual += timedelta(minutes=60)
                continue

            # En la versión demo asumimos que todos los turnos generados están libres
            slots_disponibles.append(hora_actual.isoformat())
                
            hora_actual += timedelta(minutes=duracion_minutos)
                
    return slots_disponibles

@app.route('/api/disponibilidad', methods=['GET'])
def obtener_disponibilidad():
    servicio = request.args.get('servicio', 'fisico')
    # Devolvemos los slots generados de forma automática
    return jsonify({"slots_disponibles": generar_slots_libres_mock(servicio)})

@app.route('/api/agendar', methods=['POST'])
def crear_turno():
    # En la versión demo, NO guardamos en Base de Datos ni llamamos a Mercado Pago.
    # Simplemente devolvemos un estado especial 'demo' para que el frontend (index.html) 
    # sepa que debe mostrar el Pop-up elegante de venta.
    return jsonify({
        "status": "demo",
        "message": "Simulación completada. Mostrar modal de venta."
    }), 200

# --- RUTAS DE FRONTEND ---

# 1. Ruta Original (Mercado Hispano / Argentina)
@app.route('/')
def index():
    return render_template(
        'index.html', 
        nombre=NOMBRE_PROFESIONAL, 
        especialidad=ESPECIALIDAD
    )

# 2. NUEVA Ruta Internacional (Mercado Estados Unidos)
@app.route('/en')
@app.route('/en/')
def index_en():
    # Usamos variables en inglés para que la demo impacte al cliente de EE. UU.
    return render_template(
        'en/index.html', 
        nombre=os.environ.get("NOMBRE_PROFESIONAL_EN", "Dr. John Doe"), 
        especialidad=os.environ.get("ESPECIALIDAD_EN", "Psychiatrist")
    )

if __name__ == '__main__':
    print("🚀 Servidor DEMO iniciando en http://127.0.0.1:8000")
    app.run(host='0.0.0.0', port=8000)