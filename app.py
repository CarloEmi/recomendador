from flask import Flask, request, render_template, jsonify,  redirect, url_for
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import firebase_admin
import os
from firebase_admin import credentials, firestore
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email
from uuid import uuid4


app = Flask(__name__)
app.secret_key = 'secret_key'

#app.secret_key = os.environ.get('SECRET_KEY', 'una_clave_por_defecto')


# Base de conocimiento ajustada para las carreras
reglas = [
     {"si": {'herramientas_tech': 5, 'investiga_tech': 4, 'mant_redes': 3, 'apoyo_tech': 4, 'trabajo_equipos': 5,
        'ingenieria_software': 3, 'diseno_sistemas': 4, 'actualizacion_ciencia': 3, 'liderazgo_proyectos': 2,
        'docencia_universitaria': 1, 'investigacion_educativa': 2, 'actualizacion_tech': 4}, 
     "entonces": {"carrera": "Tecnicatura Universitaria en Tecnologías de la Información", "puntaje": 80}},
       
    {"si": {'herramientas_tech': 5, 'investiga_tech': 5, 'mant_redes': 4, 'apoyo_tech': 3, 'trabajo_equipos': 4,
        'ingenieria_software': 5, 'diseno_sistemas': 4, 'actualizacion_ciencia': 4, 'liderazgo_proyectos': 3,
        'docencia_universitaria': 1, 'investigacion_educativa': 3, 'actualizacion_tech': 4}, 
     "entonces": {"carrera": "Analista en Sistemas de Computación", "puntaje": 88}},

    {"si": {'herramientas_tech': 4, 'investiga_tech': 5, 'mant_redes': 3, 'apoyo_tech': 4, 'trabajo_equipos': 5,
        'ingenieria_software': 4, 'diseno_sistemas': 3, 'actualizacion_ciencia': 5, 'liderazgo_proyectos': 5,
        'docencia_universitaria': 1, 'investigacion_educativa': 4, 'actualizacion_tech': 4}, 
     "entonces": {"carrera": "Licenciatura en Sistemas de Información", "puntaje": 85}},
    
     {"si": {'herramientas_tech': 2, 'investiga_tech': 3, 'mant_redes': 1, 'apoyo_tech': 3, 'trabajo_equipos': 4,
        'ingenieria_software': 2, 'diseno_sistemas': 3, 'actualizacion_ciencia': 4, 'liderazgo_proyectos': 5,
        'docencia_universitaria': 5, 'investigacion_educativa': 5, 'actualizacion_tech': 4}, 
     "entonces": {"carrera": "Profesorado Universitario en Computación", "puntaje": 90}},
    
]

#Motor de inferencia
def motor_inferencia(hechos, reglas):
    resultados = []  # Almacena los hechos derivados durante el proceso
    
    for regla in reglas:
        condiciones = regla["si"]
        
        # Verificar qué tan cerca están los hechos de las condiciones
        coincidencias = sum(1 for k, v in condiciones.items() if hechos.get(k, 0) == v)
        total_condiciones = len(condiciones)
        porcentaje_coincidencia = (coincidencias / total_condiciones) * 100
        
        # Si hay coincidencias significativas, derivar la conclusión
        if porcentaje_coincidencia > 50:  # Umbral ajustable
            conclusion = regla["entonces"]
            conclusion["porcentaje_coincidencia"] = porcentaje_coincidencia
            resultados.append(conclusion)
    
    # Seleccionar la recomendación con el mayor puntaje
    if resultados:
        mejor_recomendacion = max(resultados, key=lambda x: x["puntaje"])
        return [mejor_recomendacion]
    else:
        return [{"carrera": "Sin recomendación", "puntaje": 0}]


def recomendar_carrera(respuestas):
    # Procesar las respuestas en hechos
    hechos = procesar_respuestas(respuestas)

    # Ejecutar el motor de inferencia
    resultados = motor_inferencia(hechos, reglas)

    # Seleccionar la carrera con mayor puntaje
    if resultados:
        mejor_recomendacion = max(resultados, key=lambda x: x["puntaje"])
        carrera = mejor_recomendacion["carrera"]
        porcentaje = mejor_recomendacion["puntaje"]
        return carrera, porcentaje
    else:
        return "Sin recomendación", 0


#Validaciones de los campos del formulario
class PersonalInfoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    dni = StringField('DNI', validators=[DataRequired()])
    #email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[DataRequired()])

# Rutas
# Ruta para mostrar el formulario de datos personales
@app.route('/')
def datos_personales():
    return render_template('personal_info.html')

