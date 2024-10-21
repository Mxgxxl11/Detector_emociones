"""
Este módulo contiene funciones para procesar texto y eliminar palabras antes de enviarlas 
para ser procesadas por un modelo de prediccion de emociones entrenado con Knime.
"""

import unicodedata
from flask import Flask, render_template, request, jsonify
from jpmml_evaluator import make_evaluator

app = Flask(__name__)
evaluator = make_evaluator("ia3.pmml")

# Lista de palabras a eliminar
palabras_eliminar = ["muy", "yo", "tu", "nuestro", "nosotros", "somos", "ella",
                     "esta", "son", "poco", "mucho", "ademas", "incluso", "el",
                     "algo", "y", "pero", "o", "es", "tarde", "tampoco", "eres",
                     "dia", "noche", "fue", "estoy", "estamos", "estas", "me",
                     "sus", "su", "ese", "eso", "esto", "era", "eres"]

signos = [",", ".", ":", ";", "!", '"', "?", "¿", "¡", "(", ")","*", "-", "_", "´", "'", "/"]

def eliminar_acentos(palabra):
    """
    Elimina los acentos de una palabra usando normalización Unicode.
    """
    return ''.join(
        (c for c in unicodedata.normalize('NFD', palabra) if unicodedata.category(c) != 'Mn')
    )

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Renderiza la página de inicio y maneja la evaluación del texto de entrada.

    Si la solicitud es POST, procesa el texto de entrada, elimina las palabras específicas,
    evalúa las palabras restantes utilizando el modelo PMML y retorna la predicción basada
    en la mayoría de las predicciones por palabra.
    """
    if request.method == "POST":
        input_text = request.form["input_text"].lower()

        # Recorremos la lista y eliminamos cada signo en la oración
        for signo in signos:
            input_text = input_text.replace(signo, "")

        # Dividir el texto en palabras
        palabras = input_text.split()

        # Eliminar acentos de las palabras
        palabras = [eliminar_acentos(palabra) for palabra in palabras]

        # Verificar si la palabra "no" está presente
        contiene_negacion = "no" in palabras

        # Eliminar las palabras específicas de la lista palabras_eliminar
        palabras_filtradas = [palabra for palabra in palabras if palabra not in palabras_eliminar]

        if not palabras_filtradas:
            return jsonify(prediction="No se detecta ninguna emoción en el texto")

        predicciones = {"positiva": 0, "negativa": 0, "neutral": 0}

        # Evaluar cada palabra restante
        for palabra in palabras_filtradas:
            arguments = {"Reseña": palabra}
            results = evaluator.evaluate(arguments)
            prediction = results['Emocion']

            if prediction:
                predicciones[prediction.lower()] += 1

        #Calcular las palabras negativas y postitivas
        positivas = predicciones["positiva"]
        negativas = predicciones["negativa"]

        # Condición para empate entre positivo y negativo
        if (positivas == negativas) & (positivas > 0) & (negativas > 0):
            emocion_predominante = "neutral"

        elif prediction is None:
            return jsonify(prediction="No se detecta ninguna emoción en el texto")

        else:
            # Determinar la emoción predominante en base a la mayoría de predicciones
            emocion_predominante = max(predicciones, key=predicciones.get)

        # Si se encontró la palabra "no", invertimos la predicción
        if contiene_negacion:
            if emocion_predominante == "positiva":
                emocion_predominante = "negativa"
            elif emocion_predominante == "negativa":
                emocion_predominante = "positiva"

        return jsonify(prediction=emocion_predominante)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
