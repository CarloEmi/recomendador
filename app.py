from flask import Flask, request, render_template, jsonify
import numpy as np
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

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

        # Obtener la carrera recomendada y el porcentaje de coincidencia
        carrera, porcentaje, _ = recomendar_carrera(intereses)

        # Explicar la recomendación de manera detallada
        # Explicar la recomendación de manera detallada
        mensaje = f"Basado en tus respuestas, se te recomienda la carrera de {carrera}. " \
                f"Tu perfil tiene un {porcentaje}% de coincidencia con esta carrera. " \
                "Esto significa que las respuestas que diste son muy compatibles con los intereses y habilidades necesarias para esta carrera. " \
                "Es importante recordar que esta es solo una aproximación y que puedes explorar otras opciones en informática. " \
                "La recomendación está basada en tus respuestas a un conjunto de preguntas relacionadas con habilidades y áreas de interés en el campo de la informática. " \
                "No significa que debas seguir esta recomendación exclusivamente, ya que las preferencias pueden cambiar con el tiempo."

        return jsonify({"carrera_recomendada": carrera, "porcentaje": porcentaje, "explicacion": mensaje})

    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)






"""
PRIMER EJEMPLO:
from flask import Flask, request, jsonify
import numpy as np
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

# Definición de las carreras y sus características
carreras = {
    'Analista en Sistemas de Computación': {'matematicas': 4, 'programacion': 5, 'interes_tech': 4},
    'Licenciatura en Sistemas de Información': {'matematicas': 5, 'programacion': 4, 'interes_tech': 5},
    'Profesorado Universitario en Computación': {'matematicas': 3, 'programacion': 3, 'interes_tech': 3},
    'Tecnicatura en Tecnologías de la Información': {'matematicas': 3, 'programacion': 3, 'interes_tech': 4},
}

def recomendar_carrera(intereses):

    Recomienda una carrera basada en los intereses del estudiante.
    :param intereses: Lista de enteros representando el nivel de interés en matemáticas, programación y tecnología.
    :return: Nombre de la carrera recomendada.

    # Convertir las características de las carreras a una matriz
    X = np.array([list(carrera.values()) for carrera in carreras.values()])
    y = list(carreras.keys())

    # Crear y entrenar el clasificador
    clf = DecisionTreeClassifier()
    clf.fit(X, y)

    # Predecir la carrera más adecuada
    carrera_recomendada = clf.predict([intereses])
    return carrera_recomendada[0]

# Ruta principal para recomendar carrera
@app.route('/recomendar', methods=['POST'])
def recomendar():
    try:
        data = request.get_json()
        intereses = data.get("intereses", [])

        # Validación de datos
        if not intereses or len(intereses) != 3:
            return jsonify({"error": "Se requieren tres valores de interés: matemáticas, programación y tecnología."}), 400

        # Convertir los intereses a enteros si es necesario
        intereses = list(map(int, intereses))

        # Obtener la recomendación
        carrera = recomendar_carrera(intereses)
        return jsonify({"carrera_recomendada": carrera})

    except ValueError:
        return jsonify({"error": "Los valores de interés deben ser números enteros."}), 400
    except Exception as e:
        return jsonify({"error": f"Ocurrió un error inesperado: {e}"}), 500


if __name__ == "__main__":
    # Ejecuta la aplicación Flask en modo debug
    app.run(debug=True, host="0.0.0.0", port=8000)
"""