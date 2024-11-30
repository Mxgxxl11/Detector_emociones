document.getElementById('emotionForm').addEventListener('submit', function(event) {  
    event.preventDefault(); // Evita el envío del formulario normal  

    let inputText = document.getElementById('input_text').value;  
    let inputFile = document.getElementById('input_file').files[0];  
    let xhr = new XMLHttpRequest();  

    // Muestra el loader  
    document.getElementById('loader').style.display = 'block';  
    document.getElementById('predictionResult').innerText = ''; // Limpia la predicción anterior  

    xhr.open('POST', '/', true);  

    xhr.onload = function() {  
        document.getElementById('loader').style.display = 'none'; // Oculta el loader al recibir respuesta

        if (xhr.status === 200) {  
            const contentType = xhr.getResponseHeader('Content-Type');

            if (contentType && contentType.includes('application/json')) {
                // Si la respuesta es JSON
                let response = JSON.parse(xhr.responseText);  
                if (response.prediction) {
                    // Cambia el color de fondo según la predicción
                    if (response.prediction === "positiva") {  
                        document.body.style.backgroundColor = "#d4edda";  
                    } else if (response.prediction === "negativa") {  
                        document.body.style.backgroundColor = "#f8d7da";  
                    } else if (response.prediction === "neutral") {  
                        document.body.style.backgroundColor = "#fff3cd";  
                    } else {  
                        document.body.style.backgroundColor = "#f0f0f0";  
                    }  
                    document.getElementById('predictionResult').innerText = 'Predicción: ' + response.prediction;  
                } else {
                    document.getElementById('predictionResult').innerText = 'Error en la respuesta del servidor';
                }
            } else if (contentType && contentType.includes('text/plain')) {
                // Si la respuesta es un archivo
                const blob = new Blob([xhr.response], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'resultados.txt'; // Nombre del archivo a descargar
                document.body.appendChild(a);
                a.click();
                a.remove();
                URL.revokeObjectURL(url); // Libera el objeto URL
            } else {
                document.getElementById('predictionResult').innerText = 'Tipo de respuesta no reconocido';
            }
        } else {
            document.getElementById('predictionResult').innerText = 'Error al procesar la solicitud';
        }  
    };  

    // Enviar el archivo o el texto
    let formData = new FormData();
    if (inputText) {
        formData.append('input_text', inputText);
    }
    if (inputFile) {
        formData.append('input_file', inputFile);
    }
    if(inputText && inputFile){
        alert("Por favor, envía solo uno: texto o archivo.");
        document.getElementById('loader').style.display = 'none';
        return false;
    }

    xhr.send(formData); // Envía el formulario con texto o archivo
});