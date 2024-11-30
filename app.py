"""
Este archivo contiene funciones para procesar texto y eliminar palabras antes de enviarlas 
para ser procesadas por un modelo de prediccion de emociones entrenado con KNIME.
"""

import unicodedata
from flask import Flask, render_template, request, jsonify, send_file
from jpmml_evaluator import make_evaluator

app = Flask(__name__)
evaluator = make_evaluator("assets/evaluator.pmml")

# Inicializar la lista de palabras a eliminar
palabras_eliminar = []

# Leer el archivo y agregar las palabras a la lista
with open('assets/palabras_eliminar.txt', 'r', encoding='utf-8') as file:
    palabras_eliminar = [linea.strip() for linea in file]

signos = [",", ".", ":", ";", "!", '"', "?", "¿", "¡", "(", ")","*", "-", "_", "´","¨", "'", "/"]

def eliminar_acentos(palabra):
    """
    Elimina los acentos de una palabra usando normalización Unicode.
    """
    return ''.join(
        (c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn')
    )

def procesar_texto(input_text):
    """
    Procesamiento y evaluacion de la entrada
    """

    if input_text == "":
        emocion_predominante = "No se ha introducido ninguna oración"
        return emocion_predominante

    # Recorremos la lista y eliminamos cada signo en la oración
    for signo in signos:
        input_text = input_text.replace(signo, "")

    # Dividir el texto en palabras
    palabras = input_text.split()

    # Filtrar "palabras" que son solo números
    palabras = [palabra for palabra in palabras if not palabra.isdigit()]

    # Eliminar acentos de las palabras
    palabras = [eliminar_acentos(palabra) for palabra in palabras]

    # Verificar si la palabra "no" está presente
    contiene_negacion = "no" in palabras
    prediccion_siguiente = ""
    if contiene_negacion:
        indice_negacion = palabras.index("no")
        if indice_negacion +2 < len(palabras):
            palabra_siguiente = palabras[indice_negacion +2]
            # Aquí podrías analizar `palabra_siguiente` según sea necesario
            if palabra_siguiente:
                # Realiza la evaluación de la "palabra_siguiente"
                arguments_siguiente = {"Reseña": palabra_siguiente}
                results_siguiente = evaluator.evaluate(arguments_siguiente)
                prediccion_siguiente = results_siguiente['Emocion']
                if prediccion_siguiente == "negativa":
                    emocion_predominante = "positiva"
                    return emocion_predominante
                if prediccion_siguiente == "positiva":
                    emocion_predominante = "negativa"
                    return emocion_predominante

    # Verificar si la palabra "pero" está presente
    contiene_pero = "pero" in palabras

    # Verificar si la palabra "aunque" está presente
    contiene_aunque = "aunque" in palabras

    # Verificar si la palabra "demasiado" está presente
    contiene_demasiado = "demasiado" in palabras
    if contiene_demasiado:
        indice_demasiado = palabras.index("demasiado")
        if indice_demasiado +1 < len(palabras):
            palabra_siguiente = palabras[indice_demasiado +1]
            # Aquí podrías analizar `palabra_siguiente` según sea necesario
            if palabra_siguiente:
                # Realiza la evaluación de la "palabra_siguiente"
                arguments_siguiente = {"Reseña": palabra_siguiente}
                results_siguiente = evaluator.evaluate(arguments_siguiente)
                prediccion_siguiente = results_siguiente['Emocion']
                if prediccion_siguiente == "negativa":
                    emocion_predominante = prediccion_siguiente
                    return emocion_predominante
                if prediccion_siguiente == "positiva":
                    emocion_predominante = prediccion_siguiente
                    return emocion_predominante

    # Verificar si la palabra "demasiada" está presente
    contiene_demasiada = "demasiada" in palabras
    if contiene_demasiada:
        indice_demasiada = palabras.index("demasiada")
        if indice_demasiada +1 < len(palabras):
            palabra_siguiente = palabras[indice_demasiada +1]
            # Aquí podrías analizar `palabra_siguiente` según sea necesario
            if palabra_siguiente:
                # Realiza la evaluación de la "palabra_siguiente"
                arguments_siguiente = {"Reseña": palabra_siguiente}
                results_siguiente = evaluator.evaluate(arguments_siguiente)
                prediccion_siguiente = results_siguiente['Emocion']
                if prediccion_siguiente == "negativa":
                    emocion_predominante = prediccion_siguiente
                    return emocion_predominante
                if prediccion_siguiente == "positiva":
                    emocion_predominante = prediccion_siguiente
                    return emocion_predominante

    # Verificar si la palabra "ademas" está presente
    contiene_ademas = "ademas" in palabras

    # Verificar si la palabra "mucho" está presente
    contiene_mucho = "mucho" in palabras
    if contiene_mucho:
        indice_mucho = palabras.index("mucho")
        palabra_ant = palabras[indice_mucho -1]
        if palabra_ant in ("hay", "es"):
            palabra_siguiente = palabras[indice_mucho +1]
            if palabra_siguiente:
                # Realiza la evaluación de la "palabra_siguiente"
                arguments_siguiente = {"Reseña": palabra_siguiente}
                results_siguiente = evaluator.evaluate(arguments_siguiente)
                prediccion_siguiente = results_siguiente['Emocion']
                if prediccion_siguiente == "negativa":
                    emocion_predominante = prediccion_siguiente
                    return emocion_predominante
                if prediccion_siguiente == "positiva":
                    emocion_predominante = prediccion_siguiente
                    return emocion_predominante
            if palabra_siguiente in ("trabajo", "trafico", "alboroto"):
                emocion_predominante = "negativa"
                return emocion_predominante

    # Verificar si la palabra "mucha" está presente
    contiene_mucha = "mucha" in palabras
    if contiene_mucha:
        indice_mucha = palabras.index("mucha")
        palabra_ant = palabras[indice_mucha -1]
        if palabra_ant in ("hay", "es"):
            palabra_siguiente = palabras[indice_mucha +1]
            if palabra_siguiente:
                # Realiza la evaluación de la "palabra_siguiente"
                arguments_siguiente = {"Reseña": palabra_siguiente}
                results_siguiente = evaluator.evaluate(arguments_siguiente)
                prediccion_siguiente = results_siguiente['Emocion']
                if prediccion_siguiente == "negativa":
                    emocion_predominante = prediccion_siguiente
                    return emocion_predominante
                if prediccion_siguiente == "positiva":
                    emocion_predominante = prediccion_siguiente
                    return emocion_predominante
            if palabra_siguiente in ("tarea", "aglomeracion", "gente"):
                emocion_predominante = "negativa"
                return emocion_predominante

    # Verificar si la palabra "tarde" está presente
    contiene_tarde = "tarde" in palabras
    if contiene_tarde:
        indice_tarde = palabras.index("tarde")
        palabra_ant = palabras[indice_tarde -1]
        if palabra_ant in ("la", "de"):
            palabras.pop(indice_tarde)

    # Verificar si la palabra "trabajo" está presente
    contiene_trabajo = "trabajo" in palabras
    if contiene_trabajo:
        indice_trabajo = palabras.index("trabajo")
        palabra_ant = palabras[indice_trabajo -1]
        if palabra_ant in ("el", "al", "del", "tu", "mi", "su", "nuestro"):
            palabras.pop(indice_trabajo)

    # Eliminar las palabras específicas de la lista palabras_eliminar
    palabras_filtradas = [palabra for palabra in palabras if palabra not in palabras_eliminar]

    if not palabras_filtradas:
        emocion_predominante = "No se detecta ninguna emoción en el texto"
        return emocion_predominante

    predicciones = {"positiva": 0, "negativa": 0, "neutral": 0}

    # Evaluar cada palabra
    for palabra in palabras_filtradas:
        arguments = {"Reseña": palabra}
        results = evaluator.evaluate(arguments)
        prediction = results['Emocion']

        if prediction:
            predicciones[prediction.lower()] += 1

    #Calcular las palabras negativas y postitivas
    positivas = predicciones["positiva"]
    negativas = predicciones["negativa"]
    neutrales = predicciones["neutral"]

    # Condicionamos segun las palabras "no" "pero" "ademas"
    if (contiene_negacion) & (positivas == 1) & (negativas == 0):
        emocion_predominante = "negativa"
        return emocion_predominante
    if (contiene_negacion) & (negativas == 1) & (positivas == 0):
        emocion_predominante = "positiva"
        return emocion_predominante
    if (contiene_negacion) & (contiene_ademas) & (positivas == negativas):
        emocion_predominante = "negativa"
        return emocion_predominante
    if (contiene_negacion) & (contiene_pero or contiene_aunque):
        emocion_predominante = "neutral"
        return emocion_predominante
    if (contiene_pero or contiene_aunque) & (positivas == negativas):
        emocion_predominante = "neutral"
        return emocion_predominante

    # Condición para empate entre positivo y negativo
    if (positivas == negativas) & (positivas > 0) & (negativas > 0):
        emocion_predominante = "neutral"
    elif (positivas == 0) & (negativas == 0) & (neutrales == 0):
        emocion_predominante = "No se detecta ninguna emoción en el texto"
    else:
        # Determinar la emoción predominante en base a la mayoría de predicciones
        emocion_predominante = max(predicciones, key=predicciones.get)

    return emocion_predominante

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Renderiza la página de inicio y maneja la evaluación del texto de entrada.

    Si la solicitud es POST, procesa el texto de entrada, elimina las palabras específicas,
    evalúa las palabras restantes utilizando el modelo PMML y retorna la predicción basada
    en la mayoría de las predicciones por palabra.
    """
    if request.method == "POST":
        if 'input_text' in request.form:
            input_text = request.form["input_text"].lower()
            emocion_predominante = procesar_texto(input_text)
            return jsonify(prediction=emocion_predominante)
        if 'input_file' in request.files:
            input_file = request.files["input_file"]
            if input_file and input_file.filename.endswith('.txt'):
                lineas_resultado = []
                for line in input_file.readlines():
                    input_text = line.decode('utf-8').strip().lower()
                    emocion_predominante = procesar_texto(input_text)
                    lineas_resultado.append(f"{input_text} - {emocion_predominante}\n")
                archivo =  'resultados.txt'
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.writelines(lineas_resultado)

                response = send_file(archivo, as_attachment=True)

                return response

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
