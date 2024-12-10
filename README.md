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

### Descripción del sistema

El **Sistema Experto de Recomendación de Carreras** es una herramienta diseñada para orientar a los estudiantes sobre la mejor carrera en informática que se ajuste a sus intereses y habilidades. El sistema utiliza un motor de inferencia para procesar las respuestas de los estudiantes a una serie de preguntas formuladas por psicopedagogas y generar una recomendación personalizada de carrera. Las recomendaciones se basan en un conjunto de reglas que correlacionan características personales y profesionales del estudiante con distintas carreras informáticas.

Este sistema de recomendación de carreras está diseñado para ser una herramienta útil que asista a los estudiantes en su proceso de elección de carrera, basándose en un análisis lógico de sus respuestas y preferencias. Con el uso de tecnologías modernas como Flask y bibliotecas de Python, ofrece una experiencia interactiva y precisa para la toma de decisiones académicas.

### Tecnologías utilizadas para el desarrollo del sistema
1. **Base de datos:** Firebase.
2. **Framework:** Flask
3. **Lenguaje de programación:** Python 3.12.6.

 ### Ejecutar el proyecto y probar la interfaz
**IMPORTANTE: Clonar el proyecto en la carpeta de destino a elección.** Luego seguir los pasos a continuación
1. **Instalar Python**  
   Si no tienes Python instalado, puedes descargarlo desde [aquí](https://www.python.org/downloads/). Asegúrate de seleccionar la opción de añadir Python al PATH durante la instalación.

2. **Instalar Flask**  
   Flask es el framework utilizado para crear la aplicación web.  
   En la terminal, ejecuta:  
   ```bash
   pip install flask

3. Tecnologías necearias para ejecutar el Recomendador de Carreras:

- El sistema está desarrollado con las siguientes herramientas, **para su funcionamiento debe instalar las siguientes librerías**:
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

5. Acceder a la interfaz;
    - http://127.0.0.1:5000 en tu navegador para ver el formulario. Se debe completar el formulario y luego envíarlo para recibir la recomendación de carrera.


### **Fundamentación** del uso de Tecnologías utilizadas

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