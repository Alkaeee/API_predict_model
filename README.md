# API Flask con Modelo de Machine Learning

1. Este proyecto es una API Flask simple que utiliza un modelo de machine learning para realizar predicciones. La API incluye tres métodos principales:

## 1. Metodos:

1. **Predicción con Método GET:** 
   - Endpoint: `/predict`
   - Método: GET
   - Descripción: Este endpoint te permite realizar una predicción utilizando el modelo entrenado. 
        - Debes proporcionar un json con tres datos float en la consulta para obtener la predicción.


   Ejemplo de uso:
   ```bash
   GET "http://localhost:5000/predict"
   example json = {"data" : [[100,100,100]]}
2. **Ingreso de Datos con Método POST:**
    -Endpoint: /ingresar-datos
    -Método: POST
    -Descripción: Este endpoint te permite ingresar cuatro datos para agregar al conjunto de datos de entrenamiento del modelo.

    -Ejemplo de uso:
   ```bash
   POST "http://localhost:5000/ingest"
   example json = {"data" : [[100,100,100, 999]]}
3. **Reentrenamiento con Método POST:**

    -Endpoint: /retrain
    -Método: POST
    -Descripción: Este endpoint te permite realizar un reentrenamiento del modelo con los nuevos datos ingresados. Asegúrate de tener suficientes datos antes de realizar esta -operación.

    -Ejemplo de uso:
   ```bash
   POST "http://localhost:5000/retrain"
## 2. Configuración y Ejecución

- Instalación de Dependencias:
    - ``pip install -r requirements.txt``
- Ejecutar la Aplicación:
    -  ``python app.py``
- La aplicación se ejecutará en http://127.0.0.1:5000/ de forma predeterminada.

## 3. Uso con Docker

- Puedes descargar la imagen Docker de esta API desde Docker Hub utilizando el siguiente comando: 
    - ``docker pull javieralcazar/api-final-docker`` 
- Para ejecutar la imagen: 
    - ``docker run -p 5000:5000 javieralcazar/api-final-docker``
