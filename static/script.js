document.getElementById('emotionForm').addEventListener('submit', function(event) {  
    event.preventDefault(); // Evita el envío del formulario normal  

    let inputText = document.getElementById('input_text').value;  
    let xhr = new XMLHttpRequest();  
    
    // Muestra el loader  
    document.getElementById('loader').style.display = 'block';  
    document.getElementById('predictionResult').innerText = ''; // Limpia la predicción anterior  
    
    xhr.open('POST', '/', true);  
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');  
    xhr.onload = function() {  
        if (xhr.status === 200) {  
            // Mantener el loader visible por un segundo, luego ocultarlo  
            setTimeout(() => {  
                document.getElementById('loader').style.display = 'none';  
                
                // Analiza la respuesta y muestra la predicción  
                let response = JSON.parse(xhr.responseText);  
                if (response.prediction === "positiva") {  
                    document.body.style.backgroundColor = "#d4edda";  
                    document.getElementById('predictionResult').innerText = 'Predicción: ' + response.prediction;  
                } else if (response.prediction === "negativa") {  
                    document.body.style.backgroundColor = "#f8d7da";  
                    document.getElementById('predictionResult').innerText = 'Predicción: ' + response.prediction;  
                } else if (response.prediction === "neutral") {  
                    document.body.style.backgroundColor = "#fff3cd";  
                    document.getElementById('predictionResult').innerText = 'Predicción: ' + response.prediction;  
                } else {  
                    document.body.style.backgroundColor = "#f0f0f0";  
                    document.getElementById('predictionResult').innerText = response.prediction;  
                }  
            }, 1000); // Espera 1 segundo antes de ocultar el loader y mostrar la predicción  
        }  
    };  
    xhr.send('input_text=' + encodeURIComponent(inputText)); // Envía la oración  
});
