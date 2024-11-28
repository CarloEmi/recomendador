# FCEQyN, Universidad Nacional de Misiones.

    Materia: Tesis de Grado.
    Docente: Dr. Eduardo Zamudio. 
    Tutor/a: Mgter. Alice Rambo.
    Carrera: Licenciatura en Sistemas de Información.
    Estudiante: Carlos Emiliano Pereyra.
    Año:2024
* Enlace al documento del trabajo: 
[Documento de la Tesis](https://docs.google.com/document/d/1ajJu8LG7SIt8Ziu1GNKXSIN8mHBav75LwIoOJ-uF8pQ/edit?usp=sharing)
* Enlace a las preguntas elaboradas por expertos: [Documento de las preguntas](https://docs.google.com/document/d/1t8bP1550hPkPzNRexBAPPmEphUsMNMdgiOOAmUf8gsM/edit?usp=sharing)

## Sistema recomendador de carreras

 ### Ejecutar el proyecto y probar la interfaz
**IMPORTANTE: Clonar el proyecto en la carpeta de destino a elección.** Luego seguir los pasos a continuación
1. Tener instalado [python](https://www.python.org/downloads/)

2. Instalar Flask  
    * Ejecutar en la terminal: pip install flask (instalar pip)


3. Herramientas Adicionales para ejecutar el Recomendador de Carreras:
    * Instalar Numpy: 
        * pip install numpy
    * Instalar Pandas: 
        * pip install pandas
    * Instalar Scikit-Learn: 
        * pip install scikit-learn
    * Instalar Matplotlib y Seaborn: 
        * pip install matplotlib seaborn
    * Instalar NLTK: 
        * pip install nltk

4. Luego ejecutar app.py :  
    * python app.py 

5. Acceder a http://127.0.0.1:5000/preguntas en tu navegador para ver el formulario.
Se deben completar las preguntas y envíar el formulario para recibir la recomendación de carrera.


### **Fundamentación** del uso de herramientas adicionales

- **Numpy**
 Es una librería fundamental para cálculos matemáticos y científicos en Python.

- **Pandas**
Es una librería clave para la manipulación y análisis de datos.

- **Scikit-Learn**
Es una librería robusta para aprendizaje automático y minería de datos. Permitirá implementar algoritmos de machine learning, que son esenciales para el sistema recomendador.

- **Matplotlib y Seaborn**
Estas librerías son útiles para la visualización de datos. Ayudan a entender los patrones en los datos, lo cual es crucial para afinar las recomendaciones.

- **NLTK** (Natural Language Toolkit):
Si el recomendador necesita incluir procesamiento de texto (por ejemplo, si los estudiantes describen sus intereses en palabras), NLTK es una herramienta para analizar y entender ese texto.