# Ruta para guardar los datos personales
@app.route('/guardar_datos_personales', methods=['POST'])
def guardar_datos_personales():
    try:
        # Verificar qué datos llegan en la solicitud
        print(request.form)
        """
        Validar campos requeridos
        campos_requeridos = ['nombre', 'dni', 'email', 'telefono']
        for campo in campos_requeridos:
            if campo not in data or not data[campo].strip():
                return jsonify({"error": f"El campo '{campo}' es obligatorio."}), 400

        
        Validar formato del correo (opcional)
        if "@" not in data['email']:
            return jsonify({"error": "El correo no tiene un formato válido."}), 400
        """
        # Obtener los datos del formulario
        data = {
            'nombre': request.form['nombre'],
            'dni': request.form['dni'],
            'email': request.form['email'],
            'telefono': request.form['telefono']
        }
        
        # Guardar los datos en Firebase
        doc_ref = db.collection("datos personales").document(data['nombre'])
        doc_ref.set({
            "nombre": data['nombre'],
            "dni": data['dni'],
            "email": data['email'],
            "telefono": data['telefono'],
        })
        return redirect(url_for('preguntas'))

    except Exception as e:
        app.logger.error(f"Error al guardar los datos personales: {str(e)}") 
        return f"Hubo un problema al procesar tus datos: {str(e)}", 500 


# Ruta para mostrar el formulario de preguntas
@app.route('/preguntas', methods=['GET'])
def preguntas():
    return render_template('preguntas.html')


# Ruta de recomendación
@app.route('/recomendar', methods=['POST'])
def recomendar():
    try:
        # Recoger las respuestas del formulario como un diccionario
        data = request.form.to_dict()

        # Obtener la carrera recomendada y el porcentaje
        carrera, porcentaje = recomendar_carrera(data)

        # Detalles de las respuestas
        detalles = {"respuestas": data}

        # Guardar los resultados en Firebase
        guardar_resultados(data, carrera, porcentaje, detalles)

        return render_template("resultados.html", carrera=carrera, porcentaje=porcentaje)
    except Exception as e:
        app.logger.error(f"Error al procesar el formulario: {e}")
        return jsonify({"error": f"Ocurrió un error inesperado: {e}"}), 500


# Ruta para recibir y procesar respuestas del formulario
def procesar_respuestas(respuestas):
    try:
        # Recoger las respuestas del formulario como un diccionario
        data = request.form.to_dict()
        # Asumir que las claves del formulario coinciden con las características de entrada
        hechos = {
            "herramientas_tech": int(respuestas.get("herramientas_tech", 0)),
            "investiga_tech": int(respuestas.get("investiga_tech", 0)),
            "mant_redes": int(respuestas.get("mant_redes", 0)),
            "apoyo_tech": int(respuestas.get("apoyo_tech", 0)),
            "trabajo_equipos": int(respuestas.get("trabajo_equipos", 0)),
            "ingenieria_software": int(respuestas.get("ingenieria_software", 0)),
            "diseno_sistemas": int(respuestas.get("diseno_sistemas", 0)),
            "actualizacion_ciencia": int(respuestas.get("actualizacion_ciencia", 0)),
            "liderazgo_proyectos": int(respuestas.get("liderazgo_proyectos", 0)),
            "docencia_universitaria": int(respuestas.get("docencia_universitaria", 0)),
            "investigacion_educativa": int(respuestas.get("investigacion_educativa", 0)),
            "actualizacion_tech": int(respuestas.get("actualizacion_tech", 0)),
        }
        return hechos
        
    except Exception as e:
        app.logger.error(f"Error al procesar el formulario: {e}")
        return jsonify({"error": f"Ocurrió un error inesperado: {e}"}), 500



# Ruta para visualizar las estadísticas desde Firebase
@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    resultados = db.collection("resultados").stream()
    estadisticas = {}
    
    for doc in resultados:
        data = doc.to_dict()
        carrera = data["carrera_recomendada"]
        estadisticas[carrera] = estadisticas.get(carrera, 0) + 1

    return jsonify(estadisticas)

# Configuración para enviar correos
from flask_mail import Mail, Message

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='tu_email@gmail.com',
    MAIL_PASSWORD='tu_contraseña'
)
mail = Mail(app)

# Inicializar Firebase

cred = credentials.Certificate(os.path.abspath("recomendador-8df4f-firebase-adminsdk-m7sh4-d1ff9c85e5.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()

# Función para enviar correos
def enviar_correo(destinatario, asunto, cuerpo):
    msg = Message(asunto, sender=app.config["MAIL_USERNAME"], recipients=[destinatario])
    msg.body = cuerpo
    mail.send(msg)
    
# Guardar resultados en Firebase
def guardar_resultados(data, carrera, porcentaje, detalles):
    try: 
        doc_id = f"{data['nombre']}_{uuid4()}"  # Genera un ID único
        doc_ref = db.collection("resultados").document(doc_id)
        doc_ref.set({
            "nombre": data['nombre'],
            "dni": data['dni'],
            "email": data['email'],
            "telefono": data['telefono'],
            "carrera_recomendada": carrera,
            "porcentaje": porcentaje,
            "detalles": detalles
        })
        # PREPARAR ENTORNO PARA ENVIO DE CORREOS
        """
        enviar_correo(
            destinatario=data['email'],
            asunto="Resultados del Test Vocacional",
            cuerpo=f"Hola {data['nombre']}, se te recomienda la carrera '{carrera}' con un {porcentaje}% de coincidencia."
        )
        """
        pass
    except Exception as e:
        app.logger.error(f"Error al guardar resultados en Firebase: {e}")



if __name__ == '__main__':
    app.run(debug=True)