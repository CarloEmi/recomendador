from flask import Flask, request, render_template, jsonify,  redirect, url_for
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import firebase_admin
import os
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

app = Flask(__name__)
app.secret_key = 'secret_key'


# Base de conocimiento ajustada para las carreras
carreras = {
    'Tecnicatura Universitaria en Tecnologías de la Información': {
        'herramientas_tech': 5, 'investiga_tech': 4, 'mant_redes': 3, 'apoyo_tech': 4, 'trabajo_equipos': 5,
        'ingenieria_software': 3, 'diseno_sistemas': 4, 'actualizacion_ciencia': 3, 'liderazgo_proyectos': 2,
        'docencia_universitaria': 1, 'investigacion_educativa': 2, 'actualizacion_tech': 4
    },
    'Analista en Sistemas de Computación': {
        'herramientas_tech': 5, 'investiga_tech': 5, 'mant_redes': 4, 'apoyo_tech': 3, 'trabajo_equipos': 4,
        'ingenieria_software': 5, 'diseno_sistemas': 4, 'actualizacion_ciencia': 4, 'liderazgo_proyectos': 3,
        'docencia_universitaria': 1, 'investigacion_educativa': 3, 'actualizacion_tech': 4
    },
    'Licenciatura en Sistemas de Información': {
        'herramientas_tech': 4, 'investiga_tech': 5, 'mant_redes': 3, 'apoyo_tech': 4, 'trabajo_equipos': 5,
        'ingenieria_software': 4, 'diseno_sistemas': 3, 'actualizacion_ciencia': 5, 'liderazgo_proyectos': 5,
        'docencia_universitaria': 1, 'investigacion_educativa': 4, 'actualizacion_tech': 4
    },
    'Profesorado Universitario en Computación': {
        'herramientas_tech': 2, 'investiga_tech': 3, 'mant_redes': 1, 'apoyo_tech': 3, 'trabajo_equipos': 4,
        'ingenieria_software': 2, 'diseno_sistemas': 3, 'actualizacion_ciencia': 4, 'liderazgo_proyectos': 5,
        'docencia_universitaria': 5, 'investigacion_educativa': 5, 'actualizacion_tech': 4
    }
}

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

# Cargar variables de entorno desde el archivo .env
load_dotenv()
print("Ruta al archivo de credenciales:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


# Obtener la ruta al archivo de credenciales desde la variable de entorno

cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if cred_path is None:
    raise Exception("La variable de entorno 'GOOGLE_APPLICATION_CREDENTIALS' no está configurada.")


# Usar el archivo de credenciales para inicializar Firebase
cred = credentials.Certificate(cred_path)
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
        doc_ref = db.collection("resultados").document(data['nombre'])
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

# Función para recomendar la carrera
def recomendar_carrera(intereses):
    # Convertir las respuestas en un array de características
    X = np.array([list(carrera.values()) for carrera in carreras.values()])
    y = list(carreras.keys())
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    
    # Predecir la carrera recomendada
    carrera_recomendada = clf.predict([intereses])[0]
    
    # Calcular el porcentaje de coincidencia con cada carrera
    distancias = np.linalg.norm(X - intereses, axis=1)  # Calculando la distancia euclidiana
    coincidencias = 1 / (1 + distancias)  # Convertir distancia en un valor de similitud (aproximación)
    porcentaje = round(coincidencias[list(y).index(carrera_recomendada)] * 100, 2)  # Porcentaje de coincidencia

    return carrera_recomendada, porcentaje, coincidencias

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
        return jsonify({"error": f"Ocurrió un error: {e}"}), 500


# Ruta para mostrar el formulario de preguntas
@app.route('/preguntas', methods=['GET'])
def preguntas():
    return render_template('preguntas.html')

# Ruta para recibir y procesar respuestas del formulario
@app.route('/recomendar', methods=['POST'])
def recomendar():
    try:
        # Recoger las respuestas del formulario como un diccionario
        data = request.form.to_dict()
        # Asumir que las claves del formulario coinciden con las características de entrada
        intereses = [
            int(data.get("herramientas_tech", 0)),
            int(data.get("investiga_tech", 0)),
            int(data.get("mant_redes", 0)),
            int(data.get("apoyo_tech", 0)),
            int(data.get("actualizacion_tech", 0)),
            int(data.get("trabajo_equipos", 0)),
            int(data.get("ingenieria_software", 0)),
            int(data.get("diseno_sistemas", 0)),
            int(data.get("actualizacion_ciencia", 0)),
            int(data.get("liderazgo_proyectos", 0)),
            int(data.get("docencia_universitaria", 0)),
            int(data.get("investigacion_educativa", 0)),
        ]

        # Obtener la carrera recomendada y el porcentaje
        carrera, porcentaje, coincidencias = recomendar_carrera(intereses)

         # Explicación detallada
        detalles = {
            "coincidencias": list(coincidencias),
            "respuestas": intereses
        }
          # Guardar los resultados en Firebase
        guardar_resultados(data, carrera, porcentaje, detalles)

        return render_template("resultados.html", carrera=carrera, porcentaje=porcentaje)
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


if __name__ == '__main__':
    app.run(debug=True)