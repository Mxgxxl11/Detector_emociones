// ─── Toast helper ────────────────────────────────────────────────────────────

function showToast(message, type = 'default') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast ' + (type === 'error' ? 'error' : '');
    toast.classList.add('show');
    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => toast.classList.remove('show'), 3500);
}

// ─── Upload zone interactions ─────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
    const inputText   = document.getElementById('input_text');
    const inputFile   = document.getElementById('input_file');
    const uploadZone  = document.getElementById('uploadZone');
    const uploadLabel = document.getElementById('uploadLabel');

    // Mutual exclusion
    inputText.addEventListener('input', () => {
        if (inputText.value.trim() !== '') {
            inputFile.value = '';
            uploadZone.classList.remove('has-file');
            uploadLabel.textContent = 'Seleccionar archivo';
        }
    });

    inputFile.addEventListener('change', () => {
        if (inputFile.files.length > 0) {
            inputText.value = '';
            uploadZone.classList.add('has-file');
            uploadLabel.textContent = inputFile.files[0].name;
        } else {
            uploadZone.classList.remove('has-file');
            uploadLabel.textContent = 'Seleccionar archivo';
        }
    });

    // Drag & drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-over');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('drag-over');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (!file) return;
        const allowed = ['text/plain', 'text/csv',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
        if (!allowed.some(t => file.type === t) &&
            !file.name.match(/\.(txt|csv|xlsx)$/i)) {
            showToast('Formato no permitido. Usa TXT, CSV o XLSX.', 'error');
            return;
        }
        const dt = new DataTransfer();
        dt.items.add(file);
        inputFile.files = dt.files;
        inputText.value = '';
        uploadZone.classList.add('has-file');
        uploadLabel.textContent = file.name;
    });
});

// ─── Form submit ──────────────────────────────────────────────────────────────

document.getElementById('emotionForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const inputText  = document.getElementById('input_text').value.trim();
    const inputFile  = document.getElementById('input_file').files[0];
    const submitBtn  = document.getElementById('submitBtn');
    const resultBox  = document.getElementById('resultBox');
    const badge      = document.getElementById('predictionResult');

    // Validation
    if (inputText && inputFile) {
        showToast('Envía solo uno: texto o archivo.', 'error');
        return;
    }

    if (!inputText && !inputFile) {
        showToast('Escribe un texto o selecciona un archivo.', 'error');
        return;
    }

    // Start loading state
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    resultBox.classList.remove('visible');

    const formData = new FormData();
    if (inputText) formData.append('input_text', inputText);
    if (inputFile)  formData.append('input_file', inputFile);

    const xhr = new XMLHttpRequest();
    if (inputFile) xhr.responseType = 'blob';

    xhr.open('POST', '/', true);

    xhr.onload = function () {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;

        if (xhr.status !== 200) {
            showToast('Error al procesar la solicitud.', 'error');
            return;
        }

        const contentType = xhr.getResponseHeader('Content-Type') || '';

        // ── JSON prediction (text input) ──────────────────────────────────
        if (contentType.includes('application/json')) {
            const response = JSON.parse(xhr.responseText);

            if (!response.prediction) {
                showToast('Respuesta inesperada del servidor.', 'error');
                return;
            }

            const prediction = response.prediction.toLowerCase();

            badge.textContent = response.prediction;
            badge.className = 'result__badge';
            if (prediction === 'positiva')  badge.classList.add('positive');
            else if (prediction === 'negativa') badge.classList.add('negative');
            else if (prediction === 'neutral')  badge.classList.add('neutral');
            else                                badge.classList.add('unknown');

            resultBox.classList.add('visible');

        // ── File download (file input) ────────────────────────────────────
        } else if (
            contentType.includes('text/plain') ||
            contentType.includes('text/csv') ||
            contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        ) {
            const blob = new Blob([xhr.response], { type: contentType });
            const url  = URL.createObjectURL(blob);
            const a    = document.createElement('a');
            a.href = url;

            if (contentType.includes('text/csv'))         a.download = 'resultados.csv';
            else if (contentType.includes('spreadsheetml')) a.download = 'resultados.xlsx';
            else                                            a.download = 'resultados.txt';

            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);

            showToast('Archivo descargado correctamente.');

        } else {
            showToast('Tipo de respuesta no reconocido.', 'error');
        }
    };

    xhr.onerror = function () {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
        showToast('Error de conexión con el servidor.', 'error');
    };

    xhr.send(formData);
});
